from django.db import models
from io import BytesIO
from PIL import Image, ImageFilter
from django.core.files.base import ContentFile
from .utils import pil_image_to_base64

# Create your models here.

class ImageResizer:

    def procesar_imagenes(self, image_files, target_width=1024, target_height=1024):
        """
        Process a list of image files by applying:
        1. Reducing size without losing quality.
        2. Improving quality through sharpening.
        3. Standardizing dimensions (fixed canvas).

        Returns an array of ContentFile, which includes the 'name' attribute and the read() method,
        allowing segment_images to process them without issues.

        Parameters:
        image_files (list): List of UploadedFile objects.
        target_width (int): Standard output width.
        target_height (int): Standard output height.

        Returns:
        list: Array of ContentFile objects with the processed images.
        """
        imagenes_procesadas = []
        imagenes_base64 = []
        img_base64 = None
        
        for file in image_files:
            file_bytes = file.read()
            
            # Open the image using Pillow and convert it to RGB
            imagen = Image.open(BytesIO(file_bytes)).convert("RGB")

            # Improve the quality by applying a sharpening filter
            imagen_mejorada = imagen.filter(ImageFilter.SHARPEN)

            # Calculate the scaling factor to adjust the image to the canvas without distortion
            scale = min(target_width / imagen_mejorada.width, target_height / imagen_mejorada.height)
            new_width = int(imagen_mejorada.width * scale)
            new_height = int(imagen_mejorada.height * scale)

            # Resize the image using a good resampling filter (LANCZOS)
            imagen_redimensionada = imagen_mejorada.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create a fixed-size canvas (black fill)
            canvas = Image.new("RGB", (target_width, target_height), "black")

            # Calculate the offsets to center the resized image on the canvas
            offset_x = (target_width - new_width) // 2
            offset_y = (target_height - new_height) // 2

            # Paste the resized image onto the canvas
            canvas.paste(imagen_redimensionada, (offset_x, offset_y))

            # Convert to base64
            img_base64 = pil_image_to_base64(canvas)
            imagenes_base64.append(img_base64)

            # Save the processed image to a buffer and create a ContentFile
            buffer = BytesIO()
            canvas.save(buffer, format="PNG")
            processed_file = ContentFile(buffer.getvalue(), name=file.name)
            imagenes_procesadas.append(processed_file)
        
        return imagenes_procesadas, imagenes_base64
    
    def convert_to_base64(self, image_files):
        """
        Converts a list of image files to base64.
        """
        result = []
        for file in image_files:
            img_base64 = pil_image_to_base64(Image.open(file).convert("RGB"))
            result.append(img_base64)
        return result