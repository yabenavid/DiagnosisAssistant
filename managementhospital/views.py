from rest_framework import viewsets, status
from .models import Hospital
from .serializer import HospitalSerializer
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminUser

# Create your views here.
@authentication_classes([JWTAuthentication])  # Requiere autenticación JWT
@permission_classes([IsAdminUser]) 
class HospitalView(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response(
                    {"message": "Hospital creado con éxito"},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"message": f"Error al crear el hospital: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"message": "Datos inválidos para crear el hospital"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            try:
                self.perform_update(serializer)
                return Response(
                    {"message": "Hospital actualizado con éxito"},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"message": f"Error al actualizar el hospital: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"message": "Datos inválidos para actualizar el hospital"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {"message": "Hospital eliminado con éxito"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Error al eliminar el hospital: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'hospitals': serializer.data
        })