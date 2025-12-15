import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os
import winsound
from interfaz.ventana_camara import abrir_camara
from interfaz.botones import crear_boton_redondo, dibujar_boton
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


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suprimir mensajes de TensorFlow


if not os.path.exists("Galeria"):
    os.makedirs("Galeria")

# ---------------- Galería de fotos ----------------
def ver_fotos():
    gal_window = tk.Toplevel()
    gal_window.title("Galería de Fotos")
    ancho, alto = 900, 650
    centrar_ventana(gal_window, ancho, alto)
    gal_window.configure(bg="white")

    # ---------------------- BARRA SUPERIOR ----------------------
    barra_superior = tk.Frame(gal_window, bg="#003B70", height=60)
    barra_superior.pack(fill="x", side="top")

    btn_regresar = tk.Button(
        barra_superior,
        text="⟵  Regresar",
        font=("Arial", 14, "bold"),
        bg="#003B70",
        fg="white",
        activebackground="#002F55",
        activeforeground="white",
        bd=0,
        command=lambda:[gal_window.destroy(), root.deiconify()]
    )
    btn_regresar.pack(side="left", padx=15, pady=10)

   # Frame central para EL TÍTULO
    frame_titulo = tk.Frame(barra_superior, bg="#003B70")
    frame_titulo.pack(expand=True, fill="both")

    titulo = tk.Label(
        frame_titulo,
        text="GALERÍA DE FOTOS",
        bg="#003B70",
        fg="white",
        font=("Arial", 18, "bold")
    )

    # Proporción inicial: 190 px / 900 px
    x_proporcion = 190 / 900
    titulo.place(x=int(x_proporcion * 900), rely=0.5, anchor="w")  # posición inicial

    # Función para actualizar posición al cambiar tamaño de la ventana
    def actualizar_posicion_titulo(event=None):
        ancho_actual = gal_window.winfo_width()  # ancho de la ventana
        x = int(x_proporcion * ancho_actual)
        titulo.place(x=x, rely=0.5, anchor="w")

    # Vincular al redimensionamiento de la ventana
    gal_window.bind("<Configure>", actualizar_posicion_titulo)

    # ---------------------- CANVAS CENTRAL ----------------------
    canvas_frame = tk.Frame(gal_window, bg="white")
    canvas_frame.pack(expand=True, fill="both")

    canvas = tk.Canvas(canvas_frame, bg="#F2F2F2", highlightthickness=0)
    canvas.pack(expand=True, fill="both", padx=20, pady=20)

    # Obtener fotos y ordenar cronológicamente
    fotos = sorted(os.listdir("Galeria"), reverse=True)  # última foto primero
    idx = [0]  # empezamos en la última foto tomada
    ultimo_tamano = {"w": 0, "h": 0}



    def mostrar_imagen():
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Evita redibujar si el tamaño no cambió
        if ultimo_tamano["w"] == w and ultimo_tamano["h"] == h:
            return

        ultimo_tamano["w"] = w
        ultimo_tamano["h"] = h

        canvas.delete("all")

        if fotos:
            foto_path = os.path.join("Galeria", fotos[idx[0]])
            img = Image.open(foto_path)

            # Ajustar imagen al tamaño del canvas
            # Tamaño disponible
            max_w = w - 20
            max_h = h - 20

            img_w, img_h = img.size
            ratio = min(max_w / img_w, max_h / img_h)

            new_size = (int(img_w * ratio), int(img_h * ratio))
            img = img.resize(new_size, Image.LANCZOS)

            imgtk = ImageTk.PhotoImage(img)

            canvas.imgtk = imgtk
            canvas.create_image(w // 2, h // 2, anchor="center", image=imgtk)
        else:
            canvas.create_text(
                w // 2,
                h // 2,
                text="No hay fotos guardadas",
                fill="#003B70",
                font=("Arial", 20, "bold")
            )

    # Botón Siguiente (ir a fotos más antiguas)
    def siguiente():
        if idx[0] < len(fotos) - 1:  # solo si no es la última foto antigua
            idx[0] += 1
            ultimo_tamano["w"] = 0
            ultimo_tamano["h"] = 0
            mostrar_imagen()

    # Botón Anterior (ir a fotos más recientes)
    def anterior():
        if idx[0] > 0:  # solo si no es la última foto reciente
            idx[0] -= 1
            ultimo_tamano["w"] = 0
            ultimo_tamano["h"] = 0
            mostrar_imagen()

    def borrar():
        if fotos:
            foto_path = os.path.join("Galeria", fotos[idx[0]])
            os.remove(foto_path)
            fotos.pop(idx[0])

            if idx[0] >= len(fotos):
                idx[0] = len(fotos) - 1

            # FORZAR REDIBUJO
            ultimo_tamano["w"] = 0
            ultimo_tamano["h"] = 0

            mostrar_imagen()
  

    def actualizar_botones():
        btn_prev.config(state="normal" if idx[0] > 0 else "disabled")
        btn_next.config(state="normal" if idx[0] < len(fotos) - 1 else "disabled")


    # ---------------------- BOTONES INFERIORES ----------------------
    barra_botones = tk.Frame(gal_window, bg="white")
    barra_botones.pack(side="bottom", pady=15)

    style = ttk.Style(gal_window)
    style.theme_use("clam")

    style = ttk.Style(gal_window)
    style.theme_use("clam")


    # ESTILOS PARA BOTONES
    style.configure("BotonAzul.TButton",
                    background="#319BF1",    
                    foreground="black",
                    font=("Arial", 13, "bold"),
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor='none',
                    padding=8)
    style.map("BotonAzul.TButton",
              background=[("active", "#75B3F1")],  
              foreground=[("active", "black")])

    style.configure("BotonVerde.TButton",
                    background="#58F389",    
                    foreground="black",
                    font=("Arial", 13, "bold"),
                    borderwidth=0,
                    padding=8)
    
    style.map("BotonVerde.TButton",
              background=[("active", "#7EE69D")],  
              foreground=[("active", "black")])

    # BOTONES
    btn_prev = ttk.Button(barra_botones, text="⟵ Anterior", style="BotonAzul.TButton", command=anterior)
    btn_prev.grid(row=0, column=0, padx=10)

    btn_next = ttk.Button(barra_botones, text="Siguiente ⟶", style="BotonAzul.TButton", command=siguiente)
    btn_next.grid(row=0, column=1, padx=10)

    btn_borrar = ttk.Button(barra_botones, text="🗑 Borrar Foto", style="BotonVerde.TButton", command=borrar)
    btn_borrar.grid(row=0, column=2, padx=10)

    canvas.bind("<Configure>", lambda e: mostrar_imagen())

    gal_window.after(100,mostrar_imagen)
    
    gal_window.protocol("WM_DELETE_WINDOW", lambda: root.destroy())


# ---------- VENTANA ----------
root = tk.Tk()
root.title("Detección de Emociones en Tiempo Real")

BASE_W = 750
BASE_H = 500
centrar_ventana(root, BASE_W, BASE_H)

# 🎨 FONDO SÓLIDO (ya no hay degradado)
root.configure(bg="#CFEFFF")

# ---------- ESTILOS ----------
style = ttk.Style()
style.theme_use("clam")
style.configure("Titulo.TLabel",
                background="#CFEFFF",
                foreground="#000000",
                font=("Arial", 24, "bold"))

# ---------- TÍTULO ----------
titulo = ttk.Label(root, text="DETECCIÓN DE EMOCIONES EN TIEMPO REAL",
                   style="Titulo.TLabel")
titulo.pack(pady=20)

# Línea decorativa
linea = tk.Frame(root, bg="#03581E", height=3)
linea.pack(fill="x", padx=90, pady=(0, 10))

# ---------- IMAGEN ----------
IMG_BASE_W = 319
IMG_BASE_H = 270

ruta_imagen = "C:/Users/marijo monteros/Desktop/Tercer Semestre/Proyecto Pis/Codigo_Pis/img/logo_DS.png"

frame_img = tk.Frame(root, bg="#CFEFFF")
frame_img.pack(pady=10)

try:
    img_original = Image.open(ruta_imagen)
except:
    img_original = None

label_img = tk.Label(frame_img, bg="#CFEFFF")
label_img.pack()

# ---------- BOTONES ----------
frame_botones = tk.Frame(root, bg="#CFEFFF")
frame_botones.pack(pady=20)

btn_iniciar = crear_boton_redondo(frame_botones, "INICIAR", "#69E991", "black", "#97E0AE", "#69B4F1",
                                  lambda: (root.withdraw(), abrir_camara(root)))
                                                        
btn_iniciar.pack(side="left", padx=10)
dibujar_boton(btn_iniciar, 1)

btn_galeria = crear_boton_redondo(frame_botones, "GALERÍA", "#69B4F1", "black", "#A2C2DD", "#69B4F1",
                                  lambda: (root.withdraw(), ver_fotos()))
btn_galeria.pack(side="left", padx=10)
dibujar_boton(btn_galeria,1)


# ---------- RESPONSIVE OPTIMIZADO ----------
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

    escala_w = w / BASE_W
    escala_h = h / BASE_H
    escala = min(escala_w, escala_h)

    # Título
    nueva_fuente = int(24 * escala)
    if nueva_fuente < 10:
        nueva_fuente = 10
    style.configure("Titulo.TLabel", font=("Arial", nueva_fuente, "bold"))

    # Imagen
    if img_original:
        new_w = int(IMG_BASE_W * escala)
        new_h = int(IMG_BASE_H * escala)
        img_resized = img_original.resize((new_w, new_h))
        tk_img = ImageTk.PhotoImage(img_resized)
        label_img.config(image=tk_img)
        label_img.image = tk_img

    # Botones redondos
    dibujar_boton(btn_iniciar, escala)
    dibujar_boton(btn_galeria, escala)

root.bind("<Configure>", adaptar)


root.mainloop()