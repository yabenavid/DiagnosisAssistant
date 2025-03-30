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

    for image_name in image_names:
        try:
            # Descargar la imagen desde S3
            image_path = image_name
            with storage.open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()
                if image_bytes:
                    # Convertir los bytes de la imagen a un array de numpy
                    image_array = np.frombuffer(image_bytes, np.uint8)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    images.append({'image': image, 'name': image_name})
                else:
                    print(f"Error: La imagen {image_name} está vacía.")
        except Exception as e:
            print(f"Error al descargar la imagen {image_name} desde S3: {e}")
    return images

def get_all_images_from_s3():
    """
    Descarga todas las imágenes desde S3 y las retorna como objetos que pueden ser procesados con OpenCV.
    
    Retorna:
    list: Lista de imágenes como arrays de numpy.
    """
    images = []
    storage = ImgDataset().image.storage
    prefix = "dataset/"

    try:
        # Listar todos los archivos en el almacenamiento
        all_files = storage.listdir('dataset')  # [1] para obtener solo los archivos, no los directorios
        print("all_files:", all_files)

        for image_path in all_files[1]:
            print('dentro del for')
            print("image_path:", image_path)
            with storage.open(f"{prefix}{image_path}", 'rb') as image_file:
                print("image file:", image_file)
                image_bytes = image_file.read()
                if image_bytes:
                    # Convertir los bytes de la imagen a un array de numpy
                    image_array = np.frombuffer(image_bytes, np.uint8)
                    print("image array: ", image_array)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    images.append({'image': image, 'name': image_path})
                else:
                    print(f"Error: La imagen {image_path} está vacía.")
    except Exception as e:
        print(f"Error al descargar las imágenes desde S3: {e}")
    return images