# exceptions.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Llama al manejador de excepciones por defecto para obtener la respuesta base
    response = exception_handler(exc, context)

    if response is not None:
        # Personaliza la respuesta de error
        if hasattr(exc, 'get_full_details'):
            # Si la excepción tiene el método get_full_details, úsalo
            custom_response = exc.get_full_details()
            response.data = custom_response
        elif "detail" in response.data:
            # Si no, usa el campo "detail" como mensaje
            response.data = {
                "message": response.data["detail"]
            }
        elif "non_field_errors" in response.data:
            # Maneja errores de validación no asociados a un campo específico
            response.data = {
                "message": response.data["non_field_errors"][0]
            }

    return response