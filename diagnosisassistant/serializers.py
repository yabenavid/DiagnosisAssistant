# serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # Generate JWT token

        # Add custom fields in token
        token['username'] = user.username
        token['email'] = user.email
        token['is_admin'] = user.is_staff

        return token

    def validate(self, attrs):
        # Intenta validar las credenciales
        try:
            data = super().validate(attrs)
        except Exception as e:
            raise CustomAuthenticationFailed()

        data = super().validate(attrs)  # Validate credentials and generate tokens

        # Additional fields in response
        data['is_admin'] = self.user.is_staff
        data['message'] = ''

        return data
    
class CustomAuthenticationFailed(APIException):
    status_code = 401
    default_detail = "Credenciales inválidas. Por favor, verifica tu email y contraseña."
    default_code = "authentication_failed"

    def get_full_details(self):
        # Personaliza la estructura de la respuesta
        return {
            "message": self.default_detail,  # Usa el campo "message" en lugar de "detail"
            "code": self.default_code,       # Agrega un código de error (opcional)
        }