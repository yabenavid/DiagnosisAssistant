import cv2
import numpy as np
from django.core.files.storage import default_storage
from managementdataset.models import ImgDataset

def get_images_from_s3(image_names):
    """
    Descarga imágenes desde S3 y las retorna como objetos que pueden ser procesados con OpenCV.
    
    Parámetros:
    image_names (list): Lista de nombres de imágenes a descargar desde S3.
    
    Retorna:
    list: Lista de imágenes como arrays de numpy.
    """
    images = []
    storage = ImgDataset().image.storage
    prefix = "media/"

    for image_name in image_names:
        try:
            # Descargar la imagen desde S3
            # image_path = f"{prefix}{image_name}"
            image_path = image_name
            with storage.open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()
                # Convertir los bytes de la imagen a un array de numpy
                image_array = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                images.append({'image': image, 'name': image_name})
        except Exception as e:
            print(f"Error al descargar la imagen {image_name} desde S3: {e}")
    return images