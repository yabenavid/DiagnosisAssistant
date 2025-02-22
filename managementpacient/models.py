# views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from segmentation.models import ImageSegmenter

@csrf_exempt
def segment_image(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        image_files = request.FILES.getlist("images")

        segmenter = ImageSegmenter()
        segmented_images = segmenter.segment_images(image_files)

        # Crear un archivo ZIP con las imágenes segmentadas
        zip_buffer = segmenter.create_zip(segmented_images)

        # Devolver el archivo ZIP como respuesta HTTP
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="segmented_images.zip"'
        return response

    return HttpResponse("No images provided", status=400)