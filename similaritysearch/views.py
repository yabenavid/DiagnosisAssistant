# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ImageSimilarity
import os

@csrf_exempt
def compare_images(request):
    if request.method == "POST" and request.FILES.get("original_image") and request.FILES.get("compare_image"):
        # Guardar las imágenes temporalmente
        original_image = request.FILES["original_image"]
        compare_image = request.FILES["compare_image"]

        original_path = default_storage.save("uploads/" + original_image.name, ContentFile(original_image.read()))
        compare_path = default_storage.save("uploads/" + compare_image.name, ContentFile(compare_image.read()))

        # Crear una instancia de ImageSimilarity
        similarity_checker = ImageSimilarity(
            original_image_path=default_storage.path(original_path),
            compare_image_path=default_storage.path(compare_path)
        )

        # Verificar si las imágenes son idénticas
        are_identical = similarity_checker.are_images_identical()

        # Calcular la similitud
        similarity_percentage, result_image_path = similarity_checker.calculate_similarity()

        # Devolver la respuesta JSON
        return JsonResponse({
            "are_identical": are_identical,
            "similarity_percentage": similarity_percentage,
            "result_image_url": default_storage.url(result_image_path)
        })

    return JsonResponse({"error": "No se proporcionaron imágenes válidas"}, status=400)