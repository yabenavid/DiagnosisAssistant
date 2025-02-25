# views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from segmentation.models import SamImageSegmenter
from similaritysearch.models import ImageSimilarity
from vectorization.models import ImageResizer

@csrf_exempt
def segment_image(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        try:
            image_files = request.FILES.getlist("images")
            segment_model = request.POST.get("segment_model", None)

            # Depuración: imprimir los datos POST recibidos
            print("POST data:", request.POST)
            print("segment_model:", segment_model)

            if segment_model is None:
                return HttpResponse("segment_model parameter is missing", status=400)


            print('INITIALIZING VECTORIZATION')

            # Procesar las imágenes usando pyvips para estandarizarlas y mejorar su calidad
            image_resizer = ImageResizer()
            resized_images = image_resizer.procesar_imagenes(image_files)

            print('VECTORIZATION FINISHED')


            print('INITIALIZING SEGMENTATION')

            if (segment_model == '1'):
                print('Cargando modelo de sam')
                segmenter = SamImageSegmenter()
                print('Segmentando')
                segmented_images = segmenter.segment_images(resized_images)
            elif (segment_model == '2'):
                segmenter = SamImageSegmenter()
                segmented_images = segmenter.segment_images(resized_images, image_path = 'uploads/imagen.jpg')
            else:
                return HttpResponse("Invalid segmentation model param", status=400)

            print('SEGMENTATION FINISHED')

            similarity_checker = ImageSimilarity()

            similarity_checker.calculate_similarity()
            # # Crear un archivo ZIP con las imágenes segmentadas
            # zip_buffer = segmenter.create_zip(segmented_images)

            # # Devolver el archivo ZIP como respuesta HTTP
            # response = HttpResponse(zip_buffer, content_type='application/zip')
            # response['Content-Disposition'] = 'attachment; filename="segmented_images.zip"'
            return HttpResponse("Successful segmentation", status=200)
        except Exception as e:
            print(e)
            return HttpResponse("Error in segmentation: " + {e}, status=400)

    return HttpResponse("No images provided", status=400)