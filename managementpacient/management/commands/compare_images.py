import os
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from vectorization.models import ImageResizer
from segmentation.models import SamImageSegmenter, SkimageSegmenter, UnetImageSegmenter
from similaritysearch.models import ImageSimilarityResNet

class Command(BaseCommand):
    help = 'Procesa imágenes de una carpeta, las segmenta y ejecuta métricas, exportando los resultados a un CSV.'

    def handle(self, *args, **options):
        # --- Configura aquí las rutas y parámetros ---
        input_folder = r'C:\Users\yefer\OneDrive\Escritorio\imagenes_test\imagenesNoCancerTestReducida'
        segment_model = '2'  # '1' para SAM, '2' para Skimage , '3' para unet
        output_csv = r'C:\Users\yefer\OneDrive\Escritorio\resultado_metricas.csv'
        dataset_folder = r'C:\Users\yefer\OneDrive\Escritorio\imagenes_test\bancoskimage2'

        # --- Leer imágenes de la carpeta ---N
        print('Leyendo imágenes de la carpeta...')
        image_files = []
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                image_path = os.path.join(input_folder, filename)
                with open(image_path, 'rb') as f:
                    file_bytes = f.read()
                    uploaded_file = SimpleUploadedFile(
                        name=filename,
                        content=file_bytes,
                        content_type='image/png'  # Cambia si necesitas otro tipo
                    )
                    image_files.append(uploaded_file)

        if not image_files:
            self.stdout.write(self.style.ERROR('No se encontraron imágenes en la carpeta especificada.'))
            return

        # --- Vectorización (redimensionar imágenes) ---
        print('Vectorizando imágenes...')
        image_resizer = ImageResizer()
        resized_images, _ = image_resizer.procesar_imagenes(image_files)

        # --- Segmentación ---
        print('Segmentando imágenes...')
        if segment_model == '1':
            segmenter_instance = SamImageSegmenter()
            print('Usando SAM para segmentación...')
            segmented_images = segmenter_instance.segment_images(resized_images)
            segment_type = 'SAM'
        elif segment_model == '2':
            segmenter_instance = SkimageSegmenter()
            print('Usando Scikit Image para segmentación...')
            segmented_images = segmenter_instance.segment_images(resized_images)
            segment_type = 'Scikit Image'
        elif segment_model == '3':
            segmenter_instance = UnetImageSegmenter()
            print('Usando U-Net para segmentación...')
            segmented_images = segmenter_instance.segment_images(image_files)
            segment_type = 'U-Net'
        else:
            self.stdout.write(self.style.ERROR('segment_model debe ser "1" (SAM) o "2" (Skimage)'))
            return

        # --- Similaridad y exportar CSV ---
        print('Calculando similitud y exportando a CSV...')
        similarity_checker = ImageSimilarityResNet()
        similarity_checker.run_all_metrics_and_export_csv(
            segmented_images, segment_type, output_path=output_csv, dataset_folder=dataset_folder
        )

        self.stdout.write(self.style.SUCCESS(f'Proceso completado. CSV generado en: {output_csv}'))
        