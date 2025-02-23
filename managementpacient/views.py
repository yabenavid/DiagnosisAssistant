# views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from segmentation.models import SamImageSegmenter
from similaritysearch.models import ImageSimilarity

@csrf_exempt
def segment_image(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        try:
            print('INITIALIZING SEGMENTATION')
            image_files = request.FILES.getlist("images")
            segment_model = request.POST.get("segment_model", None)

            if (segment_model == 1):
                segmenter = SamImageSegmenter()
                segmented_images = segmenter.segment_images(image_files)
            elif (segment_model == 2):
                segmenter = SamImageSegmenter()
                segmented_images = segmenter.segment_images(image_files, image_path = 'uploads/imagen.jpg')

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