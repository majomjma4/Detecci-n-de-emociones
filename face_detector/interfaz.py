
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
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
    cam_window.configure(bg="#001C33")   # Azul oscuro elegante

    # --- Canvas donde va el video ---
    canvas = tk.Canvas(cam_window, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # --- Frame flotante superior (botón de regresar) ---
    barra_superior = tk.Frame(cam_window, bg="#003B70", height=45)
    barra_superior.place(relx=0, rely=0, relwidth=1)

    btn_regresar = tk.Button(
        barra_superior,
        text="⟵",
        font=("Arial", 18, "bold"),
        bg="#003B70",
        fg="white",
        bd=0,
        activebackground="#002F55",
        activeforeground="white",
        command=lambda:[cap.release(), cam_window.destroy(), mostrar_inicio()]
    )
    btn_regresar.pack(side="left", padx=10)

    # --- Frame flotante inferior para botón de foto ---
    barra_inferior = tk.Frame(cam_window, bg="#000000", height=80)
    barra_inferior.place(relx=0.5, rely=0.92, anchor="center")

    # Botón estilo cámara
    
    icono_img = Image.open("C:/Users/marijo monteros/Desktop/Tercer Semestre/Proyecto PIS/CODIGO_PIS/img/icono_camar.webp")  
    icono_img = icono_img.resize((60, 60))         
    icono = ImageTk.PhotoImage(icono_img)

    # --- Canvas que simula botón redondo ---
    btn_foto = tk.Canvas(barra_inferior, width=80, height=80, bg="#000000", highlightthickness=0)
    btn_foto.pack()

    # Dibujar círculo
    circulo = btn_foto.create_oval(5, 5, 75, 75, fill="#F0EBEB", outline="#ffffff", width=2)

    # Colocar icono en el centro
    icono_id = btn_foto.create_image(40, 40, image=icono)

    # Función clic
    def click_btn(event):
        tomar_foto()

    btn_foto.tag_bind(circulo, "<Button-1>", click_btn)
    btn_foto.tag_bind(icono_id, "<Button-1>", click_btn)

    # Evitar que la imagen se borre por garbage collector
    btn_foto.image = icono

    btn_foto.pack()

    # --- VARIABLES ---
    cap = cv2.VideoCapture(0)
    frame_global = None

    # --- FUNCIONES INTERNAS ---
    def tomar_foto():
        if frame_global is not None:
            frame_guardar = frame_global.copy()
            faces = detectar_caras(frame_guardar)
            for (x, y, w_face, h_face) in faces:
                rostro = frame_guardar[y:y+h_face, x:x+w_face]
                emotion = detectar_emocion(rostro)
                emotion_es = emociones_es.get(str(emotion).lower(), "Desconocido")
                cv2.rectangle(frame_guardar, (x, y), (x+w_face, y+h_face), (0,255,0), 2)
                cv2.putText(frame_guardar, emotion_es, (x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Galeria/foto_{timestamp}.png"
            cv2.imwrite(filename, cv2.cvtColor(frame_guardar, cv2.COLOR_RGB2BGR))

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
                emotion_es = emociones_es.get(str(emotion).lower(), "Desconocido")
                cv2.rectangle(frame_rgb, (x,y), (x+w_face, y+h_face), (0,255,0), 2)
                cv2.putText(frame_rgb, emotion_es, (x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

            # Render al canvas
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            frame_resized = cv2.resize(frame_rgb, (w, h))
            img = Image.fromarray(frame_resized)
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.imgtk = imgtk
            canvas.create_image(0, 0, anchor="nw", image=imgtk)

        canvas.after(10, mostrar_frame)

    mostrar_frame()

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
        command=lambda:[gal_window.destroy(), mostrar_inicio()]
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
    titulo.pack(expand=True)


    # ---------------------- CANVAS CENTRAL ----------------------
    canvas_frame = tk.Frame(gal_window, bg="white")
    canvas_frame.pack(expand=True, fill="both")

    canvas = tk.Canvas(canvas_frame, bg="#F2F2F2", highlightthickness=0)
    canvas.pack(expand=True, fill="both", padx=20, pady=20)

    fotos = sorted(os.listdir("Galeria"))
    idx = [0]

    def mostrar_imagen():
        canvas.delete("all")
        if fotos:
            foto_path = os.path.join("Galeria", fotos[idx[0]])
            img = Image.open(foto_path)
            img.thumbnail((gal_window.winfo_width()-100, gal_window.winfo_height()-150))
            imgtk = ImageTk.PhotoImage(img)

            def mostrar_texto_centrado():
                canvas.delete("all")
                canvas.create_text(
                    canvas.winfo_width()//2,
                    canvas.winfo_height()//2,
                    text="No hay fotos guardadas",
                    fill="#003B70",
                    font=("Arial", 20, "bold")
                )

            canvas.after(50, mostrar_texto_centrado)

        else:
            canvas.create_text(
                canvas.winfo_width()//2,
                canvas.winfo_height()//2,
                text="No hay fotos guardadas",
                fill="#003B70",
                font=("Arial", 20, "bold")
            )

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
            fotos.pop(idx[0])

            if idx[0] >= len(fotos):
                idx[0] = len(fotos) - 1

            mostrar_imagen()

    # ---------------------- BOTONES INFERIORES ----------------------
    barra_botones = tk.Frame(gal_window, bg="white")
    barra_botones.pack(side="bottom", pady=10)

    estilo_btn = {
        "font": ("Arial", 13, "bold"),
        "width": 14,
        "padding": 10
    }

    btn_prev = ttk.Button(barra_botones, text="⟵ Anterior", style="BotonAzul.TButton", command=anterior)
    btn_prev.grid(row=0, column=0, padx=10)

    btn_next = ttk.Button(barra_botones, text="Siguiente ⟶", style="BotonAzul.TButton", command=siguiente)
    btn_next.grid(row=0, column=1, padx=10)

    btn_borrar = ttk.Button(barra_botones, text="🗑 Borrar Foto", style="BotonVerde.TButton", command=borrar)
    btn_borrar.grid(row=0, column=2, padx=10)

    mostrar_imagen()


# ---------------- Ventana inicial ----------------
root = tk.Tk()
root.title("Detección de Emociones en Tiempo Real")
centrar_ventana(root, 750, 500)

# Configuración de filas y columnas para centrar y hacer responsive
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
root.rowconfigure(2, weight=3)
root.rowconfigure(3, weight=1)
root.columnconfigure(0, weight=1)

root.configure(bg="white")

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
                padding=10,
                borderwidth=1,
                relief="raised")

style.map("BotonVerde.TButton",
          background=[("!active", "#1B7F3A"), ("active", "#166b30")])

style.configure("BotonAzul.TButton",
                font=("Arial", 14, "bold"),
                foreground="white",
                padding=10,
                borderwidth=1,
                relief="raised")

style.map("BotonAzul.TButton",
          background=[("!active", "#004C89"), ("active", "#003B70")])

# ---------- TÍTULO ----------
titulo = ttk.Label(root,
                   text="DETECCIÓN DE EMOCIONES EN TIEMPO REAL",
                   style="Titulo.TLabel")
titulo.grid(row=0, column=0, pady=(20,5), sticky="n")

# Línea debajo del título
linea = tk.Frame(root, bg="#1B7F3A", height=2, width=500)
linea.grid(row=0, column=0, pady=(55,0))

# ---------- IMAGEN CENTRAL ----------
IMG_ANCHO = 319  
IMG_ALTO = 270    
ruta_imagen = "C:/Users/marijo monteros/Desktop/Tercer Semestre/Proyecto PIS/CODIGO_PIS/img/logo_DS.jpg"

frame_img = tk.Frame(root, bg="white")
frame_img.grid(row=1, column=0, pady=(30,10))

try:
    img = Image.open(ruta_imagen)
    img = img.resize((IMG_ANCHO, IMG_ALTO)) 
    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(frame_img, image=img_tk, bg="white")
    label_img.pack(expand=True)
except:
    label_img = tk.Label(frame_img,
                         text="(Aquí se mostrará tu imagen)",
                         bg="white",
                         fg="#003B70",
                         font=("Arial", 12))
    label_img.pack(expand=True)

def crear_boton_redondo(frame, texto, color_fondo, color_texto, comando):
    # Tamaño del botón
    ancho, alto = 150, 50
    # Crear imagen transparente
    img = Image.new("RGBA", (ancho, alto), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Dibujar rectángulo redondeado
    draw.rounded_rectangle((0, 0, ancho, alto), radius=15, fill=color_fondo)
    imgtk = ImageTk.PhotoImage(img)

    # Crear botón con imagen
    btn = tk.Button(frame, image=imgtk, text=texto, compound="center",
                    font=("Arial",14,"bold"), fg=color_texto, bd=0,
                    activebackground=color_fondo,
                    command=comando)
    btn.image = imgtk  # Evitar que lo borre el garbage collector
    return btn

# Reemplazar frame de botones
frame_botones = tk.Frame(root, bg="white")
frame_botones.grid(row=2, column=0, pady=20)

# Crear botones redondeados
btn_iniciar = crear_boton_redondo(frame_botones, "INICIAR", "#1B7F3A", "white",
                                  lambda:[root.withdraw(), abrir_camara()])
btn_iniciar.pack(side="left", padx=30)

btn_galeria = crear_boton_redondo(frame_botones, "GALERÍA", "#004C89", "white",
                                  lambda:[root.withdraw(), ver_fotos()])
btn_galeria.pack(side="left", padx=30)

root.mainloop()