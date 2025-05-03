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
from skimage import filters, segmentation as skimage_segmentation, color

class SamImageSegmenter:
    def __init__(self):
        # Load SAM model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
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

        for image_file in image_files:
            
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

    def segment_images(self, image_files, image_path=None):
        segmented_images = []

        for image_file in image_files:
            # Guardar temporalmente el archivo si es un ContentFile
            if isinstance(image_file, ContentFile):
                temp_file_path = default_storage.save(f"temp/{image_file.name}", image_file)
                img_path = default_storage.path(temp_file_path)
            else:
                img_path = image_file

            # Cargar la imagen
            print('>>Cargar la imagen')
            imgn = Image.open(img_path)
            
            # Convertir a RGB si tiene canal alfa (RGBA)
            print('>>Convertir a RGB si tiene canal alfa (RGBA)')
            if imgn.mode == 'RGBA':
                imgn = imgn.convert('RGB')
                
            img = np.array(imgn)
            
            # Convertir a escala de grises si es una imagen a color
            print('>>Convertir a escala de grises si es una imagen a color')
            if len(img.shape) == 3:
                img_gray = color.rgb2gray(img)
            else:
                img_gray = img / 255.0 if img.max() > 1 else img
                
            # Mostrar imagen inicial
            # print('>>Mostrar imagen inicial')
            # plt.figure(figsize=(8, 6))
            # plt.title("Imagen Histológica Original")
            # plt.imshow(img)
            # plt.axis("off")
            # plt.show()
            
            # Preprocesamiento - mejora de contraste
            print('>>Preprocesamiento - mejora de contraste')
            p2, p98 = np.percentile(img_gray, (2, 98))
            img_rescale = np.clip((img_gray - p2) / (p98 - p2), 0, 1)
            
            # Mostrar imagen preprocesada
            # print('>>Mostrar imagen preprocesada')
            # plt.figure(figsize=(8, 6))
            # plt.title("Imagen Preprocesada")
            # plt.imshow(img_rescale, cmap="gray")
            # plt.axis("off")
            # plt.show()
            
            # Crear marcadores adaptados a histología
            # Ajustar estos umbrales según la imagen específica
            print('>>Crear marcadores adaptados a histología')
            markers = np.zeros_like(img_gray, dtype=np.uint8)
            
            # Marcar estructuras oscuras (núcleos, estructuras epiteliales)
            print('>>Marcar estructuras oscuras (núcleos, estructuras epiteliales)')
            markers[img_gray < 0.4] = 1
            
            # Marcar estructuras claras (fondo, espacios vacíos)
            print('>>Marcar estructuras claras (fondo, espacios vacíos)')
            markers[img_gray > 0.8] = 2
            
            # Marcar tejido conectivo (valores intermedios)
            print('>>Marcar tejido conectivo (valores intermedios)')
            mask_conectivo = (img_gray >= 0.5) & (img_gray <= 0.7)
            markers[mask_conectivo] = 3
            
            # Mostrar marcadores
            # print('>>Mostrar marcadores')
            # plt.figure(figsize=(8, 6))
            # plt.title("Marcadores para Tejidos")
            # plt.imshow(markers, cmap="nipy_spectral")
            # plt.colorbar(label='Tipo de Tejido')
            # plt.axis("off")
            # plt.show()
            
            # Calcular el mapa de elevación con un filtro más adecuado para tejidos
            print('>>Calcular el mapa de elevación con un filtro más adecuado para tejidos')
            elevation_map = filters.scharr(img_gray)
            
            # Mostrar mapa de elevación
            # print('>>Mostrar mapa de elevación')
            # plt.figure(figsize=(8, 6))
            # plt.title("Mapa de Bordes (Filtro Scharr)")
            # plt.imshow(elevation_map, cmap="magma")
            # plt.axis("off")
            # plt.show()
            
            # Realizar la segmentación watershed
            print('>>Realizar la segmentación watershed')
            segmentation = skimage_segmentation.watershed(elevation_map, markers, watershed_line=True)
            
            # Mostrar segmentación obtenida
            # print('>>Mostrar segmentación obtenida')
            # plt.figure(figsize=(8, 6))
            # plt.title("Segmentación de Tejidos")
            # plt.imshow(segmentation, cmap="nipy_spectral")
            # plt.colorbar(label='Regiones')
            # plt.axis("off")
            # plt.show()
            
            # Superponer resultado sobre la imagen original
            # print('>>Superponer resultado sobre la imagen original')
            # plt.figure(figsize=(10, 8))
            # plt.title("Resultado: Imagen Original con Segmentación")
            # plt.imshow(img)
            # plt.imshow(segmentation, alpha=0.5, cmap="nipy_spectral")
            # plt.axis("off")
            # plt.show()

            # Guardar la segmentación como imagen procesada temporalmente
            print('>>Guardar la segmentación como imagen procesada temporalmente')
            output_filename = f"segmented_{os.path.basename(img_path)}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
            plt.imsave(output_path, segmentation, cmap="nipy_spectral")

            # Leer la imagen procesada y convertirla a ContentFile
            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=output_filename)

            segmented_images.append(segmented_image_content)

        return segmented_images
