# views.py
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.decorators import api_view, authentication_classes
from segmentation.models import SamImageSegmenter
from segmentation.apps import segmenter_instance
from similaritysearch.models import ImageSimilarity, ImageSimilarityResNet
from vectorization.models import ImageResizer
from .pdf_service import PDFGenerator
import json

from .models import History, HistoryStorage
from managementdoctor.models import Doctor
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.files.base import ContentFile
from datetime import datetime

from rest_framework import generics
from .serializer import HistorySerializer
from rest_framework.permissions import IsAuthenticated
from urllib.parse import quote

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def evaluate_images(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        try:
            if not request.user.is_authenticated:
                return HttpResponse("Authentication required", status=401)

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
                # segmenter_instance = get_segmenter()
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
            pdf_content = PDFGenerator.generate_similarity_report(result, resized_images_base64)
            
            print('SAVING PDF IN S3')
            storage = HistoryStorage()
            current_date = datetime.now().strftime("%Y%m%d")
            pdf_filename = f"resumen-{current_date}.pdf"

            user = request.user
            doctor = Doctor.objects.get(user=user)
            hospital = doctor.belong_set.first().hospital

            # Estructura en S3: history/hospital_<id>/<filename>
            s3_key = f"hospital_{hospital.id}/{pdf_filename}"
            storage.save(s3_key, ContentFile(pdf_content))
            
            # 2. Crear registro en DB
            History.objects.create(
                hospital=hospital,
                s3_pdf_key=s3_key
            )

            # 3. URL temporal para descarga
            pdf_url = storage.url(s3_key)
            
            print('PREPARING RESPONSE')

            frontend_results = [
                {
                    'average_similarity_percentage': r['average_similarity_percentage'],
                    'diagnosis_message': r['diagnosis_message'],
                    'pacient_image': resized_images_base64[i],
                    'segmented_pacient_image': r['pacient_image']
                }
                for i, r in enumerate(result)
            ]
            return JsonResponse({
                'results': frontend_results,
                'pdf_url': pdf_url
            }, status=200)
            
        except Exception as e:
            print(e)
            return HttpResponse(f"Error in segmentation: {str(e)}", status=400)

    return HttpResponse("No images provided", status=400)

def download_report(request, report_id):
    try:
        report = History.objects.get(id=report_id)
        storage = HistoryStorage()
        
        if storage.exists(report.s3_pdf_key):
            file = storage.open(report.s3_pdf_key)
            response = FileResponse(file)
            filename = report.s3_pdf_key.split('/')[-1]
            
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
            response['Content-Length'] = file.size
            return response
            
        return HttpResponse("File not found", status=404)
    except History.DoesNotExist:
        return HttpResponse("Report not found", status=404)

class HistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            user = self.request.user
            doctor = Doctor.objects.get(user=user)
            belong = doctor.belong_set.first()
            
            if not belong or not belong.hospital:
                return History.objects.none()
                
            return History.objects.filter(hospital=belong.hospital).order_by('id')
            
        except Doctor.DoesNotExist:
            return History.objects.none()