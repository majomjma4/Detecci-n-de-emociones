import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from interfaz.ventana_camara import abrir_camara
from interfaz.ventana_galeria import ver_fotos
from interfaz.botones import crear_boton_redondo, dibujar_boton
from interfaz.utils_ui import centrar_ventana

# ---------------- VENTANA PRINCIPAL ----------------
root = tk.Tk()
root.title("Detección de Emociones en Tiempo Real")

BASE_W = 750
BASE_H = 500
centrar_ventana(root, BASE_W, BASE_H)
root.configure(bg="#CFEFFF")

# ---------------- ESTILOS ----------------
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Titulo.TLabel",
    background="#CFEFFF",
    foreground="#000000",
    font=("Arial", 24, "bold")
)

# ---------------- TÍTULO ----------------
titulo = ttk.Label(
    root,
    text="DETECCIÓN DE EMOCIONES EN TIEMPO REAL",
    style="Titulo.TLabel"
)
titulo.pack(pady=20)

linea = tk.Frame(root, bg="#03581E", height=3)
linea.pack(fill="x", padx=90, pady=(0, 10))

# ---------------- IMAGEN ----------------
IMG_BASE_W = 319
IMG_BASE_H = 270

ruta_imagen = "img/logo_DS.png"

frame_img = tk.Frame(root, bg="#CFEFFF")
frame_img.pack(pady=10)

label_img = tk.Label(frame_img, bg="#CFEFFF")
label_img.pack()

try:
    img_original = Image.open(ruta_imagen)
except:
    img_original = None

# ---------------- BOTONES ----------------
frame_botones = tk.Frame(root, bg="#CFEFFF")
frame_botones.pack(pady=20)

btn_iniciar = crear_boton_redondo(
    frame_botones,
    "INICIAR",
    "#69E991",
    "black",
    "#97E0AE",
    "#69B4F1",
    lambda: (root.withdraw(), abrir_camara(root))
)
btn_iniciar.pack(side="left", padx=10)
dibujar_boton(btn_iniciar, 1)

btn_galeria = crear_boton_redondo(
    frame_botones,
    "GALERÍA",
    "#69B4F1",
    "black",
    "#A2C2DD",
    "#69B4F1",
    lambda: (root.withdraw(), ver_fotos(root))
)
btn_galeria.pack(side="left", padx=10)
dibujar_boton(btn_galeria, 1)

# ---------------- RESPONSIVE ----------------
pending = None

def adaptar(event=None):
    global pending
    if pending:
        root.after_cancel(pending)
    pending = root.after(80, aplicar_cambios)

def aplicar_cambios():
    global pending
    pending = None

    w = root.winfo_width()
    h = root.winfo_height()

    escala = min(w / BASE_W, h / BASE_H)

    nueva_fuente = max(int(24 * escala), 10)
    style.configure("Titulo.TLabel", font=("Arial", nueva_fuente, "bold"))

    if img_original:
        new_w = int(IMG_BASE_W * escala)
        new_h = int(IMG_BASE_H * escala)
        img_resized = img_original.resize((new_w, new_h))
        tk_img = ImageTk.PhotoImage(img_resized)
        label_img.config(image=tk_img)
        label_img.image = tk_img

    dibujar_boton(btn_iniciar, escala)
    dibujar_boton(btn_galeria, escala)

root.bind("<Configure>", adaptar)

root.mainloop()