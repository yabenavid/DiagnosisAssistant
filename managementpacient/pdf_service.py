import io
import os
import base64
import fitz
import tempfile
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table,
    TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

def base64_to_compressed_image(base64_str, width, height, quality=95):
    img_data = base64.b64decode(base64_str)
    pil_img = PILImage.open(io.BytesIO(img_data)).convert("RGB")

    # No modificar resolución original
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return Image(buffer, width=width, height=height)

class PDFGenerator:
    @staticmethod
    def generate_similarity_report(results, resized_images_base64, doctor_name=None, elevation_maps=None, apply_image_compression=False):
        def build_pdf(apply_compression):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()

            styles.add(ParagraphStyle(
                name='CenterTitle',
                parent=styles['Title'],
                alignment=TA_CENTER,
                spaceAfter=20
            ))

            story = []

            story.append(Spacer(1, 3 * inch))  # Centrar verticalmente
            story.append(Paragraph("Reporte de Análisis de Imágenes Médicas", styles['CenterTitle']))
            story.append(PageBreak())

            for i, (result, resized_b64) in enumerate(zip(results, resized_images_base64)):
                elevation_b64 = elevation_maps[i] if elevation_maps and elevation_maps[i] else None

                analysis_block = []

                analysis_block.append(Paragraph(f"Análisis {i+1}", styles['Heading2']))
                analysis_block.append(Spacer(1, 12))

                analysis_block.append(Paragraph(
                    f"Porcentaje de similitud: {result['average_similarity_percentage']:.2f}%",
                    styles['Normal']
                ))
                analysis_block.append(Paragraph(
                    f"Diagnóstico: {result['diagnosis_message']}",
                    styles['Normal']
                ))
                analysis_block.append(Spacer(1, 18))  # REDUCIDO de 24 a 18

                try:
                    if apply_compression:
                        resized_img = base64_to_compressed_image(resized_b64, width=3*inch, height=3*inch, quality=85)
                        segmented_img = base64_to_compressed_image(result['pacient_image'], width=3*inch, height=3*inch, quality=85)
                        if elevation_b64:
                            elevation_img = base64_to_compressed_image(elevation_b64, width=3*inch, height=3*inch, quality=85)
                    else:
                        resized_img = Image(io.BytesIO(base64.b64decode(resized_b64)), width=3*inch, height=3*inch)
                        segmented_img = Image(io.BytesIO(base64.b64decode(result['pacient_image'])), width=3*inch, height=3*inch)
                        if elevation_b64:
                            elevation_img = Image(io.BytesIO(base64.b64decode(elevation_b64)), width=3*inch, height=3*inch)

                    if elevation_b64:
                        img_table_top = Table([
                            ["Imagen Original", "Mapa de elevación"],
                            [resized_img, elevation_img]
                        ], colWidths=[3.2*inch, 3.2*inch])

                        img_table_bottom = Table([
                            ["Imagen Segmentada"],
                            [segmented_img]
                        ], colWidths=[6.5*inch])

                        for t in [img_table_top, img_table_bottom]:
                            t.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('FONTSIZE', (0, 0), (-1, 0), 10),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ]))

                        analysis_block.append(img_table_top)
                        analysis_block.append(Spacer(1, 12))
                        analysis_block.append(img_table_bottom)

                    else:
                        img_table = Table([
                            ["Imagen Original", "Imagen Segmentada"],
                            [resized_img, segmented_img]
                        ], colWidths=[3.2*inch, 3.2*inch])

                        img_table.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ]))

                        analysis_block.append(img_table)

                except Exception as e:
                    analysis_block.append(Paragraph(f"Error al cargar imágenes: {str(e)}", styles['Normal']))

                # Quitar Spacer grande aquí para evitar desborde
                # analysis_block.append(Spacer(1, 24))  ← eliminar esta línea

                analysis_block.append(Paragraph(
                    f"Evaluación realizada por Dr. {doctor_name}" if doctor_name else "Evaluación realizada por el asistente de diagnóstico OncoJuntas.",
                    styles['Italic']
                ))

                # Salto de página antes del análisis (excepto el primero)
                if i > 0:
                    story.append(PageBreak())

                # Añadir todo como bloque unido
                story.append(KeepTogether(analysis_block))

            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        # 1. Generar PDF en alta calidad
        pdf_data = build_pdf(apply_compression=False)

        # 2. Verificar tamaño
        if len(pdf_data) > 25 * 1024 * 1024:
            print("PDF supera 25MB, regenerando con compresión de imágenes...")
            pdf_data = build_pdf(apply_compression=True)

            # 3. Compresión adicional con fitz
            fd_in, path_in = tempfile.mkstemp(suffix=".pdf")
            fd_out, path_out = tempfile.mkstemp(suffix=".pdf")
            os.close(fd_in)
            os.close(fd_out)
            try:
                with open(path_in, "wb") as f_in:
                    f_in.write(pdf_data)

                doc = fitz.open(path_in)
                doc.save(path_out, deflate=True, garbage=3, clean=True)
                doc.close()

                with open(path_out, "rb") as f_out:
                    pdf_data = f_out.read()
            finally:
                os.remove(path_in)
                os.remove(path_out)

        return pdf_data
