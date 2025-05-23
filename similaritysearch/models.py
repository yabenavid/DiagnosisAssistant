# models.py
from PIL import Image
import cv2
import numpy as np
import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from django.conf import settings
from django.core.files.storage import default_storage
from managementdataset.models import ImgDataset
from managementdataset.utils import get_images_from_s3, get_all_images_from_s3
from .utils import calculate_average, image_to_base64, get_diagnosis_message

class ImageSimilarity:
    def __init__(self):
        pass

    def calculate_similarity(self, pacient_images, segment_type):
        """
        Calcula la similitud entre las imágenes proporcionadas y las imágenes almacenadas en la base de datos.
        Devuelve un array con los porcentajes de similitud y las rutas de las imágenes con los matches.
        """
        results = []
        matches_data = []

        # Obtener keypoints y descriptors de la tabla ImgDataset
        data_datasets = ImgDataset.objects.all()

        for pacient_image in pacient_images:
            # Leer la imagen del paciente
            print(">>Reading pacient image")
            pacient_image_data = cv2.imdecode(
                np.frombuffer(pacient_image.read(), np.uint8), cv2.IMREAD_GRAYSCALE
            )

            # Inicializar SIFT
            print(">>Initializing SIFT")
            sift = cv2.SIFT_create()

            # Detectar keypoints y descriptores en la imagen del paciente
            print(">>Detecting keypoints and descriptors")
            kp1, desc1 = sift.detectAndCompute(pacient_image_data, None)


            for data_dataset in data_datasets:
                # Descomprimir y deserializar los keypoints y descriptors almacenados
                print(">>Reading keypoints and descriptors")
                keypoints = data_dataset.get_keypoints()
                descriptors = data_dataset.get_descriptors()

                # Convertir keypoints a objetos cv2.KeyPoint
                print(">>Converting keypoints")

                kp2 = [
                    cv2.KeyPoint(
                        x=kp["pt"][0],
                        y=kp["pt"][1],
                        size=kp["size"],
                        angle=kp["angle"],
                        response=kp["response"],
                        octave=kp["octave"],
                        class_id=kp["class_id"],
                    )
                    for kp in keypoints
                ]

                # Configurar FLANN
                print(">>Configuring FLANN")
                index_params = dict(algorithm=0, trees=5)
                search_params = dict()
                flann = cv2.FlannBasedMatcher(index_params, search_params)

                # Encontrar matches
                print(">>Finding matches")
                matches = flann.knnMatch(desc1, descriptors, k=2)

                # Filtrar buenos matches usando el ratio de Lowe
                print(">>Filtering good matches")
                good_points = []
                for m, n in matches:
                    if m.distance < 0.6 * n.distance:
                        good_points.append(m)

                # Calcular el porcentaje de similitud
                print(">>Calculating similarity")
                number_keypoints = min(len(kp1), len(kp2))
                similarity_percentage = (
                    len(good_points) / number_keypoints * 100
                    if number_keypoints > 0
                    else 0
                )

                # TODO: Tener en cuenta el porcentaje segun la similitud que tengan las imagenes
                print(data_dataset.get_image())
                print(similarity_percentage)
                if similarity_percentage > 90:
                    print('>>Match: ', data_dataset.get_image())
                    matches_data.append(
                        {
                            "pacient_image": pacient_image_data,
                            "dataset_image_path": data_dataset.get_image(),
                            "kp1": kp1,
                            "kp2": kp2,
                            "good_points": good_points,
                            "similarity_percentage": similarity_percentage,
                        }
                    )
                
        print("Matches found:", len(matches_data))
        # Obtener una lista de todos los 'dataset_image' contenidos en 'matches_data'
        print(">>Getting dataset images")
        dataset_images = [match["dataset_image_path"] for match in matches_data]

        # Obtener las imágenes desde S3
        print(">>Getting images from S3")
        dataset_images_from_s3 = get_images_from_s3(dataset_images, segment_type)

        for dataset_image in dataset_images_from_s3:
            for match in matches_data:
                if dataset_image["name"] == match["dataset_image_path"]:
                    print(">>Drawing matches")
                    result_image = cv2.drawMatches(
                        match["pacient_image"],
                        match["kp1"],
                        dataset_image["image"],
                        match["kp2"],
                        match["good_points"],
                        None,
                    )

                    # Guardar la imagen resultante
                    print(">>Saving result image")
                    print('dataset_image_path:', match['dataset_image_path'])
                    result_filename = os.path.basename(match['dataset_image_path'])
                    result_path = os.path.join(
                        settings.MEDIA_ROOT,
                        f"feature_matching_{result_filename}",
                    )
                    print(">>Result path:", result_path)
                    cv2.imwrite(result_path, result_image)
    
                    # Almacenar el resultado
                    print(">>Storing result")
                    results.append(
                        {
                            "similarity_percentage": match["similarity_percentage"],
                            "result_path": result_path,
                        }
                    )

        return results

class ImageSimilarityResNet:
    def __init__(self):
        # Cargar el modelo preentrenado de ResNet
        self.model = models.resnet18(weights='IMAGENET1K_V1')
        self.model.eval()
        
        # Definir las transformaciones para las imágenes
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def calculate_similarity(self, pacient_images, segment_type):
        """
        Calcula la similitud entre las imágenes proporcionadas y las imágenes almacenadas en la base de datos.
        Utiliza ResNet para calcular las similitudes.
        """
        results = []

        # Obtener las imágenes de la base de datos
        print(">>Getting images from S3")
        dataset_images_from_s3 = get_all_images_from_s3(segment_type)

        for pacient_image in pacient_images:

            percentage_similarity_by_pacient = []

            # Leer la imagen del paciente
            print(">>Reading pacient image")
            pacient_image_data = cv2.imdecode(
                np.frombuffer(pacient_image.read(), np.uint8), cv2.IMREAD_COLOR
            )

            # Convertir la imagen de NumPy a PIL
            pacient_image_pil = Image.fromarray(cv2.cvtColor(pacient_image_data, cv2.COLOR_BGR2RGB))

            # Transformar la imagen segmentada
            print(">>Transforming image")
            pacient_image_tensor = self.transform(pacient_image_pil).unsqueeze(0)

            # Extraer características con ResNet
            print(">>Extracting features")
            with torch.no_grad():
                pacient_features = self.model(pacient_image_tensor).numpy()

            for data_dataset in dataset_images_from_s3:
                # Leer la imagen de la base de datos desde el diccionario
                print(">>Reading dataset image")
                dataset_image = data_dataset['image']

                # Convertir la imagen de NumPy a PIL
                dataset_image_pil = Image.fromarray(cv2.cvtColor(dataset_image, cv2.COLOR_BGR2RGB))

                # Transformar la imagen segmentada
                print(">>Transforming image")
                dataset_image_tensor = self.transform(dataset_image_pil).unsqueeze(0)

                # Extraer características con ResNet
                print(">>Extracting features")
                with torch.no_grad():
                    dataset_features = self.model(dataset_image_tensor).numpy()

                # Calcular la similitud entre las características
                print(">>Calculating similarity")
                similarity_percentage = self.calculate_cosine_similarity(pacient_features, dataset_features)

                percentage_similarity_by_pacient.append(similarity_percentage)

            average_pacient_similarity = calculate_average(percentage_similarity_by_pacient)
            _, img_bytes = cv2.imencode('.png', pacient_image_data)
            img_bytes = img_bytes.tobytes()
            pacient_image_base64 = image_to_base64(pacient_image_data)
            diagnosis_message = get_diagnosis_message(average_pacient_similarity/100)
            print(">>Diagnosis message: ", diagnosis_message)
            
            results.append(
                {
                    "average_similarity_percentage": average_pacient_similarity,
                    "diagnosis_message": diagnosis_message,
                    "pacient_image": pacient_image_base64,
                    "pacient_image_bytes": img_bytes
                }
            )

        return results

    def calculate_cosine_similarity(self, features1, features2):
        """
        Calcula la similitud coseno entre dos vectores de características.
        """
        print(">>Calculating cosine similarity")
        dot_product = np.dot(features1, features2.T)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        similarity = dot_product / (norm1 * norm2)
        print(similarity * 100)
        return similarity * 100

class ImageSimilarityTest:
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
        print(">>Initializing SIFT")
        sift = cv2.SIFT_create()

        # Detectar keypoints y descriptores
        print(">>Detecting keypoints and descriptors")
        kp1, desc1 = sift.detectAndCompute(original, None)
        kp2, desc2 = sift.detectAndCompute(compare, None)

        # Configurar FLANN
        print(">>Configuring FLANN")
        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Encontrar matches
        print(">>Finding matches")
        matches = flann.knnMatch(desc1, desc2, k=2)

        # Filtrar buenos matches usando el ratio de Lowe
        print(">>Filtering good matches")
        good_points = []
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                good_points.append(m)

        # Calcular el porcentaje de similitud
        print(">>Calculating similarity")
        number_keypoints = min(len(kp1), len(kp2))
        similarity_percentage = (len(good_points) / number_keypoints * 100 if number_keypoints > 0 else 0)

        # Dibujar los matches
        print(">>Drawing matches")
        result_image = cv2.drawMatches(
            cv2.imread(self.original_image_path), kp1,
            cv2.imread(self.compare_image_path), kp2,
            good_points, None
        )

        # Guardar la imagen resultante
        print(">>Saving result image")
        result_path = os.path.join(settings.MEDIA_ROOT, "feature_matching.jpg")
        cv2.imwrite(result_path, result_image)

        return similarity_percentage, result_path