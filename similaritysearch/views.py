# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ImageSimilarityTest

@csrf_exempt
def compare_images(request):
    if request.method == "POST" and request.FILES.get("original_image") and request.FILES.get("compare_image"):
        original_image = request.FILES["original_image"]
        compare_image = request.FILES["compare_image"]

        # Save the images temporarily
        original_path = default_storage.save("uploads/" + original_image.name, ContentFile(original_image.read()))
        compare_path = default_storage.save("uploads/" + compare_image.name, ContentFile(compare_image.read()))

        # Create an instance of ImageSimilarity
        similarity_checker = ImageSimilarityTest(
            original_image_path=default_storage.path(original_path),
            compare_image_path=default_storage.path(compare_path)
        )

        # Check if the images are identical
        are_identical = similarity_checker.are_images_identical()

        # Calculate the similarity
        similarity_percentage, result_image_path = similarity_checker.calculate_similarity()

        # Return the JSON response
        return JsonResponse({
            "are_identical": are_identical,
            "similarity_percentage": similarity_percentage,
            "result_image_url": default_storage.url(result_image_path)
        })

    return JsonResponse({"error": "No se proporcionaron imágenes válidas"}, status=400)