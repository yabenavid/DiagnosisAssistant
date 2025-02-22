from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django.db import IntegrityError
from .serializer import DoctorSerializer
from .models import Doctor
from collections import defaultdict
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminUser

# Create your views here.
@authentication_classes([JWTAuthentication])  # JWT Authentication
@permission_classes([IsAdminUser])        # Only admin users can access
class DoctorView(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response(
                    {"message": "Doctor creado con éxito"},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"message": f"Error al crear el doctor: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        error_messages = " / ".join(
            [f"{key}: {', '.join(value)}" for key, value in serializer.errors.items()]
        ) if serializer.errors else _("Datos inválidos para crear el doctor")
        return Response(
            {"message": error_messages},
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
                    {"message": "Doctor actualizado con éxito"},
                    status=status.HTTP_200_OK
                )
            except serializers.ValidationError as e:
                if 'hospital' in e.detail:
                    return Response(
                        {"message": "El hospital especificado no existe."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"message": f"Error al actualizar el doctor: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {"message": f"Error al actualizar el doctor: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        error_messages = " / ".join(
            [f"{key}: {', '.join(value)}" for key, value in serializer.errors.items()]
        ) if serializer.errors else ("Datos inválidos para actualizar el doctor")
        return Response(
            {"message": error_messages},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {"message": "Doctor y credencial asociada eliminados correctamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Error al eliminar: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'doctors': serializer.data
        })