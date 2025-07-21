# models.py
import torch
import numpy as np
import cv2
import os
from io import BytesIO
import zipfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from PIL import Image
import matplotlib.pyplot as plt
from skimage import filters, segmentation as skimage_segmentation, color, morphology, measure
from scipy import ndimage
from scipy.ndimage import maximum_filter
from .UNet import UNet
import torchvision.transforms as T
from skimage.morphology import remove_small_objects, remove_small_holes
import base64

class SamImageSegmenter:
    def __init__(self):
        # Load SAM model
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # if self.device == "cuda":
        #     torch.cuda.empty_cache()
        self.device = 'cpu'

        sam_checkpoint = "sam_vit_h.pth"
        model_type = "vit_h"
        
        # Carga el modelo en CPU primero
        self.sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.sam.to(device=self.device)  # Mueve a CUDA aquí
        
        # Opcional: Limpia la caché de CUDA
        if self.device == "cuda":
            torch.cuda.empty_cache()
            
        self.mask_generator = SamAutomaticMaskGenerator(self.sam)

    def segment_images(self, image_files, image_path = None):
        segmented_images = []

        cont = 0
        for image_file in image_files:
            cont = cont + 1
            print(f'>>Imagen {cont} de {len(image_files)}')
            # Guardar la imagen temporalmente
            if image_path is None:
                file_path = default_storage.save("uploads/" + image_file.name, ContentFile(image_file.read()))
            else:
                file_path = image_path

            # Leer la imagen
            print('>>Leer la imagen')
            img = cv2.imread(default_storage.path(file_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Generar máscaras
            print('>>Generar máscaras')
            masks = self.mask_generator.generate(img_rgb)

            # Aplicar máscara sobre la imagen
            print('>>Aplicar máscara sobre la imagen')
            mask_image = np.zeros_like(img, dtype=np.uint8)

            for mask in masks:
                segmentation = mask["segmentation"]
                mask_image[segmentation] = [0, 255, 0]  # Máscara en color verde

            # Combinar la imagen original con la máscara
            print('>>Combinar la imagen original con la máscara')
            blended = cv2.addWeighted(img, 0.6, mask_image, 0.4, 0)

            # Guardar la imagen procesada temporalmente
            print('>>Guardar la imagen procesada temporalmente')
            output_path = os.path.join(settings.MEDIA_ROOT, f"segmented_{image_file.name}")
            cv2.imwrite(output_path, blended)

            # ESTE CODIGO ES PARA QUE GENERE LA IMAGEN EN BLANCO Y NEGRO
            # binary_mask = np.zeros(img.shape[:2], dtype=np.uint8)
            # for mask in masks:
            #     segmentation = mask["segmentation"]
            #     binary_mask[segmentation] = 1  # Marca como blanco

            # # Guardar la imagen procesada temporalmente en blanco y negro
            # print('>>Guardar la imagen procesada temporalmente')
            # output_path = os.path.join(settings.MEDIA_ROOT, f"segmented_{image_file.name}")
            # cv2.imwrite(output_path, binary_mask * 255)

            # Leer la imagen procesada y convertirla a ContentFile
            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=f"segmented_{image_file.name}")

            segmented_images.append(segmented_image_content)

        return segmented_images

    def create_zip(self, segmented_images):
        # Crear un archivo ZIP con las imágenes segmentadas
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img_path in segmented_images:
                zip_file.write(img_path, os.path.basename(img_path))
        zip_buffer.seek(0)
        return zip_buffer


class SkimageSegmenter:

    def _preprocess_histological_image(self, img_rgb):
        """
        Preprocesamiento específico para imágenes histológicas
        """
        # Convertir a diferentes espacios de color para mejor análisis
        img_hsv = color.rgb2hsv(img_rgb)
        img_gray = color.rgb2gray(img_rgb)
        
        # Mejorar contraste usando CLAHE (Contrast Limited Adaptive Histogram Equalization)
        img_gray_uint8 = (img_gray * 255).astype(np.uint8)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_enhanced = clahe.apply(img_gray_uint8) / 255.0
        
        return img_enhanced, img_hsv, img_gray

    def _detect_cancer_regions(self, img_enhanced, img_hsv, img_rgb):
        """
        Detecta regiones potencialmente cancerígenas basándose en características histológicas
        """
        # Análisis de color específico para tejido canceroso
        # Las células cancerosas tienden a ser más basófilas (azul-púrpura)
        hue = img_hsv[:,:,0]
        saturation = img_hsv[:,:,1]
        value = img_hsv[:,:,2]
        
        # Detectar regiones con alta densidad nuclear (más oscuras y azuladas)
        nuclear_mask = (hue > 0.6) & (hue < 0.8) & (saturation > 0.3) & (value < 0.7)
        
        # Detectar regiones hipercromáticas (núcleos más densos)
        hyperchromatic_mask = img_enhanced < np.percentile(img_enhanced, 25)
        
        # Combinar máscaras
        potential_cancer = nuclear_mask | hyperchromatic_mask
        
        # Limpiar ruido con operaciones morfológicas
        kernel = morphology.disk(2)
        potential_cancer = morphology.binary_opening(potential_cancer, kernel)
        potential_cancer = morphology.binary_closing(potential_cancer, morphology.disk(3))
        
        return potential_cancer

    def _find_local_maxima(self, distance_map, min_distance=10, threshold_abs=3):
        """
        Encuentra máximos locales usando scipy en lugar de skimage.feature
        """
        # Crear un filtro de máximo local
        local_maxima = maximum_filter(distance_map, size=min_distance) == distance_map
        
        # Aplicar umbral
        local_maxima = local_maxima & (distance_map > threshold_abs)
        
        # Obtener coordenadas de los máximos
        coords = np.where(local_maxima)
        
        return coords

    def _create_smart_markers(self, img_enhanced, potential_cancer_mask):
        """
        Crea marcadores inteligentes para watershed controlado
        """
        markers = np.zeros_like(img_enhanced, dtype=np.int32)
        
        # 1. Marcadores para fondo (regiones muy claras)
        background_threshold = np.percentile(img_enhanced, 85)
        background_mask = img_enhanced > background_threshold
        
        # Limpiar el fondo
        background_mask = morphology.binary_opening(background_mask, morphology.disk(5))
        background_mask = morphology.remove_small_objects(background_mask, min_size=100)
        
        # 2. Marcadores para regiones cancerosas potenciales
        # Aplicar distance transform para encontrar centros de regiones
        cancer_distance = ndimage.distance_transform_edt(potential_cancer_mask)
        
        # Encontrar máximos locales como centros de regiones cancerosas
        cancer_peaks = self._find_local_maxima(cancer_distance, min_distance=10, threshold_abs=3)
        
        # 3. Marcadores para tejido normal (valores intermedios)
        normal_tissue_mask = (~potential_cancer_mask) & (~background_mask)
        normal_distance = ndimage.distance_transform_edt(normal_tissue_mask)
        normal_peaks = self._find_local_maxima(normal_distance, min_distance=15, threshold_abs=5)
        
        # Asignar etiquetas a los marcadores
        marker_id = 1
        
        # Marcar fondo
        markers[background_mask] = marker_id
        marker_id += 1
        
        # Marcar centros de regiones cancerosas
        if len(cancer_peaks[0]) > 0:
            for i in range(len(cancer_peaks[0])):
                y, x = cancer_peaks[0][i], cancer_peaks[1][i]
                # Crear una pequeña región alrededor del pico
                y_start, y_end = max(0, y-2), min(img_enhanced.shape[0], y+3)
                x_start, x_end = max(0, x-2), min(img_enhanced.shape[1], x+3)
                markers[y_start:y_end, x_start:x_end] = marker_id
                marker_id += 1
        
        # Marcar centros de tejido normal (con menos marcadores)
        if len(normal_peaks[0]) > 0:
            # Limitar el número de marcadores de tejido normal
            n_normal_markers = min(len(normal_peaks[0]), len(cancer_peaks[0]) // 2 + 1)
            for i in range(n_normal_markers):
                y, x = normal_peaks[0][i], normal_peaks[1][i]
                y_start, y_end = max(0, y-3), min(img_enhanced.shape[0], y+4)
                x_start, x_end = max(0, x-3), min(img_enhanced.shape[1], x+4)
                markers[y_start:y_end, x_start:x_end] = marker_id
                marker_id += 1

        # plt.figure(figsize=(8, 6))
        # plt.title("Marcadores inteligentes")
        # plt.imshow(markers, cmap="nipy_spectral")
        # plt.axis("off")
        # plt.show()
        
        return markers

    def _create_gradient_map(self, img_enhanced):
        """
        Crea un mapa de gradientes más apropiado para tejidos
        Además, muestra las imágenes generadas por los filtros Scharr, Sobel y Gaussian.
        """
        import matplotlib.pyplot as plt

        # Combinar diferentes filtros de gradiente
        scharr_grad = filters.scharr(img_enhanced)
        sobel_grad = filters.sobel(img_enhanced)
        
        # Promedio ponderado de gradientes
        gradient_map = 0.6 * scharr_grad + 0.4 * sobel_grad
        
        # Suavizar ligeramente para reducir ruido
        gaussian_grad = filters.gaussian(gradient_map, sigma=0.5)

        # Mostrar resultados de los filtros
        # plt.figure(figsize=(8, 6))
        # # plt.subplot(1, 4, 1)
        # plt.imshow(img_enhanced, cmap='gray')
        # plt.title('Imagen Mejorada')
        # plt.axis('off')
        # plt.show()

        # # plt.subplot(1, 4, 2)
        # plt.figure(figsize=(8, 6))
        # plt.imshow(scharr_grad, cmap='magma')
        # plt.title('Filtro Scharr')
        # plt.axis('off')
        # plt.show()

        # # plt.subplot(1, 4, 3)
        # plt.figure(figsize=(8, 6))
        # plt.imshow(sobel_grad, cmap='magma')
        # plt.title('Filtro Sobel')
        # plt.axis('off')
        # plt.show()

        # # plt.subplot(1, 4, 4)
        # plt.figure(figsize=(8, 6))
        # plt.imshow(gaussian_grad, cmap='magma')
        # plt.title('Filtro Gaussian')
        # plt.axis('off')
        # plt.show()

        # plt.tight_layout()

        return gaussian_grad

    def _post_process_segmentation(self, segmentation, potential_cancer_mask, min_region_size=50):
        """
        Post-procesamiento para limpiar la segmentación
        """
        # Remover regiones muy pequeñas
        cleaned_segmentation = morphology.remove_small_objects(
            segmentation.astype(bool), min_size=min_region_size
        ).astype(segmentation.dtype)
        
        # Re-etiquetar regiones
        labeled_segmentation = measure.label(cleaned_segmentation)
        
        # Filtrar regiones que no coinciden con áreas potencialmente cancerosas
        final_segmentation = np.zeros_like(labeled_segmentation)
        region_id = 1
        
        for region in measure.regionprops(labeled_segmentation):
            # Calcular overlap con mask de cáncer potencial
            region_mask = labeled_segmentation == region.label
            overlap = np.sum(region_mask & potential_cancer_mask) / np.sum(region_mask)
            
            # Solo mantener regiones con suficiente overlap con áreas cancerosas potenciales
            if overlap > 0.3:  # Al menos 30% de overlap
                final_segmentation[region_mask] = region_id
                region_id += 1
        
        return final_segmentation

    def segment_images(self, image_files, image_path=None):
        segmented_images = []

        for image_file in image_files:
            # Guardar temporalmente el archivo si es un ContentFile
            if isinstance(image_file, ContentFile):
                temp_file_path = default_storage.save(f"temp/{image_file.name}", image_file)
                img_path = default_storage.path(temp_file_path)
            else:
                img_path = image_file

            print('>>Cargando y preprocesando imagen')
            imgn = Image.open(img_path)
            
            # Convertir a RGB si tiene canal alfa (RGBA)
            if imgn.mode == 'RGBA':
                imgn = imgn.convert('RGB')
                
            img_rgb = np.array(imgn)
            
            # Preprocesamiento específico para histología
            img_enhanced, img_hsv, img_gray = self._preprocess_histological_image(img_rgb)
            
            print('>>Detectando regiones potencialmente cancerosas')
            potential_cancer_mask = self._detect_cancer_regions(img_enhanced, img_hsv, img_rgb)
            
            print('>>Creando marcadores inteligentes')
            markers = self._create_smart_markers(img_enhanced, potential_cancer_mask)
            
            print('>>Calculando mapa de gradientes optimizado')
            gradient_map = self._create_gradient_map(img_enhanced)
            
            print('>>Aplicando Watershed controlado por marcadores')
            segmentation = skimage_segmentation.watershed(
                gradient_map, 
                markers, 
                mask=potential_cancer_mask,  # Solo segmentar en áreas de interés
                watershed_line=True
            )

            # plt.figure(figsize=(8, 6))
            # plt.imshow(segmentation, cmap='nipy_spectral')
            # plt.title('Segmentación con Watershed')
            # plt.axis('off')
            # plt.show()
            
            print('>>Post-procesando segmentación')
            final_segmentation = self._post_process_segmentation(
                segmentation, potential_cancer_mask
            )
            
            # Crear máscara binaria para todas las regiones segmentadas
            binary_segmentation_mask = final_segmentation > 0
            
            # Crear visualización final usando el mismo approach que el otro proyecto
            print('>>Generando imagen de resultado usando cv2.addWeighted')
            
            # Convertir imagen original a formato BGR para OpenCV (si es necesario para consistencia)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            
            # Crear imagen de máscara similar al otro proyecto
            mask_image = np.zeros_like(img_bgr, dtype=np.uint8)
            
            # Aplicar el mismo color verde del otro proyecto [0, 255, 0]
            # Convertir de RGB a BGR para OpenCV: [0, 255, 0] -> BGR [0, 255, 0]
            green_bgr = [0, 255, 0]  # Verde puro en formato BGR (igual al otro proyecto)
            mask_image[binary_segmentation_mask] = green_bgr
            
            # Combinar la imagen original con la máscara usando los mismos pesos
            print('>>Combinar la imagen original con la máscara')
            blended = cv2.addWeighted(img_bgr, 0.6, mask_image, 0.4, 0)
            
            # Convertir de vuelta a RGB para matplotlib
            blended_rgb = cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)
            
            # Mostrar resultado final
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            ax.imshow(blended_rgb)
            
            ax.axis('off')
            plt.tight_layout()
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

            # Guardar la segmentación como imagen procesada
            output_filename = f"segmented_{os.path.basename(img_path)}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
            blended_bgr = cv2.cvtColor(blended_rgb, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, blended_bgr)

            # ESTO GUARDA LA IMAGEN EN BLANCO Y NEGRO
            # binary_output_filename = f"cancer_segmented_binary_{os.path.basename(img_path)}"
            # binary_output_path = os.path.join(settings.MEDIA_ROOT, binary_output_filename)
            # cv2.imwrite(binary_output_path, binary_segmentation_mask.astype(np.uint8) * 255)

            # # Leer la imagen binaria procesada y convertirla a ContentFile (opcional, si la necesitas en la respuesta)
            # with open(binary_output_path, 'rb') as f:
            #     binary_image_data = f.read()
            # binary_segmented_image_content = ContentFile(binary_image_data, name=binary_output_filename)


            # ESTO MUESTRA LA IMAGEN ORIGINAL SEGMENTADA
            # plt.figure(figsize=(8, 6))
            # plt.imshow(blended_rgb, cmap='nipy_spectral')
            # plt.title('Imagen original segmentada')
            # plt.axis('off')
            # plt.show()

            # Leer la imagen procesada y convertirla a ContentFile
            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=output_filename)

            segmented_images.append(segmented_image_content)
            
            # Limpiar archivo temporal si fue creado
            if isinstance(image_file, ContentFile):
                default_storage.delete(temp_file_path)

        return segmented_images

class UnetImageSegmenter:
    
    def segment_images(self, image_files):
        model = UNet(in_channels=3, out_channels=1)
        model_path = os.path.join(os.path.dirname(__file__), "trained_models", "unet_stomach_cancer_model.pth")
        model.load_state_dict(torch.load(model_path, weights_only=True))
        model.eval()

        segmented_images = []
        elevation_maps_base64 = []

        for image_file in image_files:
            if isinstance(image_file, ContentFile):
                temp_file_path = default_storage.save(f"temp/{image_file.name}", image_file)
                img_path = default_storage.path(temp_file_path)
            else:
                img_path = image_file

            image = Image.open(img_path).convert("RGB")

            transform = T.Compose([
                T.Resize((512, 512)),
                T.ToTensor(),
                T.Normalize(mean=[0.8896, 0.7711, 0.9064], std=[0.1091, 0.1464, 0.0761])
            ])
            input_tensor = transform(image).unsqueeze(0)

            with torch.no_grad():
                pred_mask = model(input_tensor)

            pred_mask_np = pred_mask.squeeze().numpy()
            binary_mask = (pred_mask_np >= 0.3).astype("uint8")
            binary_mask = self.clean_mask(binary_mask)

            # Guardar imagen segmentada
            output_path = os.path.join(settings.MEDIA_ROOT, f"segmented_{image_file.name}")
            cv2.imwrite(output_path, binary_mask * 255)

            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=f"segmented_{image_file.name}")
            segmented_images.append(segmented_image_content)

            # Generar y codificar mapa de elevación
            elevation_img = (pred_mask_np * 255).astype("uint8")
            _, buffer = cv2.imencode(".png", elevation_img)
            elevation_b64 = base64.b64encode(buffer).decode("utf-8")
            elevation_maps_base64.append(elevation_b64)

            if isinstance(image_file, ContentFile):
                default_storage.delete(temp_file_path)

        return segmented_images, elevation_maps_base64


    def clean_mask(self, binary_mask):
        # Asegúrate de que sea booleano para skimage
        mask = binary_mask.astype(bool)
        # Elimina objetos pequeños (ruido)
        mask = remove_small_objects(mask, min_size=500)
        # Rellena pequeños huecos dentro de las regiones
        mask = remove_small_holes(mask, area_threshold=500)
        # Convierte de nuevo a uint8
        mask = mask.astype("uint8")
        # Aplica cierre morfológico para agrupar regiones cercanas
        kernel = np.ones((15, 15), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # Aplica apertura para suavizar bordes
        kernel2 = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2)
        # Suaviza los bordes con un filtro gaussiano y vuelve a binarizar
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        # mask = (mask > 0.4).astype("uint8")
        return mask