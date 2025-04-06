# pdf_service.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import base64
from PyPDF2 import PdfMerger

class PDFGenerator:
    @staticmethod
    def generate_similarity_report(results):
        """
        Genera un PDF con los resultados del análisis de similitud.
        
        Args:
            results (list): Lista de resultados de ImageSimilarityResNet
            
        Returns:
            bytes: Contenido del PDF generado
        """
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
        
        # Título del documento
        print("Título del documento")
        story.append(Paragraph("Reporte de Análisis de Imágenes Médicas", styles['CenterTitle']))
        
        for i, result in enumerate(results):
            # Sección para cada imagen
            print(f"Procesando imagen {i+1}")
            story.append(Paragraph(f"Imagen {i+1}", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Mostrar el porcentaje de similitud
            print("Mostrar el porcentaje de similitud")
            story.append(Paragraph(
                f"Porcentaje de similitud promedio: {result['average_similarity_percentage']:.2f}%",
                styles['Normal']
            ))
            
            # Mostrar el mensaje de diagnóstico
            print("Mostrar el mensaje de diagnóstico")
            story.append(Paragraph(
                f"Diagnóstico: {result['diagnosis_message']}",
                styles['Normal']
            ))
            story.append(Spacer(1, 12))
            
            print("Mostrar la imagen desde bytes (nuevo enfoque)")
            # Mostrar la imagen desde bytes (nuevo enfoque)
            try:
                img = Image(io.BytesIO(result['pacient_image_bytes']), 
                          width=4*inch, height=4*inch)
                story.append(img)
            except Exception as e:
                story.append(Paragraph("No se pudo cargar la imagen", styles['Normal']))
                print(f"Error al cargar imagen: {e}")
            
            # Agregar salto de página si no es la última imagen
            print("Agregar salto de página si no es la última imagen")
            if i < len(results) - 1:
                story.append(PageBreak())
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()