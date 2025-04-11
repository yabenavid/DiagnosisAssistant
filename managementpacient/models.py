# models.py
from django.db import models
from managementhospital.models import Hospital
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class History(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    s3_pdf_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'

    def __str__(self):
        return f"Reporte {self.id} - Hospital {self.hospital.name}"

class HistoryStorage(S3Boto3Storage):
    location = 'history'
    file_overwrite = False
    default_acl = 'private'