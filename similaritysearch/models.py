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
from .utils import calculate_average, image_to_base64, get_diagnosis_message, calculate_statistics
from scipy import linalg
import torch.nn.functional as F
from torchvision.models import inception_v3
from torchvision.models import Inception_V3_Weights
import csv
import matplotlib.pyplot as plt

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
        self.model = models.resnet18(weights='IMAGENET1K_V1')
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def extract_green_mask(self, image_bgr):
        """
        Extracts a binary mask from the (segmented) green area in a BGR image.
        It also displays the original image and the resulting mask using matplotlib.
        """
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        binary_mask = (mask > 0).astype(np.uint8)

        return binary_mask

    def calculate_similarity(self, pacient_images, segment_type, method="resnet"):
        results = []
        dataset_images_from_s3 = get_all_images_from_s3(segment_type)

        if method == "fid":
            pacient_imgs_list = [cv2.imdecode(np.frombuffer(p.read(), np.uint8), cv2.IMREAD_COLOR) for p in pacient_images]
            dataset_imgs_list = [d['image'] for d in dataset_images_from_s3]
            fid_value = self.calculate_fid_score(pacient_imgs_list, dataset_imgs_list)
            results.append({
                "fid_score": fid_value,
                "diagnosis_message": f"FID: {fid_value:.2f} (menor es mejor)",
                "pacient_image": None,
                "pacient_image_bytes": None
            })
            return results

        for pacient_image in pacient_images:
            percentage_similarity_by_pacient = []

            pacient_image_data = cv2.imdecode(
                np.frombuffer(pacient_image.read(), np.uint8), cv2.IMREAD_COLOR
            )

            if method == "resnet":
                pacient_image_pil = Image.fromarray(cv2.cvtColor(pacient_image_data, cv2.COLOR_BGR2RGB))
                pacient_image_tensor = self.transform(pacient_image_pil).unsqueeze(0)
                with torch.no_grad():
                    pacient_features = self.model(pacient_image_tensor).numpy()

            elif method in ["dice", "iou"]:
                pacient_binary = self.extract_green_mask(pacient_image_data)
            
            elif method == "psnr":
                pacient_image_clean = pacient_image_data

            else:
                raise ValueError("Método de comparación no soportado: elija 'resnet', 'dice' o 'iou'.")

            for data_dataset in dataset_images_from_s3:
                dataset_image = data_dataset['image']

                if method == "resnet":
                    dataset_image_pil = Image.fromarray(cv2.cvtColor(dataset_image, cv2.COLOR_BGR2RGB))
                    dataset_image_tensor = self.transform(dataset_image_pil).unsqueeze(0)
                    with torch.no_grad():
                        dataset_features = self.model(dataset_image_tensor).numpy()
                    similarity_percentage = self.calculate_cosine_similarity(pacient_features, dataset_features)

                elif method == "dice":
                    dataset_binary = self.extract_green_mask(dataset_image)
                    similarity_percentage = self.dice_coefficient_images(pacient_binary, dataset_binary) * 100

                elif method == "iou":
                    dataset_binary = self.extract_green_mask(dataset_image)
                    similarity_percentage = self.iou_coefficient_images(pacient_binary, dataset_binary) * 100

                elif method == "psnr":
                    similarity_percentage = self.calculate_psnr(pacient_image_clean, dataset_image)


                print("Similarity percentage:", similarity_percentage)
                percentage_similarity_by_pacient.append(similarity_percentage)

            average_pacient_similarity = calculate_average(percentage_similarity_by_pacient)
            _, img_bytes = cv2.imencode('.png', pacient_image_data)
            img_bytes = img_bytes.tobytes()
            pacient_image_base64 = image_to_base64(pacient_image_data)
            diagnosis_message = get_diagnosis_message(average_pacient_similarity / 100)

            results.append({
                "average_similarity_percentage": average_pacient_similarity,
                "diagnosis_message": diagnosis_message,
                "pacient_image": pacient_image_base64,
                "pacient_image_bytes": img_bytes
            })

        return results

    def calculate_cosine_similarity(self, features1, features2):
        """
        Calculates the cosine similarity between two feature vectors.
        """
        features1 = features1.flatten()
        features2 = features2.flatten()
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        similarity = dot_product / (norm1 * norm2)
        return float(similarity * 100)  # Ensures it returns a float

    def dice_coefficient_images(self, img1, img2):
        """
        Calculates the Dice coefficient between two binary images.
        """
        if img1.shape != img2.shape:
            raise ValueError("Las imágenes deben tener el mismo tamaño.")

        img1 = img1.astype(bool)
        img2 = img2.astype(bool)

        intersection = np.logical_and(img1, img2).sum()
        total = img1.sum() + img2.sum()

        if total == 0:
            return 1.0

        return 2.0 * intersection / total
    
    def iou_coefficient_images(self, img1, img2):
        """
        Calculates the IoU (Intersection over Union) coefficient between two binary images.
        """
        if img1.shape != img2.shape:
            raise ValueError("Las imágenes deben tener el mismo tamaño.")

        img1 = img1.astype(bool)
        img2 = img2.astype(bool)
        
        intersection = np.logical_and(img1, img2).sum()
        union = np.logical_or(img1, img2).sum()

        if union == 0:
            return 1.0

        return intersection / union

    def calculate_fid_score(self, imgs1, imgs2, device='cpu'):
        """
        Calculates the FID between two sets of images (PIL or numpy tensors).
        """
        model = inception_v3(weights=Inception_V3_Weights.DEFAULT, transform_input=False).to(device)
        model.fc = torch.nn.Identity()
        model.eval()

        def get_activations(imgs):
            processed = []
            for img in imgs:
                if isinstance(img, np.ndarray):
                    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                img = transforms.Resize((299, 299))(img)
                img = transforms.ToTensor()(img).unsqueeze(0)
                img = transforms.Normalize([0.5]*3, [0.5]*3)(img)
                processed.append(img.to(device))  # <-- Moves each tensor to the specified device
            batch = torch.cat(processed)
            with torch.no_grad():
                activations = model(batch).cpu().numpy()
            return activations

        act1 = get_activations(imgs1)
        act2 = get_activations(imgs2)

        mu1, sigma1 = act1.mean(axis=0), np.cov(act1, rowvar=False)
        mu2, sigma2 = act2.mean(axis=0), np.cov(act2, rowvar=False)

        diff = mu1 - mu2
        covmean, _ = linalg.sqrtm(sigma1 @ sigma2, disp=False)

        if np.iscomplexobj(covmean):
            covmean = covmean.real

        fid = diff.dot(diff) + np.trace(sigma1 + sigma2 - 2 * covmean)
        return fid

    def calculate_psnr(self, img1, img2): 
        """
        Calculates the PSNR (Peak Signal to Noise Ratio) metric between two color images.
        """
        if img1.shape != img2.shape:
            raise ValueError("Las imágenes deben tener el mismo tamaño.")

        mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
        if mse == 0:
            return float('inf')
        max_pixel = 255.0
        psnr = 10 * np.log10((max_pixel ** 2) / mse)
        return psnr

    def run_all_metrics_and_export_csv(self, pacient_images, segment_type, output_path="resultados_metricas.csv", dataset_folder=None):
        """
        Runs all available metrics on the patient's images and saves the results to a CSV file.
        Uses images from a local folder if dataset_folder is defined.
        """
        csv_rows = []

        # Convert images to a reusable format
        pacient_imgs_list = []
        pacient_filenames = []
        for p in pacient_images:
            img = cv2.imdecode(np.frombuffer(p.read(), np.uint8), cv2.IMREAD_COLOR)
            pacient_imgs_list.append(img)
            pacient_filenames.append(getattr(p, 'name', 'desconocida'))

        # Get dataset from local folder or S3
        print(">>Getting dataset images")
        if dataset_folder:
            dataset_imgs_list = [d['image'] for d in self.get_images_from_local_folder(dataset_folder)]
        else:
            dataset_imgs_list = [d['image'] for d in get_all_images_from_s3(segment_type)]

        for idx, pacient_img in enumerate(pacient_imgs_list):
            print(">>Image", idx + 1)
            filename = pacient_filenames[idx]

            # ---------- Metric: Cosine ----------
            print(">>Calculating cosine similarity")
            try:
                pacient_tensor = self.transform(Image.fromarray(cv2.cvtColor(pacient_img, cv2.COLOR_BGR2RGB))).unsqueeze(0)
                with torch.no_grad():
                    pacient_features = self.model(pacient_tensor).numpy()
                cosine_scores = []
                for ds_img in dataset_imgs_list:
                    ds_tensor = self.transform(Image.fromarray(cv2.cvtColor(ds_img, cv2.COLOR_BGR2RGB))).unsqueeze(0)
                    with torch.no_grad():
                        ds_features = self.model(ds_tensor).numpy()
                    cosine_scores.append(self.calculate_cosine_similarity(pacient_features, ds_features))
                avg_cosine = calculate_statistics(cosine_scores)
                mode = avg_cosine['mode'] if avg_cosine['mode'] is not None else 0
                print("Cosine statistics:", avg_cosine)
                result = "Cancer" if mode >= 67 else "No cancer"
                csv_rows.append([filename, segment_type, "cosine", round(mode, 2), result])
            except Exception as e:
                print("Error en cosine:", e)

            # # ---------- Metric: Dice ----------
            print(">>Calculating dice coefficient")
            try:
                pacient_mask = self.extract_green_mask(pacient_img)
                dice_scores = []
                for ds_img in dataset_imgs_list:
                    ds_mask = self.extract_green_mask(ds_img)
                    dice_scores.append(self.dice_coefficient_images(pacient_mask, ds_mask) * 100)
                avg_dice = calculate_statistics(dice_scores)
                print("Dice statistics:", avg_dice)
                mode = avg_dice['mode'] if avg_dice['mode'] is not None else 0
                result = "Cancer" if mode >= 40 else "No cancer"
                csv_rows.append([filename, segment_type, "dice", round(mode, 2), result])
            except Exception as e:
                print("Error en dice:", e)

            # # ---------- Metric: IoU ----------
            print(">>Calculating IoU")
            try:
                pacient_mask = self.extract_green_mask(pacient_img)
                iou_scores = []
                for ds_img in dataset_imgs_list:
                    ds_mask = self.extract_green_mask(ds_img)
                    iou_scores.append(self.iou_coefficient_images(pacient_mask, ds_mask) * 100)
                avg_iou = calculate_statistics(iou_scores)
                print("IoU statistics:", avg_iou)
                mode = avg_iou['mode'] if avg_iou['mode'] is not None else 0
                result = "Cancer" if mode >= 39 else "No cancer"
                csv_rows.append([filename, segment_type, "iou", round(mode, 2), result])
            except Exception as e:
                print("Error en iou:", e)

            # # ---------- Metric: PSNR ----------
            print(">>Calculating PSNR")
            try:
                psnr_scores = []
                for ds_img in dataset_imgs_list:
                    if pacient_img.shape == ds_img.shape:
                        psnr_scores.append(self.calculate_psnr(pacient_img, ds_img))
                avg_psnr = calculate_statistics(psnr_scores)
                print("PSNR statistics:", avg_psnr)
                mode = avg_psnr['mode'] if avg_psnr['mode'] is not None else 0
                result = "Cancer" if mode <= 10 else "No cancer"
                csv_rows.append([filename, segment_type, "psnr", round(mode, 2), result])
            except Exception as e:
                print("Error en psnr:", e)

        # ---------- Metric: FID (solo una vez por lote) ----------
        print(">>Calculating FID")
        try:
            fid_value = self.calculate_fid_score(pacient_imgs_list, dataset_imgs_list)
            print("FID Value:", fid_value)
            result = "Cáncer" if fid_value <= 30 else "No cáncer"
            csv_rows.append(["LOTE", "inceptionv3", "fid", round(fid_value, 2), result])
        except Exception as e:
            print("Error en fid:", e)

        # ---------- Save CSV ----------
        print(">>Saving CSV")
        try:
            with open(output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["imagen", "modelo", "metrica", "resultado %", "diagnostico"])
                writer.writerows(csv_rows)
            print(f"CSV guardado en: {output_path}")
        except Exception as e:
            print("Error al guardar CSV:", e)

    def get_images_from_local_folder(self, folder_path):
        """
        Reads all images from a local folder and returns them as a list of dictionaries
        with the keys 'image' (np.ndarray) and 'name' (filename).
        """
        import cv2
        import numpy as np
        images = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(folder_path, filename)
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                if image is not None:
                    images.append({'image': image, 'name': filename})

        print(f"Imágenes leídas de dataset: {len(images)}")
        return images

def visualizar_mascara_verde(imagen_bgr, extract_mask_fn, titulo="Visualización máscara"):
    """
    Display the original BGR image alongside the binary mask extracted with extract_green_mask.

    Args:
        imagen_bgr (np.ndarray): Original image in BGR format.
        extract_mask_fn (callable): Function that extracts the mask (e.g., extract_green_mask).
        titulo (str): Title for the figure.
    """
    # Ensure the image has the correct format
    if imagen_bgr is None or imagen_bgr.ndim != 3 or imagen_bgr.shape[2] != 3:
        raise ValueError("La imagen debe ser un arreglo BGR válido con 3 canales.")

    # Convert BGR image to RGB for visualization with matplotlib
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)

    # Generate binary mask
    mascara_binaria = extract_mask_fn(imagen_bgr)

    # Show side by side
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(imagen_rgb)
    plt.title("Imagen Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(mascara_binaria, cmap="gray")
    plt.title("Máscara Verde (Binaria)")
    plt.axis("off")

    plt.suptitle(titulo)
    plt.tight_layout()
    plt.show()

class ImageSimilarityTest:
    def __init__(self, original_image_path, compare_image_path):
        self.original_image_path = original_image_path
        self.compare_image_path = compare_image_path

    def are_images_identical(self):
        """
        Compares if two images are identical pixel by pixel.
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
        Calculates the similarity between two images using SIFT and FLANN.
        Returns the similarity percentage and the image with the matches.
        """
        original = cv2.imread(self.original_image_path, cv2.IMREAD_GRAYSCALE)
        compare = cv2.imread(self.compare_image_path, cv2.IMREAD_GRAYSCALE)

        # Initialize SIFT
        print(">>Initializing SIFT")
        sift = cv2.SIFT_create()

        # Detect keypoints and descriptors
        print(">>Detecting keypoints and descriptors")
        kp1, desc1 = sift.detectAndCompute(original, None)
        kp2, desc2 = sift.detectAndCompute(compare, None)

        # Configure FLANN
        print(">>Configuring FLANN")
        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Find matches
        print(">>Finding matches")
        matches = flann.knnMatch(desc1, desc2, k=2)

        # Filter good matches using the Lowe ratio
        print(">>Filtering good matches")
        good_points = []
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                good_points.append(m)

        # Calculate the similarity percentage
        print(">>Calculating similarity")
        number_keypoints = min(len(kp1), len(kp2))
        similarity_percentage = (len(good_points) / number_keypoints * 100 if number_keypoints > 0 else 0)

        # Draw the matches
        print(">>Drawing matches")
        result_image = cv2.drawMatches(
            cv2.imread(self.original_image_path), kp1,
            cv2.imread(self.compare_image_path), kp2,
            good_points, None
        )

        # Save the result image
        print(">>Saving result image")
        result_path = os.path.join(settings.MEDIA_ROOT, "feature_matching.jpg")
        cv2.imwrite(result_path, result_image)

        return similarity_percentage, result_path