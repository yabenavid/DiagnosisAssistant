from django.http import JsonResponse
from .firebase_config import bucket
from PIL import Image
import os

OUTPUT_SIZE = (300, 300)  # Tamaño para redimensionar las imágenes

def upload_to_storage(local_file_path, destination_blob_name):
    # Referencia al bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    print(f"Archivo subido a {destination_blob_name}")

def download_from_storage(destination_file_path, source_blob_name):
    # Referencia al archivo en el bucket
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_path)
    print(f"Archivo descargado de {source_blob_name} a {destination_file_path}")

def get_file_url(blob_name):
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(expiration=3600)  # URL válida por 1 hora
    print(f"URL generada: {url}")
    return url

def list_files_in_storage():
    # Obtiene la lista de archivos almacenados en el bucket y retorna sus nombres.
    blobs = bucket.list_blobs()  # Lista todos los blobs en el bucket
    file_names = [blob.name for blob in blobs]  # Obtiene los nombres de los archivos
    return file_names

def get_images():
    blobs = bucket.list_blobs()
    image_urls = [
        blob.generate_signed_url(expiration=3600)  # URL válida por 1 hora
        for blob in blobs
    ]
    return image_urls

def save_image_to_firebase(image):
    """
    Redimensiona una imagen, la convierte a PNG y la sube a Firebase Storage.
    
    Args:
        image (InMemoryUploadedFile): La imagen recibida desde el frontend.
    
    Returns:
        str: URL firmada de la imagen subida.
    """
    try:
        # Abrir la imagen recibida
        img = Image.open(image)

        # Redimensionar la imagen
        img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)

        # Obtener el nombre base del archivo sin la extensión original
        base_name = os.path.splitext(image.name)[0]
        new_image_name = f"{base_name}.png"  # Cambiar la extensión a .png

        # Guardar la imagen temporalmente en el sistema de archivos
        temp_path = f"temp_{new_image_name}"
        img.save(temp_path, format="PNG")

        # Subir la imagen redimensionada a Firebase Storage
        blob = bucket.blob(f"imagenes_redimensionadas/{new_image_name}")
        blob.upload_from_filename(temp_path)

        """ solo generar url privada """
        # Generar una URL firmada para acceder a la imagen
        #image_url = blob.generate_signed_url(expiration=86400)  # URL válida por 24 horas

        """ generar url publica """
        # Hacer que el archivo sea público
        blob.make_public()

        # Generar una URL firmada para acceder a la imagen
        image_url = blob.public_url  # URL publica de imagen subida

        # Eliminar el archivo temporal
        os.remove(temp_path)

        return image_url

    except Exception as e:
        raise Exception(f"Error al procesar y guardar la imagen: {str(e)}")

def save_images_to_firebase(images):
    """
    Procesa y guarda múltiples imágenes en Firebase Storage.
    
    Args:
        images (list): Lista de objetos InMemoryUploadedFile.
    
    Returns:
        list: Lista de URLs firmadas de las imágenes subidas.
    """
    urls = []
    for image in images:
        try:
            url = save_image_to_firebase(image)
            urls.append(url)
        except Exception as e:
            raise Exception(f"Error al procesar la imagen {image.name}: {str(e)}")
    return urls
