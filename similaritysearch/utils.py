import base64
import cv2
import os

def calculate_average(values):
    """
    Calculates the average of an array of values.

    Parameters:
    values (list): List of numeric values.

    Returns:
    float: The average of the values.
    """
    if not values:
        return 0
    return float(sum(values) / len(values))

def calculate_statistics(values):
    """
    Calculates the mean, mode, and median of an array of numeric values.

    Parameters:
    values (list): List of numeric values.

    Returns:
    dict: Dictionary with 'mean', 'mode', and 'median'.
    """
    import statistics

    if not values:
        return {'mean': 0, 'mode': None, 'median': 0}

    mean = float(sum(values) / len(values))
    try:
        mode = float(statistics.mode(values))
    except statistics.StatisticsError:
        mode = None  # No unique mode
    median = float(statistics.median(values))

    return {'mean': mean, 'mode': mode, 'median': median, 'max': max(values)}

def image_to_base64(image):
    """
    Converts an OpenCV image to a base64 string.
    """
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

def get_diagnosis_message(percentage):
    """
    Returns a diagnostic message based on the similarity percentage.

    Parameters:
    percentage (float): Similarity percentage.

    Return:
    str: Diagnostic message.
    """
    if percentage >= 0.9:
        return "Alta probabilidad de coincidencia. Las características de la imagen analizada presentan una similitud significativa con patrones asociados a cáncer de estómago. Se recomienda una evaluación médica inmediata."
    elif percentage >= 0.7:
        return "Probabilidad moderada-alta de coincidencia. Las características de la imagen analizada muestran similitudes relevantes con patrones asociados a cáncer de estómago. Se sugiere un análisis médico detallado."
    elif percentage >= 0.5:
        return "Probabilidad moderada de coincidencia. Las características de la imagen analizada presentan similitudes parciales con patrones asociados a cáncer de estómago. Se recomienda un seguimiento clínico."
    elif percentage >= 0.3:
        return "Probabilidad baja de coincidencia. Las características de la imagen analizada muestran similitudes limitadas con patrones asociados a cáncer de estómago. Se sugiere monitoreo adicional si es necesario."
    return "Muy baja probabilidad de coincidencia. Las características de la imagen analizada no presentan similitudes significativas con patrones asociados a cáncer de estómago. Es poco probable que haya indicios relevantes en esta imagen."
