import cv2
import numpy as np
from keras.models import load_model
from pathlib import Path

# ORDEN CORRECTO DEL MODELO
GENERO_LABELS = ["Masculino", "Femenino"]

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "gender_mini_XCEPTION.21-0.95.hdf5"

genero_model = load_model(MODEL_PATH, compile=False)

def detectar_genero(face_img):
    try:
        # ✅ face_img YA VIENE EN RGB
        gray = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)

        # Tamaño correcto del modelo
        gray = cv2.resize(gray, (64, 64))

        # Normalizar
        gray = gray.astype("float32") / 255.0

        # (1, 64, 64, 1)
        gray = np.expand_dims(gray, axis=-1)
        gray = np.expand_dims(gray, axis=0)

        preds = genero_model.predict(gray, verbose=0)[0]

        print("Pred:", preds)


        genero_idx = np.argmax(preds)
        genero = GENERO_LABELS[genero_idx]

        return genero

    except Exception as e:
        print("Error en detectar_genero:", e)
        return "Desconocido"
