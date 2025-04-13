# pdf_service.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import base64

class PDFGenerator:
    @staticmethod
    def generate_similarity_report(results, resized_images_base64, doctor_name=None):
        """
        Genera un PDF con ambas imágenes (redimensionada y segmentada) lado a lado.
        
        Args:
            results (list): Resultados de ImageSimilarityResNet (contiene segmented_pacient_image)
            resized_images_base64 (list): Lista de imágenes redimensionadas en base64
            doctor_name (str): Nombre del médico que realiza el análisis
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el título
        styles.add(ParagraphStyle(
            name='CenterTitle',
            parent=styles['Title'],
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        story = []
        
        # Título del documento
        story.append(Paragraph("Reporte de Análisis de Imágenes Médicas", styles['CenterTitle']))
        
        for i, (result, resized_b64) in enumerate(zip(results, resized_images_base64)):
            # Sección para cada imagen
            story.append(Paragraph(f"Análisis {i+1}", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Datos de diagnóstico
            story.append(Paragraph(
                f"Similitud promedio: {result['average_similarity_percentage']:.2f}%", 
                styles['Normal']
            ))
            story.append(Paragraph(
                f"Diagnóstico: {result['diagnosis_message']}", 
                styles['Normal']
            ))
            story.append(Spacer(1, 24))
            
            # Tabla con ambas imágenes lado a lado
            try:
                # Decodificar imágenes
                resized_img = Image(io.BytesIO(base64.b64decode(resized_b64)), width=3*inch, height=3*inch)
                segmented_img = Image(io.BytesIO(base64.b64decode(result['pacient_image'])), width=3*inch, height=3*inch)
                
                # Crear tabla de 2 columnas
                img_table = Table([
                    ["Imagen Original", "Imagen Segmentada"],
                    [resized_img, segmented_img]
                ], colWidths=[4*inch, 4*inch])
                
                # Estilo de la tabla
                img_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('FONTSIZE', (0,0), (-1,0), 10),
                    ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ]))
                
                story.append(img_table)
                
            except Exception as e:
                story.append(Paragraph(f"Error al cargar imágenes: {str(e)}", styles['Normal']))
            
            story.append(Spacer(1, 24))
    
            if doctor_name:
                analysis_text = f"Evaluación realizada por Dr. {doctor_name}"
            else:
                analysis_text = "Evaluación realizada por el asistente de diagnóstico OncoJuntas."
                
            story.append(Paragraph(analysis_text, styles['Italic']))
            
            if i < len(results) - 1:
                story.append(PageBreak())
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()