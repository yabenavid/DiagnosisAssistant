import cv2
import numpy as np
from django.core.files.storage import default_storage
from managementdataset.models import ImgDataset

def get_images_from_s3(image_names, segment_type='SAM'):
    """
    Download images from S3 and return them as objects that can be processed with OpenCV.

    Parameters:
    image_names (list): List of image names to download from S3.
    segment_type (str): 'SAM', 'ScikitImage' or 'UNet'

    Returns:
    list: List of images as numpy arrays.
    """
    images = []
    storage = ImgDataset().image.storage
    prefix = f"dataset/{segment_type}/"

    for image_name in image_names:
        try:
            image_path = f"{prefix}{image_name}"
            with storage.open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()
                if image_bytes:
                    image_array = np.frombuffer(image_bytes, np.uint8)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    images.append({'image': image, 'name': image_name})
                else:
                    print(f"Error: La imagen {image_name} está vacía.")
        except Exception as e:
            print(f"Error al descargar la imagen {image_name} desde S3: {e}")
    return images

def get_all_images_from_s3(segment_type='SAM'):
    """
    Download all images from S3 and return them as objects that can be processed with OpenCV.

    segment_type (str): 'SAM', 'ScikitImage' or 'UNet'
    Returns:
    list: List of images as numpy arrays.
    """
    images = []
    storage = ImgDataset().image.storage
    prefix = f"dataset/{segment_type}/"

    try:
        all_files = storage.listdir(prefix)
        for image_path in all_files[1]:
            with storage.open(f"{prefix}{image_path}", 'rb') as image_file:
                print(f"Downloading image: {image_path}")
                image_bytes = image_file.read()
                if image_bytes:
                    image_array = np.frombuffer(image_bytes, np.uint8)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    images.append({'image': image, 'name': image_path})
                else:
                    print(f"Error: La imagen {image_path} está vacía.")
        print(f"Se obtuvieron {len(images)} imágenes del dataset {segment_type}.")
    except Exception as e:
        print(f"Error al descargar las imágenes desde S3: {e}")
    return images