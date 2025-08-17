from django.core.management.base import BaseCommand
from managementdataset.serializer import ZipImageUploadSerializer
import os

class Command(BaseCommand):
    help = 'Load images from a ZIP file using the serializer'

    def handle(self, *args, **options):
        zip_path = r'C:\Users\yefer\OneDrive\Escritorio\imagenes_test\CARGADATASET\2017-06-09_18.08.16.ndpi.16.17875_16008.2048x2048.zip'
        segment_model = '2'
        from django.core.files.base import File

        with open(zip_path, 'rb') as f:
            django_file = File(f, name=os.path.basename(zip_path))
            data = {
                'zip_file': django_file,
                'segment_model': segment_model
            }
            serializer = ZipImageUploadSerializer(data=data)
            if serializer.is_valid():
                result = serializer.save()
                self.stdout.write(self.style.SUCCESS(f"Resultado: {result}"))
            else:
                self.stdout.write(self.style.ERROR(f"Errores de validación: {serializer.errors}"))
