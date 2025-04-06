# views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from segmentation.models import SamImageSegmenter
from segmentation.apps import segmenter_instance
from similaritysearch.models import ImageSimilarity, ImageSimilarityResNet
from vectorization.models import ImageResizer
from .pdf_service import PDFGenerator
import json
import os
from django.conf import settings
import uuid
from django.http import FileResponse

@csrf_exempt
def segment_image(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        try:
            image_files = request.FILES.getlist("images")
            segment_model = request.POST.get("segment_model", None)

            if segment_model is None:
                return HttpResponse("segment_model parameter is missing", status=400)

            print('INITIALIZING VECTORIZATION')
            image_resizer = ImageResizer()
            resized_images, resized_images_base64 = image_resizer.procesar_imagenes(image_files)
            print('VECTORIZATION FINISHED')

            print('INITIALIZING SEGMENTATION')
            if segment_model == '1':
                # print('Cargando modelo de sam')
                # segmenter = SamImageSegmenter()
                # print('Segmentando')
                # segmented_images = segmenter.segment_images(resized_images)
                segmented_images = segmenter_instance.segment_images(resized_images)
            else:
                return HttpResponse("Invalid segmentation model param", status=400)
            print('SEGMENTATION FINISHED')

            print('INITIALIZING SIMILARITY')
            similarity_checker_resnet = ImageSimilarityResNet()
            result = similarity_checker_resnet.calculate_similarity(segmented_images)
            print('SIMILARITY FINISHED')

            # Convertir el resultado a JSON si es necesario
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    pass

            print('GENERATING PDF')
            pdf_content = PDFGenerator.generate_similarity_report(result)
            
            print('SAVING PDF LOCALLY')
            # Guardar el PDF temporalmente (opcional, dependiendo de tus necesidades)
            pdf_filename = f"report_{uuid.uuid4().hex}.pdf"
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', pdf_filename)
            
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_content)
            
            print('PREPARING RESPONSE')

            frontend_results = [
                {
                    'average_similarity_percentage': r['average_similarity_percentage'],
                    'diagnosis_message': r['diagnosis_message'],
                    'pacient_image': resized_images_base64[i],  # De vectorization
                    'segmented_pacient_image': r['pacient_image']  # De similarity
                }
                for i, r in enumerate(result)
            ]
            return JsonResponse({
                'results': frontend_results,
                'pdf_url': f"/media/reports/{pdf_filename}"
            }, status=200)
            
        except Exception as e:
            print(e)
            return HttpResponse(f"Error in segmentation: {str(e)}", status=400)

    return HttpResponse("No images provided", status=400)

def download_report(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("File not found", status=404)