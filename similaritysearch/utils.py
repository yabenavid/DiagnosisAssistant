import base64
import cv2
import os
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
        return "Diagnóstico: Alta probabilidad de coincidencia. Las características de la imagen analizada presentan una similitud significativa con patrones asociados a cáncer de estómago. Se recomienda una evaluación médica inmediata."
    elif percentage >= 0.7:
        return "Diagnóstico: Probabilidad moderada-alta de coincidencia. Las características de la imagen analizada muestran similitudes relevantes con patrones asociados a cáncer de estómago. Se sugiere un análisis médico detallado."
    elif percentage >= 0.5:
        return "Diagnóstico: Probabilidad moderada de coincidencia. Las características de la imagen analizada presentan similitudes parciales con patrones asociados a cáncer de estómago. Se recomienda un seguimiento clínico."
    elif percentage >= 0.3:
        return "Diagnóstico: Probabilidad baja de coincidencia. Las características de la imagen analizada muestran similitudes limitadas con patrones asociados a cáncer de estómago. Se sugiere monitoreo adicional si es necesario."
    return "Diagnóstico: Muy baja probabilidad de coincidencia. Las características de la imagen analizada no presentan similitudes significativas con patrones asociados a cáncer de estómago. Es poco probable que haya indicios relevantes en esta imagen."

def analyze_image(image_path):

    # Ruta al archivo JSON con tus credenciales
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/yefer/OneDrive/Escritorio/DiagnosisAssistant/oncojuntas-8910822da3bd.json"

    print("Analyzing image...")
    print('image path: ' + image_path)

    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    return [label.description for label in response.label_annotations]

CANCER_KEYWORDS = [
    "cancer", "stomach cancer", "gastric cancer", "tumor", "carcinoma",
    "ulcer", "abnormal tissue", "lesion", "malignant", "neoplasm", "biopsy"
]


def analyze_image2(image_path, porcentaje_minimo=0.75):
    """
    Analiza una imagen usando Google Cloud Vision y evalúa si hay probabilidad
    de cáncer de estómago según las etiquetas detectadas y su score.

    :param image_path: Ruta al archivo de imagen.
    :param porcentaje_minimo: Umbral mínimo de score (entre 0 y 1).
    :return: Diccionario con diagnóstico y detalles de las etiquetas.
    """
    print("Analizando imagen...")
    print(f"Ruta: {image_path} | Umbral mínimo: {porcentaje_minimo}")
    
    # Ruta al archivo JSON con tus credenciales
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/yefer/OneDrive/Escritorio/DiagnosisAssistant/oncojuntas-8910822da3bd.json"
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    probable = False
    matched_labels = []

    for label in response.label_annotations:
        desc = label.description.lower()
        score = label.score

        # Revisamos si la descripción contiene alguna palabra clave
        if any(keyword in desc for keyword in CANCER_KEYWORDS):
            matched_labels.append({
                "descripcion": label.description,
                "score": round(score * 100, 2)
            })
            if score >= porcentaje_minimo:
                probable = True

    resultado = {
        "diagnostico": "Alta probabilidad de cáncer de estómago" if probable else "Baja probabilidad",
        "coincidencias": matched_labels,
        "umbral_usado": round(porcentaje_minimo * 100, 2)
    }

    return resultado
