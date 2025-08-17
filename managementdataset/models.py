# models.py
import uuid
import pickle
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
import cv2
import zlib

def image_file_name(instance: models.Model, filename: str) -> str:
    # Temp attribute to decide the final route
    segment_type = getattr(instance, 'segment_type', 'SAM')  # Default SAM
    return f"dataset/{segment_type}/{uuid.uuid4()}.jpg"

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
        Extract keypoints and descriptors from the image and save them to the database.
        """
        print("Extracting keypoints and descriptors from the image...")

        # Read the image directly from the file in memory
        image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Extract keypoints and descriptors with SIFT
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image_data, None)

        if keypoints and descriptors is not None:
            # Convert keypoints to a serializable format
            serializable_keypoints = []
            for kp in keypoints:
                keypoint_dict = {
                    'pt': kp.pt,          # Point (x, y)
                    'size': kp.size,      # Diameter of the keypoint
                    'angle': kp.angle,    # Orientation
                    'response': kp.response,
                    'octave': kp.octave,
                    'class_id': kp.class_id
                }
                serializable_keypoints.append(keypoint_dict)

            # Serialize and compress keypoints and descriptors
            self.keypoints = zlib.compress(pickle.dumps(serializable_keypoints))
            self.descriptors = zlib.compress(pickle.dumps(descriptors))
            self.save()

    def get_keypoints(self):
        """
        Decompress and deserialize the keypoints.
        """
        if self.keypoints:
            return pickle.loads(zlib.decompress(self.keypoints))
        return None

    def get_descriptors(self):
        """
        Decompress and deserialize the descriptors.
        """
        if self.descriptors:
            return pickle.loads(zlib.decompress(self.descriptors))
        return None
    
    def get_image(self):
        """
        Returns the image path in the file system.
        """
        return self.image.name