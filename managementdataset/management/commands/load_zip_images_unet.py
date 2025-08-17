from django.core.management.base import BaseCommand
from managementdataset.serializer import ZipImageUploadSerializer
import os
from django.core.files.base import ContentFile
from zipfile import ZipFile
from django.core.files.storage import default_storage
from vectorization.models import ImageResizer

class Command(BaseCommand):
    help = 'Load images from a ZIP file'

    def handle(self, *args, **options):
        zip_path = r'C:\Users\yefer\OneDrive\Escritorio\imagenes_test\bancounet.zip'
        from django.core.files.base import File

        with open(zip_path, 'rb') as f:
            django_file = File(f, name=os.path.basename(zip_path))
            self.vectorize_and_save_images(django_file)

    def vectorize_and_save_images(self, django_file):
        zip_file = django_file
        images = []
        ex = False;

        image_resizer = ImageResizer()
        print('INITIALIZING VECTORIZATION')
        cont = 0
        try:
            with ZipFile(zip_file, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    cont = cont + 1
                    print(f'>>>>IMAGEN {cont} | nombre de archivo: {file_name}')
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        image_file = zip_ref.read(file_name)
                        image_content = ContentFile(image_file, name=file_name)

                        resized_images, resized_images_base64 = image_resizer.procesar_imagenes([image_content], 512, 512)

                        resized_image = resized_images[0]
                        original_path = default_storage.save("uploads/" + resized_image.name, ContentFile(resized_image.read())) 
                print('VECTORIZATION FINISHED')
        except Exception as e:
            ex = f'Failed reading, segmenting or saving the image. Reason: {e}'
            print(ex)

        return True
