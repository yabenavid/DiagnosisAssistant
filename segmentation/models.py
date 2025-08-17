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
        self.device = 'cpu'

        sam_checkpoint = "sam_vit_h.pth"
        model_type = "vit_h"
        
        # Load the SAM model
        self.sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.sam.to(device=self.device)
        
        if self.device == "cuda":
            torch.cuda.empty_cache()
            
        self.mask_generator = SamAutomaticMaskGenerator(self.sam)

    def segment_images(self, image_files, image_path = None):
        segmented_images = []

        cont = 0
        for image_file in image_files:
            cont = cont + 1
            print(f'>>Imagen {cont} de {len(image_files)}')
            # Save image temporarily
            if image_path is None:
                file_path = default_storage.save("uploads/" + image_file.name, ContentFile(image_file.read()))
            else:
                file_path = image_path

            img = cv2.imread(default_storage.path(file_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Generate masks
            masks = self.mask_generator.generate(img_rgb)

            # Apply mask to the image
            mask_image = np.zeros_like(img, dtype=np.uint8)

            for mask in masks:
                segmentation = mask["segmentation"]
                mask_image[segmentation] = [0, 255, 0]  # Green color

            # Combine original image with mask
            blended = cv2.addWeighted(img, 0.6, mask_image, 0.4, 0)

            # Save processed image temporarily
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

            # Read processed image and convert to ContentFile
            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=f"segmented_{image_file.name}")

            segmented_images.append(segmented_image_content)

        return segmented_images

    def create_zip(self, segmented_images):
        # Create a ZIP file with the segmented images
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img_path in segmented_images:
                zip_file.write(img_path, os.path.basename(img_path))
        zip_buffer.seek(0)
        return zip_buffer


class SkimageSegmenter:

    def _preprocess_histological_image(self, img_rgb):
        """
        Specific preprocessing for histological images
        """
        # Convert to different color spaces for better analysis
        img_hsv = color.rgb2hsv(img_rgb)
        img_gray = color.rgb2gray(img_rgb)

        # Improve contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        img_gray_uint8 = (img_gray * 255).astype(np.uint8)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_enhanced = clahe.apply(img_gray_uint8) / 255.0
        
        return img_enhanced, img_hsv, img_gray

    def _detect_cancer_regions(self, img_enhanced, img_hsv, img_rgb):
        """
        Detects potentially cancerous regions based on histological features
        """
        # Specific color analysis for cancerous tissue
        # Cancer cells tend to be more basophilic (blue-purple)
        hue = img_hsv[:,:,0]
        saturation = img_hsv[:,:,1]
        value = img_hsv[:,:,2]

        # Detect regions with high nuclear density (darker and more bluish)
        nuclear_mask = (hue > 0.6) & (hue < 0.8) & (saturation > 0.3) & (value < 0.7)

        # Detect hyperchromatic regions (denser nuclei)
        hyperchromatic_mask = img_enhanced < np.percentile(img_enhanced, 25)
        
        # Combine masks
        potential_cancer = nuclear_mask | hyperchromatic_mask
        
        # Cleaning noise with morphological operations
        kernel = morphology.disk(2)
        potential_cancer = morphology.binary_opening(potential_cancer, kernel)
        potential_cancer = morphology.binary_closing(potential_cancer, morphology.disk(3))
        
        return potential_cancer

    def _find_local_maxima(self, distance_map, min_distance=10, threshold_abs=3):
        """
        Find local maxima using scipy instead of skimage.feature
        """
        # Create a local maximum filter
        local_maxima = maximum_filter(distance_map, size=min_distance) == distance_map

        # Apply threshold
        local_maxima = local_maxima & (distance_map > threshold_abs)

        # Get coordinates of the maxima
        coords = np.where(local_maxima)
        
        return coords

    def _create_smart_markers(self, img_enhanced, potential_cancer_mask):
        """
        Create smart markers for controlled watershed
        """
        markers = np.zeros_like(img_enhanced, dtype=np.int32)

        # Markers for background (very light regions)
        background_threshold = np.percentile(img_enhanced, 85)
        background_mask = img_enhanced > background_threshold

        # Clean the background
        background_mask = morphology.binary_opening(background_mask, morphology.disk(5))
        background_mask = morphology.remove_small_objects(background_mask, min_size=100)

        # Markers for potential cancer regions
        # Apply distance transform to find centers of regions
        cancer_distance = ndimage.distance_transform_edt(potential_cancer_mask)

        # Find local maxima as centers of cancerous regions
        cancer_peaks = self._find_local_maxima(cancer_distance, min_distance=10, threshold_abs=3)

        # Markers for normal tissue (intermediate values)
        normal_tissue_mask = (~potential_cancer_mask) & (~background_mask)
        normal_distance = ndimage.distance_transform_edt(normal_tissue_mask)
        normal_peaks = self._find_local_maxima(normal_distance, min_distance=15, threshold_abs=5)

        # Assign labels to the markers
        marker_id = 1

        # Mark background
        markers[background_mask] = marker_id
        marker_id += 1

        # Mark centers of cancerous regions
        if len(cancer_peaks[0]) > 0:
            for i in range(len(cancer_peaks[0])):
                y, x = cancer_peaks[0][i], cancer_peaks[1][i]
                # Create a small region around the peak
                y_start, y_end = max(0, y-2), min(img_enhanced.shape[0], y+3)
                x_start, x_end = max(0, x-2), min(img_enhanced.shape[1], x+3)
                markers[y_start:y_end, x_start:x_end] = marker_id
                marker_id += 1
        
        # Mark normal tissue centers (with fewer markers)
        if len(normal_peaks[0]) > 0:
            # Limit the number of normal tissue markers
            n_normal_markers = min(len(normal_peaks[0]), len(cancer_peaks[0]) // 2 + 1)
            for i in range(n_normal_markers):
                y, x = normal_peaks[0][i], normal_peaks[1][i]
                y_start, y_end = max(0, y-3), min(img_enhanced.shape[0], y+4)
                x_start, x_end = max(0, x-3), min(img_enhanced.shape[1], x+4)
                markers[y_start:y_end, x_start:x_end] = marker_id
                marker_id += 1
        
        return markers

    def _create_gradient_map(self, img_enhanced):
        """
        Create a gradient map more suitable for tissues
        Additionally, display the images generated by the Scharr, Sobel, and Gaussian filters.
        """
        import matplotlib.pyplot as plt

        # Combine different gradient filters
        scharr_grad = filters.scharr(img_enhanced)
        sobel_grad = filters.sobel(img_enhanced)

        # Weighted average of gradients
        gradient_map = 0.6 * scharr_grad + 0.4 * sobel_grad

        # Slightly smooth to reduce noise
        gaussian_grad = filters.gaussian(gradient_map, sigma=0.5)

        return gaussian_grad

    def _post_process_segmentation(self, segmentation, potential_cancer_mask, min_region_size=50):
        """
        Post-processing to clean up the segmentation
        """
        # Remove very small regions
        cleaned_segmentation = morphology.remove_small_objects(
            segmentation.astype(bool), min_size=min_region_size
        ).astype(segmentation.dtype)

        # Re-label regions
        labeled_segmentation = measure.label(cleaned_segmentation)

        # Filter regions that do not overlap with potential cancer areas
        final_segmentation = np.zeros_like(labeled_segmentation)
        region_id = 1
        
        for region in measure.regionprops(labeled_segmentation):
            # Calculate overlap with potential cancer mask
            region_mask = labeled_segmentation == region.label
            overlap = np.sum(region_mask & potential_cancer_mask) / np.sum(region_mask)

            # Only keep regions with sufficient overlap with potential cancer areas
            if overlap > 0.3:  # At least 30% overlap
                final_segmentation[region_mask] = region_id
                region_id += 1
        
        return final_segmentation

    def segment_images(self, image_files, image_path=None):
        segmented_images = []

        for image_file in image_files:
            # Save image temporarily
            if isinstance(image_file, ContentFile):
                temp_file_path = default_storage.save(f"temp/{image_file.name}", image_file)
                img_path = default_storage.path(temp_file_path)
            else:
                img_path = image_file

            print('>>Cargando y preprocesando imagen')
            imgn = Image.open(img_path)
            
            # Convert to RGB if it has alpha channel (RGBA)
            if imgn.mode == 'RGBA':
                imgn = imgn.convert('RGB')
                
            img_rgb = np.array(imgn)

            # Preprocessing specific to histology
            img_enhanced, img_hsv, img_gray = self._preprocess_histological_image(img_rgb)
            
            potential_cancer_mask = self._detect_cancer_regions(img_enhanced, img_hsv, img_rgb)
            
            markers = self._create_smart_markers(img_enhanced, potential_cancer_mask)
            
            gradient_map = self._create_gradient_map(img_enhanced)
            
            segmentation = skimage_segmentation.watershed(
                gradient_map, 
                markers, 
                mask=potential_cancer_mask,
                watershed_line=True
            )
            
            print('>>Post-procesando segmentación')
            final_segmentation = self._post_process_segmentation(
                segmentation, potential_cancer_mask
            )
            
            # Create binary mask for all segmented regions
            binary_segmentation_mask = final_segmentation > 0

            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

            mask_image = np.zeros_like(img_bgr, dtype=np.uint8)
            
            green_bgr = [0, 255, 0]
            mask_image[binary_segmentation_mask] = green_bgr

            # Combine the original image with the mask
            blended = cv2.addWeighted(img_bgr, 0.6, mask_image, 0.4, 0)
            
            blended_rgb = cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)
            
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            ax.imshow(blended_rgb)
            
            ax.axis('off')
            plt.tight_layout()
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

            # Save the segmentation as processed image
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

            # Read processed image and convert to ContentFile
            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=output_filename)

            segmented_images.append(segmented_image_content)
            
            # Clean temporal file
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

            # Save segmented image
            output_path = os.path.join(settings.MEDIA_ROOT, f"segmented_{image_file.name}")
            cv2.imwrite(output_path, binary_mask * 255)

            with open(output_path, 'rb') as f:
                image_data = f.read()
            segmented_image_content = ContentFile(image_data, name=f"segmented_{image_file.name}")
            segmented_images.append(segmented_image_content)

            # Generate and encode elevation map
            elevation_img = (pred_mask_np * 255).astype("uint8")
            _, buffer = cv2.imencode(".png", elevation_img)
            elevation_b64 = base64.b64encode(buffer).decode("utf-8")
            elevation_maps_base64.append(elevation_b64)

            if isinstance(image_file, ContentFile):
                default_storage.delete(temp_file_path)

        return segmented_images, elevation_maps_base64

    def clean_mask(self, binary_mask):
        mask = binary_mask.astype(bool)

        mask = remove_small_objects(mask, min_size=500)

        mask = remove_small_holes(mask, area_threshold=500)

        mask = mask.astype("uint8")
        # Apply morphological closing to group nearby regions
        kernel = np.ones((15, 15), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # Apply opening to smooth edges
        kernel2 = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2)
        # Smooth edges with Gaussian filter and binarize again
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        return mask