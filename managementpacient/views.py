# views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImageSegmenter

@csrf_exempt
def segment_image(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        try:
            print('INITIALIZING SEGMENTATION')
            image_files = request.FILES.getlist("images")

            # Llamar al modelo para segmentar las imágenes
            segmenter = ImageSegmenter()
            segmented_images = segmenter.segment_images(image_files)

            print('SEGMENTATION FINISHED')
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