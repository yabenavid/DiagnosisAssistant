import base64
import cv2
from google.cloud import vision

def calculate_average(values):
    """
    Calcula el promedio de un array de valores.

    Parámetros:
    values (list): Lista de valores numéricos.

    Retorna:
    float: El promedio de los valores.
    """
    if not values:
        return 0
    return float(sum(values) / len(values))

def image_to_base64(image):
    """
    Convierte una imagen de OpenCV a una cadena base64.
    """
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

def get_diagnosis_message(percentage):
    """
    Retorna un mensaje de diagnóstico basado en el porcentaje de similitud.

    Parámetros:
    percentage (float): Porcentaje de similitud.

    Retorna:
    str: Mensaje de diagnóstico.
    """
    if percentage >= 0.9:
        return "¡Excelente! La similitud es muy alta."
    elif percentage >= 0.7:
        return "¡Muy bien! La similitud es alta."
    elif percentage >= 0.5:
        return "¡Bien! La similitud es moderada."
    elif percentage >= 0.3:
        return "¡Regular! La similitud es baja."
    return "¡Mal! La similitud es muy baja."

def analyze_image(image_path):
    print("Analyzing image...")
    print('image path: ' + image_path)
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    return [label.description for label in response.label_annotations]