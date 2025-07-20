from django.db import models
from io import BytesIO
from PIL import Image, ImageFilter
from django.core.files.base import ContentFile
from .utils import pil_image_to_base64

# Create your models here.

class ImageResizer:

    def procesar_imagenes(self, image_files, target_width=1024, target_height=1024):
        """
        Procesa una lista de archivos de imagen aplicando:
        1. Reducción del tamaño sin perder calidad.
        2. Mejora de calidad mediante afilado.
        3. Estandarización de dimensiones (canvas fijo).
        
        Se retorna un array de ContentFile, que incluye el atributo 'name' y el método read(),
        permitiendo que segment_images las procese sin inconvenientes.
        
        Parámetros:
        image_files (list): Lista de objetos UploadedFile.
        target_width (int): Ancho estándar de salida.
        target_height (int): Alto estándar de salida.
        
        Retorna:
        list: Array de objetos ContentFile con las imágenes procesadas.
        """
        imagenes_procesadas = []
        imagenes_base64 = []
        img_base64 = None
        
        for file in image_files:
            # Leer el contenido en bytes de la imagen
            print('Leer el contenido en bytes de la imagen')
            file_bytes = file.read()
            
            # Abrir la imagen usando Pillow y convertirla a RGB
            print('>>Abrir la imagen usando Pillow y convertirla a RGB')
            imagen = Image.open(BytesIO(file_bytes)).convert("RGB")
            
            # Mejorar la calidad aplicando un filtro de afilado
            print('>>Mejorar la calidad aplicando un filtro de afilado')
            imagen_mejorada = imagen.filter(ImageFilter.SHARPEN)
            
            # Calcular el factor de escala para ajustar la imagen al canvas sin deformarla
            print('>>Calcular el factor de escala para ajustar la imagen al canvas sin deformarla')
            scale = min(target_width / imagen_mejorada.width, target_height / imagen_mejorada.height)
            new_width = int(imagen_mejorada.width * scale)
            new_height = int(imagen_mejorada.height * scale)
            
            # Redimensionar la imagen usando un buen filtro de remuestreo (LANCZOS)
            print('>>Redimensionar la imagen usando un buen filtro de remuestreo (LANCZOS)')
            imagen_redimensionada = imagen_mejorada.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crear un canvas de tamaño fijo (relleno de negro)
            print('>>Crear un canvas de tamaño fijo (relleno de negro)')
            canvas = Image.new("RGB", (target_width, target_height), "black")
            
            # Calcular los offsets para centrar la imagen redimensionada en el canvas
            print('>>Calcular los offsets para centrar la imagen redimensionada en el canvas')
            offset_x = (target_width - new_width) // 2
            offset_y = (target_height - new_height) // 2
            
            # Pegar la imagen redimensionada en el canvas
            print('>>Pegar la imagen redimensionada en el canvas')
            canvas.paste(imagen_redimensionada, (offset_x, offset_y))

            # Convertir a base64
            img_base64 = pil_image_to_base64(canvas)
            imagenes_base64.append(img_base64)
            
            # Guardar la imagen procesada en un buffer y crear un ContentFile
            print('>>Guardar la imagen procesada en un buffer y crear un ContentFile')
            buffer = BytesIO()
            canvas.save(buffer, format="PNG")
            processed_file = ContentFile(buffer.getvalue(), name=file.name)
            imagenes_procesadas.append(processed_file)
        
        return imagenes_procesadas, imagenes_base64
    
    def convert_to_base64(self, image_files):
        """
        Convierte una lista de archivos de imagen a base64.
        """
        result = []
        for file in image_files:
            img_base64 = pil_image_to_base64(Image.open(file).convert("RGB"))
            result.append(img_base64)
        return result