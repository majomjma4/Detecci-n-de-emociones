import cv2
import numpy as np

# Cargar modelo pre-entrenado (sin TensorFlow)
emotion_net = cv2.dnn.readNetFromONNX(
    "C:/ruta/a/tu/modelo/emotion-ferplus-8.onnx"
)

EMOTIONS = [
    "Neutral", "Feliz", "Triste", "Sorpresa",
    "Enojo", "Disgusto", "Miedo"
]

def detectar_emocion(face):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(face, (64, 64)),
        scalefactor=1/255.0,
        size=(64, 64),
        mean=(0, 0, 0),
        swapRB=True,
        crop=False
    )

    emotion_net.setInput(blob)
    preds = emotion_net.forward()

    idx = np.argmax(preds)
    return EMOTIONS[idx]
