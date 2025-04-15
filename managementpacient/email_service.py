# managementpacient/utils/email_service.py
from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email_with_pdf(subject, body, to_emails, pdf_content, filename="diagnostico.pdf"):
        """
        Envía un email con PDF adjunto
        
        Args:
            subject (str): Asunto del email
            body (str): Cuerpo del email
            to_emails (list): Lista de emails destinatarios
            pdf_content (bytes): Contenido binario del PDF
            filename (str): Nombre del archivo adjunto
        """
        try:
            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                to_emails
            )
            email.attach(filename, pdf_content, 'application/pdf')
            email.send()
            return True
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False