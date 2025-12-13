import os
import cv2
import numpy as np
from keras.models import load_model

# Etiquetas del modelo
GENERO_LABELS = ["Femenino", "Masculino"]

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "gender_mini_XCEPTION.21-0.95.hdf5"

print("MODEL PATH:", MODEL_PATH)


genero_model = load_model(MODEL_PATH, compile=False)

# ===============================
# Función de predicción
# ===============================
def detectar_genero(face_img):

    try:
        # Convertir a escala de grises
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

        # Redimensionar a 64x64 (Mini-XCEPTION)
        gray = cv2.resize(gray, (64, 64))

        # Normalizar
        gray = gray.astype("float32") / 255.0

        # Ajustar dimensiones (1, 64, 64, 1)
        gray = np.expand_dims(gray, axis=-1)
        gray = np.expand_dims(gray, axis=0)

        # Predicción
        preds = genero_model.predict(gray, verbose=0)
        genero_idx = np.argmax(preds)

        return GENERO_LABELS[genero_idx]

    except Exception as e:
        print("Error en detectar_genero:", e)
        return "Desconocido"

