import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
from detectar_caras import detectar_caras
from detectar_emociones import detectar_emocion
from detectar_genero import detectar_genero 
import os
import winsound

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
    cam_window.configure(bg="#001C33")

    # Canvas principal
    canvas = tk.Canvas(cam_window, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Barra superior
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
        command=lambda:[cap.release(), cam_window.destroy(), root.deiconify()]
    )
    btn_regresar.pack(side="left", padx=10)

    # Barra inferior con botón de foto
    barra_inferior = tk.Frame(cam_window, bg="#000000", height=80)
    barra_inferior.place(relx=0.5, rely=0.92, anchor="center")

    icono_img = Image.open("C:/Users/josue/Desktop/Tercero/Proyecto Pis/emociones2/Detecci-n-de-emociones/img/icono_camar.webp")
    icono_img = icono_img.resize((60, 60))
    icono = ImageTk.PhotoImage(icono_img)

    btn_foto = tk.Canvas(barra_inferior, width=80, height=80, bg="#000000", highlightthickness=0)
    btn_foto.pack()
    circulo = btn_foto.create_oval(5,5,75,75, fill="#F0EBEB", outline="#ffffff", width=2)
    icono_id = btn_foto.create_image(40,40, image=icono)

    def click_btn(event):
        tomar_foto()
    btn_foto.tag_bind(circulo, "<Button-1>", click_btn)
    btn_foto.tag_bind(icono_id, "<Button-1>", click_btn)
    btn_foto.image = icono

    # Barra lateral derecha
    barra_genero = tk.Frame(cam_window, bg="#003B70", width=220)
    barra_genero.place(relx=1, rely=0, anchor="ne", relheight=1)

    titulo_genero = tk.Label(
        barra_genero,
        text="DETECTAR GÉNERO:",
        bg="#003B70",
        fg="white",
        font=("Arial", 12, "bold")
    )
    titulo_genero.pack(pady=(60, 15))

    btn_genero = tk.Label(
        barra_genero,
        text="DESACTIVADO",
        bg="#B00020",
        fg="white",
        font=("Arial", 11, "bold"),
        width=14,
        height=2,
        cursor="hand2"
    )
    btn_genero.pack()

    # -------------función para Activa/Desactivar ------------

    def toggle_genero(event=None):
        nonlocal detectar_genero_activo
        detectar_genero_activo = not detectar_genero_activo

        if detectar_genero_activo:
            btn_genero.config(text="ACTIVADO", bg="#1FAA00")
        else:
            btn_genero.config(text="DESACTIVADO", bg="#B00020")

    btn_genero.bind("<Button-1>", toggle_genero)



    # Variables
    cap = cv2.VideoCapture(0)
    frame_global = None

    # Tomar foto
    def tomar_foto():
        if frame_global is not None:
            frame_guardar = frame_global.copy()
            faces = detectar_caras(frame_guardar)
            for (x, y, w_face, h_face) in faces:
                rostro = frame_guardar[y:y+h_face, x:x+w_face]

                # --- EMOCIÓN (SIEMPRE) ---
                emotion = detectar_emocion(rostro)
                emotion_es = emociones_es.get(str(emotion).lower(), "Desconocido")

                cv2.rectangle(frame_guardar, (x, y), (x+w_face, y+h_face), (0,255,0), 2)

                cv2.putText(
                    frame_guardar,
                    emotion_es,
                    (x, y - 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0,255,0),
                    2
                )

                # --- GÉNERO (SOLO SI ESTÁ ACTIVADO) ---
                if detectar_genero_activo:
                    genero = detectar_genero(rostro)
                    cv2.putText(
                        frame_guardar,
                        genero,
                        (x, y + h_face + 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,255,0),
                        2
                    )

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Galeria/foto_{timestamp}.png"
            cv2.imwrite(filename, cv2.cvtColor(frame_guardar, cv2.COLOR_RGB2BGR))

            mostrar_mensaje(cam_window, "Foto guardada")
            winsound.PlaySound("C:/Users/josue/Desktop/Tercero/Proyecto Pis/emociones2/Detecci-n-de-emociones/sound/A-modern-camera-shutter-click.wav",
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
            

    # Activador de la función género

    detectar_genero_activo = False


    # Mostrar frame
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
                cv2.rectangle(frame_rgb, (x, y), (x+w_face, y+h_face), (0,255,0), 2)
                cv2.putText(frame_rgb, emotion_es, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                
                # --- GÉNERO (SOLO SI ESTÁ ACTIVADO) ---
                if detectar_genero_activo:
                    genero = detectar_genero(rostro)
                    cv2.putText(
                        frame_rgb,
                        genero,
                        (x, y + h_face + 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0,255,0),
                        2
                    )

            # Escalar proporcionalmente solo dentro de la zona izquierda (70% ancho)
            canvas_w, canvas_h = canvas.winfo_width(), canvas.winfo_height()
            if canvas_w < 1 or canvas_h < 1:
                # Esperar un poco hasta que el canvas tenga tamaño válido
                cam_window.after(50, mostrar_frame)
                return

            video_w = int(canvas_w * 0.7)  
            frame_h, frame_w = frame_rgb.shape[:2]
            scale = min(canvas_w/frame_w, canvas_h/frame_h)
            new_w, new_h = max(1,int(frame_w*scale)), max(1,int(frame_h*scale))  # evitar cero
            frame_resized = cv2.resize(frame_rgb, (new_w, new_h))


            img = Image.fromarray(frame_resized)
            imgtk = ImageTk.PhotoImage(img)
            canvas.imgtk = imgtk

            # Limpiar canvas y centrar
            canvas.delete("VIDEO")
            canvas.create_image(canvas_w//2, canvas_h//2, image=imgtk, anchor="center", tags="VIDEO")

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
    titulo.pack(expand=True)

    # ---------------------- CANVAS CENTRAL ----------------------
    canvas_frame = tk.Frame(gal_window, bg="white")
    canvas_frame.pack(expand=True, fill="both")

    canvas = tk.Canvas(canvas_frame, bg="#F2F2F2", highlightthickness=0)
    canvas.pack(expand=True, fill="both", padx=20, pady=20)

    fotos = sorted(os.listdir("Galeria"))
    idx = [0]
    ultimo_tamano = {"w": 0, "h": 0}

    # Mostrar la última foto por defecto al abrir la galería
    if fotos:
        idx[0] = len(fotos) - 1

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

            # FORZAR REDIBUJO
            ultimo_tamano["w"] = 0
            ultimo_tamano["h"] = 0

            mostrar_imagen()


    # ---------------------- BOTONES INFERIORES ----------------------
    barra_botones = tk.Frame(gal_window, bg="white")
    barra_botones.pack(side="bottom", pady=15)

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


# ---------- FUNCIONES ----------
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_mensaje(cam_window, texto, duracion=10000):
    mensaje = tk.Label(cam_window, text=texto,
                       bg="#7BC0D9", fg="black",
                       font=("Arial", 14, "bold"),
                       bd=2, relief="solid", padx=10, pady=5)
    
    mensaje.place(x=10, y=10)  

    def posicionar():
        # Actualizar dimensiones reales
        mensaje.update_idletasks()
        ventana_h = cam_window.winfo_height()
        label_h = mensaje.winfo_height()
        mensaje.place(x=10, y=ventana_h - label_h - 10)

    # Llamar a posicionar después de 50 ms
    cam_window.after(50, posicionar)

    # Destruir después de duracion
    cam_window.after(duracion, mensaje.destroy)


# Aclarar/oscurecer color
def shade_color(color, factor):
    color = color.lstrip('#')
    r = int(color[0:2],16)
    g = int(color[2:4],16)
    b = int(color[4:6],16)
    r = min(int(r*factor),255)
    g = min(int(g*factor),255)
    b = min(int(b*factor),255)
    return f"#{r:02x}{g:02x}{b:02x}"

# ---------- BOTÓN REDONDO ----------
def crear_boton_redondo(parent, texto, bg_color, fg_color,
                        hover_color, active_color, comando):

    canvas = tk.Canvas(parent, highlightthickness=0, bg=parent["bg"], bd=0)

    canvas.texto = texto
    canvas.color_bg = bg_color
    canvas.color_fg = fg_color
    canvas.comando = comando

    # 🎨 colores hover / click
    canvas.hover_bg = hover_color
    canvas.active_bg = active_color

    # Estado actual
    canvas.current_bg = bg_color

    # -------- EVENTOS --------
    def on_enter(e):
        canvas.current_bg = canvas.hover_bg
        dibujar_boton(canvas, 1)

    def on_leave(e):
        canvas.current_bg = canvas.color_bg
        dibujar_boton(canvas, 1)

    def on_click(e):
        canvas.current_bg = canvas.active_bg
        dibujar_boton(canvas, 1)
        canvas.comando()

    def on_release(e):
        canvas.current_bg = canvas.hover_bg
        dibujar_boton(canvas, 1)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<ButtonRelease-1>", on_release)

    return canvas

def dibujar_boton(canvas, escala):
    canvas.delete("all")

    ancho = int(140 * escala)
    alto = int(50 * escala)
    radio = int(20 * escala)
    fuente = int(14 * escala)

    canvas.config(width=ancho, height=alto)

    x0, y0, x1, y1 = 0, 0, ancho, alto
    color = canvas.current_bg

    canvas.create_rectangle(x0+radio, y0, x1-radio, y1, fill=color, outline="")
    canvas.create_rectangle(x0, y0+radio, x1, y1-radio, fill=color, outline="")
    canvas.create_oval(x0, y0, x0+2*radio, y0+2*radio, fill=color, outline="")
    canvas.create_oval(x1-2*radio, y0, x1, y0+2*radio, fill=color, outline="")
    canvas.create_oval(x0, y1-2*radio, x0+2*radio, y1, fill=color, outline="")
    canvas.create_oval(x1-2*radio, y1-2*radio, x1, y1, fill=color, outline="")

    canvas.create_text(ancho//2, alto//2,
                       text=canvas.texto,
                       fill=canvas.color_fg,
                       font=("Arial", fuente, "bold"))

    canvas.bind("<Button-1>", lambda e: canvas.comando())

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

ruta_imagen = "C:/Users/josue/Desktop/Tercero/Proyecto Pis/emociones2/Detecci-n-de-emociones/img/logo_DS.png"

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
                                  lambda: (root.withdraw(), abrir_camara()))
                                                        
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