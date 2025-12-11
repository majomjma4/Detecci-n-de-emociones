import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
from detectar_caras import detectar_caras
from detectar_emociones import detectar_emocion
import os

# Diccionario de traducción
emociones_es = {
    "anger": "Enojado",
    "disgust": "Disgustado",
    "fear": "Asustado",
    "happiness": "Feliz",
    "neutral": "Neutral",
    "sadness": "Triste",
    "surprise": "Sorprendido"
}

# Carpeta para guardar fotos
if not os.path.exists("Galeria"):
    os.makedirs("Galeria")

# ---------------- Función para ventana principal ----------------
def mostrar_inicio():
    root.deiconify()   

# ---------------- Función para centrar ventana ----------------
def centrar_ventana(win, ancho, alto):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - ancho) / 2)
    y = int((screen_h - alto) / 2)
    win.geometry(f"{ancho}x{alto}+{x}+{y}")

# ---------------- Ventana de cámara ----------------
def abrir_camara():
    cam_window = tk.Toplevel()
    cam_window.title("Cámara - Detección de Emociones")
    ancho, alto = 800, 600
    centrar_ventana(cam_window, ancho, alto)
    
    canvas = tk.Canvas(cam_window, bg="black")
    canvas.pack(fill="both", expand=True)

    # Función para cerrar cámara
    def detener():
        cap.release()
        cam_window.destroy()
        mostrar_inicio()

    # Función para tomar foto
    def tomar_foto():
        if frame_global is not None:
            frame_guardar = frame_global.copy()
            faces = detectar_caras(frame_guardar)
            for (x, y, w_face, h_face) in faces:
                rostro = frame_guardar[y:y+h_face, x:x+w_face]
                emotion = detectar_emocion(rostro)
                emotion_str = str(emotion).lower()
                emotion_es = emociones_es.get(emotion_str, "Desconocido")
                cv2.rectangle(frame_guardar, (x, y), (x+w_face, y+h_face), (0, 255, 0), 2)
                cv2.putText(frame_guardar, emotion_es, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Galeria/foto_{timestamp}.png"
            cv2.imwrite(filename, cv2.cvtColor(frame_guardar, cv2.COLOR_RGB2BGR))
            print(f"Foto guardada en {filename}")

    # Barra superior de botones
    barra = tk.Frame(cam_window, bg="#000000", height=40)
    barra.place(relx=0, rely=0, relwidth=1)
    btn_detener = ttk.Button(barra, text="Detener Cámara", command=detener)
    btn_detener.pack(side="left", padx=5)
    btn_foto = ttk.Button(barra, text="Tomar Foto", command=tomar_foto)
    btn_foto.pack(side="left", padx=5)

    cap = cv2.VideoCapture(0)
    frame_global = None

    def mostrar_frame():
        nonlocal frame_global
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_global = frame_rgb.copy()

            faces = detectar_caras(frame_rgb)
            for (x, y, w_face, h_face) in faces:
                rostro = frame_rgb[y:y+h_face, x:x+w_face]
                emotion = detectar_emocion(rostro)
                emotion_str = str(emotion).lower()
                emotion_es = emociones_es.get(emotion_str, "Desconocido")
                cv2.rectangle(frame_rgb, (x, y), (x+w_face, y+h_face), (0, 255, 0), 2)
                cv2.putText(frame_rgb, emotion_es, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Ajustar a tamaño del canvas
            canvas_w = canvas.winfo_width()
            canvas_h = canvas.winfo_height()
            frame_rgb_resized = cv2.resize(frame_rgb, (canvas_w, canvas_h))
            img = Image.fromarray(frame_rgb_resized)
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.imgtk = imgtk
            canvas.create_image(0, 0, anchor="nw", image=imgtk)

        canvas.after(10, mostrar_frame)

    mostrar_frame()

# ---------------- Galería de fotos ----------------
def ver_fotos():
    gal_window = tk.Toplevel()
    gal_window.title("Galería de Fotos")
    ancho, alto = 800, 600
    centrar_ventana(gal_window, ancho, alto)

    canvas = tk.Canvas(gal_window, bg="gray")
    canvas.pack(fill="both", expand=True)

    fotos = sorted(os.listdir("Galeria"))
    idx = [0]  # índice actual

    def mostrar_imagen():
        canvas.delete("all")
        if fotos:
            foto_path = os.path.join("Galeria", fotos[idx[0]])
            img = Image.open(foto_path)
            img.thumbnail((gal_window.winfo_width(), gal_window.winfo_height()))
            imgtk = ImageTk.PhotoImage(img)
            canvas.imgtk = imgtk
            canvas.create_image(gal_window.winfo_width()//2, gal_window.winfo_height()//2,
                                anchor="center", image=imgtk)
        else:
            label = ttk.Label(canvas, text="No hay fotos guardadas aún")
            label.pack(pady=20)

    def siguiente():
        if fotos:
            idx[0] = (idx[0] + 1) % len(fotos)
            mostrar_imagen()

    def anterior():
        if fotos:
            idx[0] = (idx[0] - 1) % len(fotos)
            mostrar_imagen()

    def borrar():
        if fotos:
            foto_path = os.path.join("Galeria", fotos[idx[0]])
            os.remove(foto_path)
            print(f"Foto {fotos[idx[0]]} borrada")
            fotos.pop(idx[0])
            if idx[0] >= len(fotos):
                idx[0] = len(fotos) - 1
            mostrar_imagen()

    def regresar():
        gal_window.destroy()
        mostrar_inicio()

    # Botones
    barra = tk.Frame(gal_window, bg="#000000", height=40)
    barra.pack(side="bottom", fill="x")
    btn_prev = ttk.Button(barra, text="Anterior", command=anterior)
    btn_prev.pack(side="left", padx=5, pady=5)
    btn_next = ttk.Button(barra, text="Siguiente", command=siguiente)
    btn_next.pack(side="left", padx=5, pady=5)
    btn_borrar = ttk.Button(barra, text="Borrar Foto", command=borrar)
    btn_borrar.pack(side="left", padx=5, pady=5)
    btn_regresar = ttk.Button(barra, text="Regresar", command=regresar)
    btn_regresar.pack(side="right", padx=5, pady=5)

    mostrar_imagen()

# ---------------- Ventana inicial ----------------
root = tk.Tk()
centrar_ventana(root, 750, 500)
root.title("Detección de Emociones en Tiempo Real")
root.configure(bg="white")

# Permitir que la ventana sea responsive
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=3)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

# ---------- ESTILOS ----------
style = ttk.Style()
style.theme_use("clam")

style.configure("Titulo.TLabel",
                background="white",
                foreground="#003B70",
                font=("Arial", 24, "bold"),
                anchor="center")  

style.configure("BotonVerde.TButton",
                font=("Arial", 14, "bold"),
                foreground="white",
                padding=10)

style.map("BotonVerde.TButton",
          background=[("!active", "#1B7F3A"), ("active", "#166b30")])

style.configure("BotonAzul.TButton",
                font=("Arial", 14, "bold"),
                foreground="white",
                padding=10)

style.map("BotonAzul.TButton",
          background=[("!active", "#004C89"), ("active", "#003B70")])

# ---------- TÍTULO ----------
titulo = ttk.Label(root,
                   text="DETECCIÓN DE EMOCIONES EN TIEMPO REAL",
                   style="Titulo.TLabel")
titulo.grid(row=0, column=0, pady=20, sticky="n")

# ---------- IMAGEN CENTRAL ----------
IMG_ANCHO = 319  
IMG_ALTO = 270    

ruta_imagen = "C:/Users/marijo monteros/Desktop/Tercer Semestre/Proyecto PIS/Codigo_Pis/img/logo_DS.jpg"

frame_img = tk.Frame(root, bg="white")
frame_img.grid(row=1, column=0, sticky="n", pady=10)

try:
    img = Image.open(ruta_imagen)
    img = img.resize((IMG_ANCHO, IMG_ALTO)) 
    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(frame_img, image=img_tk, bg="white")
    label_img.pack()
except:
    label_img = tk.Label(frame_img,
                         text="(Aquí se mostrará tu imagen)",
                         bg="white",
                         fg="#003B70",
                         font=("Arial", 12))
    label_img.pack()

# ---------- BOTONES ----------
frame_botones = tk.Frame(root, bg="white")
frame_botones.grid(row=2, column=0, pady=20)

btn_iniciar = ttk.Button(frame_botones, text="INICIAR",
                         style="BotonVerde.TButton",
                         command=lambda:[root.withdraw(),abrir_camara()])

btn_iniciar.grid(row=0, column=0, padx=30)

btn_galeria = ttk.Button(frame_botones, text="GALERÍA",
                         style="BotonAzul.TButton",
                         command=lambda:[root.withdraw(),ver_fotos()])

btn_galeria.grid(row=0, column=1, padx=30)



root.mainloop()