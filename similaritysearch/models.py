# models.py
import cv2
import numpy as np
import os
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

class ImageSimilarity:
    def __init__(self, original_image_path, compare_image_path):
        self.original_image_path = original_image_path
        self.compare_image_path = compare_image_path

    def are_images_identical(self):
        """
        Compara si dos imágenes son idénticas pixel a pixel.
        """
        original = cv2.imread(self.original_image_path)
        compare = cv2.imread(self.compare_image_path)

        if original.shape == compare.shape:
            difference = cv2.subtract(original, compare)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                return True
        return False

    def calculate_similarity(self):
        """
        Calcula la similitud entre dos imágenes utilizando SIFT y FLANN.
        Devuelve el porcentaje de similitud y la imagen con los matches.
        """
        original = cv2.imread(self.original_image_path, cv2.IMREAD_GRAYSCALE)
        compare = cv2.imread(self.compare_image_path, cv2.IMREAD_GRAYSCALE)

        # Inicializar SIFT
        sift = cv2.SIFT_create()

        # Detectar keypoints y descriptores
        kp1, desc1 = sift.detectAndCompute(original, None)
        kp2, desc2 = sift.detectAndCompute(compare, None)

        # Configurar FLANN
        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Encontrar matches
        matches = flann.knnMatch(desc1, desc2, k=2)

        # Filtrar buenos matches usando el ratio de Lowe
        good_points = []
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                good_points.append(m)

        # Calcular el porcentaje de similitud
        number_keypoints = min(len(kp1), len(kp2))
        similarity_percentage = (len(good_points) / number_keypoints * 100 if number_keypoints > 0 else 0)

        # Dibujar los matches
        result_image = cv2.drawMatches(
            cv2.imread(self.original_image_path), kp1,
            cv2.imread(self.compare_image_path), kp2,
            good_points, None
        )

        # Guardar la imagen resultante
        result_path = os.path.join(settings.MEDIA_ROOT, "feature_matching.jpg")
        cv2.imwrite(result_path, result_image)

        return similarity_percentage, result_path