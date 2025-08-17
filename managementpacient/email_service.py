# managementpacient/utils/email_service.py
from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email_with_pdf(subject, body, to_emails, pdf_content, filename="diagnostico.pdf"):
        """
        Sends an email with a PDF attachment.
        
        Args:
            subject (str): Email subject
            body (str): Email body
            to_emails (list): List of recipient email addresses
            pdf_content (bytes): PDF binary content
            filename (str): Attachment file name
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