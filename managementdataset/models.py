# models.py
import uuid
import pickle
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
import cv2
import zlib  # Importar zlib para la compresión

def image_file_name(instance: models.Model, filename: str) -> str:
    return f"dataset/{uuid.uuid4()}.jpg"

if settings.DEBUG:
    class PostImageStorage(FileSystemStorage):
        pass
else:
    class PostImageStorage(S3Boto3Storage):
        location = "media"
        file_overwrite = True

class ImgDataset(models.Model):
    image = models.ImageField(
        verbose_name="Imagen",
        upload_to=image_file_name,
        storage=PostImageStorage(),
        null=True,
        blank=True,
    )
    keypoints = models.BinaryField(
        verbose_name="Image keypoints",
        null=True,
        blank=True,
    )
    descriptors = models.BinaryField(
        verbose_name="Image descriptors",
        null=True,
        blank=True,
    )

    def extract_and_save_features(self, image_path):
        """
        Extrae keypoints y descriptores de la imagen usando SIFT y los guarda en la base de datos.
        """
        print("Extrayendo keypoints y descriptores de la imagen...")

        # Leer la imagen directamente desde el archivo en memoria
        image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Extraer keypoints y descriptores con SIFT
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image_data, None)

        if keypoints and descriptors is not None:
            # Convertir keypoints a un formato serializable
            serializable_keypoints = []
            for kp in keypoints:
                keypoint_dict = {
                    'pt': kp.pt,          # Punto (x, y)
                    'size': kp.size,      # Diámetro del keypoint
                    'angle': kp.angle,    # Orientación
                    'response': kp.response,  # Respuesta del detector
                    'octave': kp.octave, # Octava
                    'class_id': kp.class_id  # ID de clase
                }
                serializable_keypoints.append(keypoint_dict)

            # Serializar y comprimir keypoints y descriptores
            self.keypoints = zlib.compress(pickle.dumps(serializable_keypoints))
            self.descriptors = zlib.compress(pickle.dumps(descriptors))
            self.save()

    def get_keypoints(self):
        """
        Descomprime y deserializa los keypoints.
        """
        if self.keypoints:
            return pickle.loads(zlib.decompress(self.keypoints))
        return None

    def get_descriptors(self):
        """
        Descomprime y deserializa los descriptores.
        """
        if self.descriptors:
            return pickle.loads(zlib.decompress(self.descriptors))
        return None
    
    def get_image(self):
        """
        Retorna la ruta de la imagen en el sistema de archivos.
        """
        return self.image.name