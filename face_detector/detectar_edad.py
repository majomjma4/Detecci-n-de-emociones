import cv2
import os

# Rangos de edad que devuelve el modelo
AGE_BUCKETS = [
    "(0-2)", "(4-6)", "(8-12)", "(15-20)",
    "(25-32)", "(38-43)", "(48-53)", "(60+)"
]

# Cargar modelo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta donde está este archivo
AGE_PROTO = os.path.join(BASE_DIR, "models", "age_deploy.prototxt")
AGE_MODEL = os.path.join(BASE_DIR, "models", "age_net.caffemodel")

age_net = cv2.dnn.readNetFromCaffe(AGE_PROTO, AGE_MODEL)

def detectar_edad(rostro):
    """
    rostro: imagen recortada del rostro (BGR)
    devuelve: rango de edad como string, ej: "25-32"
    """
    blob = cv2.dnn.blobFromImage(
        rostro,
        1.0,
        (227, 227),
        (78.4263377603, 87.7689143744, 114.895847746),
        swapRB=False
    )

    age_net.setInput(blob)
    preds = age_net.forward()
    return AGE_BUCKETS[preds[0].argmax()]
