from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib3 import request
from .models import ImgDataset
from .serializer import MultipleImageUploadSerializer, ImageDatasetSerializer, ZipImageUploadSerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from django.conf import settings
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminUser

# Create your views here.

def index(request):
    return HttpResponse('<h1>Index Page</h1>')

def hello(request, username):
    return HttpResponse('<h1>Hello %s!</h1>' % username)

def about(request):
    a = 1
    return HttpResponse('<h1>About</h1>')

@authentication_classes([JWTAuthentication])  # JWT Authentication
@permission_classes([IsAdminUser])        # Only admin users can access
class DatasetView(viewsets.ModelViewSet):
    queryset = ImgDataset.objects.all()
    serializer_class = ImageDatasetSerializer

    def create(self, request, *args, **kwargs):
        serializer = ZipImageUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                instances = serializer.save()
                return Response({"message": "Imágenes guardadas con éxito"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Errores del serializer:", serializer.errors)
            return Response(
                {"message": "El archivo enviado no es válido. Asegúrate de subir un archivo ZIP que contenga imágenes."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtiene el objeto a eliminar
        # Elimina el archivo de S3 antes de eliminar el registro
        if instance.image:
            instance.image.delete(save=False)  # Borra la imagen en S3
        instance.delete()  # Elimina el registro de la base de datos
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Count images
    @action(detail=False, methods=['GET'], url_path='count')

    def count(self, request, *args, **kwargs):
        try:
            # Si estamos en modo DEBUG, contamos las imágenes en la base de datos local
            if settings.DEBUG:
                count = ImgDataset.objects.count()
            else:
                # Si no estamos en modo DEBUG, contamos las imágenes en S3
                storage = ImgDataset().image.storage
                prefix = "media/dataset/"

                # Listar todos los objetos en el bucket con el prefijo especificado
                s3_objects = storage.bucket.objects.filter(Prefix=prefix)
                count = sum(1 for _ in s3_objects)

            return Response(count, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                0,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
