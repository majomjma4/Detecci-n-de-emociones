import cv2
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import os
import winsound

from detectar_caras import detectar_caras
from detectar_emociones import detectar_emocion
from detectar_genero import detectar_genero
from detectar_edad import detectar_edad

from interfaz.utils_ui import (
    centrar_ventana,
    texto_con_fondo,
    mostrar_mensaje,
    emociones_es
)
