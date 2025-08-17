# vectorization/utils.py
import base64
from io import BytesIO
from PIL import Image

def pil_image_to_base64(pil_image, format='PNG'):
    """
    Converts a PIL image to base64 without prefix
    Args:
        pil_image: Image in PIL.Image format
        format: Image format (PNG by default)
    Returns:
        str: Base64 string without prefix
    """
    buffered = BytesIO()
    pil_image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')