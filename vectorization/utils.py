# vectorization/utils.py
import base64
from io import BytesIO
from PIL import Image

def pil_image_to_base64(pil_image, format='PNG'):
    """
    Convierte una imagen PIL a base64 con prefijo data URL
    Args:
        pil_image: Imagen en formato PIL.Image
        format: Formato de imagen (PNG por defecto)
    Returns:
        str: Cadena base64 con prefijo (ej: "data:image/png;base64,...")
    """
    buffered = BytesIO()
    pil_image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/{format.lower()};base64,{img_str}"