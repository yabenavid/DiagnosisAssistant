# exceptions.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the base response
    response = exception_handler(exc, context)

    if response is not None:
        # Customize error response
        if hasattr(exc, 'get_full_details'):
            custom_response = exc.get_full_details()
            response.data = custom_response
        elif "detail" in response.data:
            response.data = {
                "message": response.data["detail"]
            }
        elif "non_field_errors" in response.data:
            response.data = {
                "message": response.data["non_field_errors"][0]
            }

    return response