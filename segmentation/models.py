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

class SamImageSegmenter:
    def __init__(self):
        # Load SAM model
        sam_checkpoint = "sam_vit_h.pth"
        model_type = "vit_h"
        self.sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.sam.to(device="cuda" if torch.cuda.is_available() else "cpu")
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