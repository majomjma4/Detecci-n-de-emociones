import cv2
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import winsound

from detectar_caras import detectar_caras
from detectar_emociones import detectar_emocion
from detectar_genero import detectar_genero
from detectar_edad import detectar_edad
from collections import deque, Counter

from interfaz.utils_ui import (
    centrar_ventana,
    texto_con_fondo,
    mostrar_mensaje,
    emociones_es
)


# ---------- Ventana de cámara ----------

print("🔥 ESTE ES MI ventana_camara.py 🔥")

def abrir_camara(root):

    frame_count = 0

    ultima_emocion = ""
    ultima_edad = ""
    ultimo_genero = ""

    hist_genero = [deque(maxlen=20)]
    hist_edad = [deque(maxlen=20)]



    global cap 
    cam_window = tk.Toplevel()
    cam_window.title("Cámara - Detección de Emociones")
    ancho, alto = 900, 600
    centrar_ventana(cam_window, ancho, alto)
    cam_window.configure(bg="#1E1E1E")  # fondo gris oscuro

    # Barra superior azul
    barra_superior = tk.Frame(cam_window, bg="#003B70", height=45)
    barra_superior.pack(side="top", fill="x")

    def regresar():
        if cap.isOpened():
            cap.release()           # cerrar cámara
        cam_window.destroy()       # cerrar ventana cámara
        root.deiconify()           # volver a ventana principal

    btn_regresar = tk.Button(
        barra_superior,
        text="⟵ Regresar",
        font=("Arial", 18, "bold"),
        bg="#003B70",
        fg="white",
        bd=0,
        activebackground="#002F55",
        activeforeground="white",
        command=regresar
    )
    btn_regresar.pack(side="left", padx=10, pady=5)

    # ---------- Abrimos la cámara ----------
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("NO SE PUDO ABRIR LA CÁMARA")
        cam_window.destroy()
        root.deiconify()
        return


    # Barra lateral derecha GENERO 
    barra_genero = tk.Frame(cam_window, bg="#2B2B2B", width=220)
    barra_genero.pack(side="right", fill="y")

    titulo_genero = tk.Label(
        barra_genero,
        text="DETECTAR GÉNERO:",
        bg="#2B2B2B",
        fg="white",
        font=("Arial", 12, "bold")
    )
    titulo_genero.pack(pady=(60, 15))

    btn_genero = tk.Label(
        barra_genero,
        text="DESACTIVADO",
        bg="#B00020",
        fg="black",
        font=("Arial", 11, "bold"),
        width=14,
        height=2,
        cursor="hand2"
    )
    btn_genero.pack(pady=5)

    detectar_genero_activo = False

    # Colores
    color_activado = "#1FAA00"
    color_activado_hover = "#9af58a"  # un verde más oscuro
    color_desactivado = "#B00020"
    color_desactivado_hover = "#FE9AAB"  # rojo más oscuro

    def toggle_genero(event=None):
        nonlocal detectar_genero_activo, ultimo_genero

        detectar_genero_activo = not detectar_genero_activo

        hist_genero[0].clear()
        ultimo_genero = ""

        if detectar_genero_activo:
            btn_genero.config(text="ACTIVADO", bg=color_activado)
        else:
            btn_genero.config(text="DESACTIVADO", bg=color_desactivado)


    def on_enter(event):
        if detectar_genero_activo:
            btn_genero.config(bg=color_activado_hover)
        else:
            btn_genero.config(bg=color_desactivado_hover)

    def on_leave(event):
        if detectar_genero_activo:
            btn_genero.config(bg=color_activado)
        else:
            btn_genero.config(bg=color_desactivado)

    btn_genero.bind("<Button-1>", toggle_genero)
    btn_genero.bind("<Enter>", on_enter)
    btn_genero.bind("<Leave>", on_leave)

    # Barra lateral derecha EDAD 

    titulo_edad = tk.Label(
        barra_genero,
        text="DETECTAR EDAD:",
        bg="#2B2B2B",
        fg="white",
        font=("Arial", 12, "bold")
    )
    titulo_edad.pack(pady=(25, 15))

    btn_edad = tk.Label(
        barra_genero,
        text="DESACTIVADO",
        bg=color_desactivado,
        fg="black",
        font=("Arial", 11, "bold"),
        width=14,
        height=2,
        cursor="hand2"
    )
    btn_edad.pack(pady=5)

    detectar_edad_activo = False

    def toggle_edad(event=None):
        nonlocal detectar_edad_activo, ultima_edad

        detectar_edad_activo = not detectar_edad_activo

        hist_edad[0].clear()
        ultima_edad = "Calculando..."

        if detectar_edad_activo:
            
            btn_edad.config(text="ACTIVADO", bg=color_activado)
        else:
            btn_edad.config(text="DESACTIVADO", bg=color_desactivado)


    def on_enter_edad(event):
        if detectar_edad_activo:
            btn_edad.config(bg=color_activado_hover)
        else:
            btn_edad.config(bg=color_desactivado_hover)

    def on_leave_edad(event):
        if detectar_edad_activo:
            btn_edad.config(bg=color_activado)
        else:
            btn_edad.config(bg=color_desactivado)

    btn_edad.bind("<Button-1>", toggle_edad)
    btn_edad.bind("<Enter>", on_enter_edad)
    btn_edad.bind("<Leave>", on_leave_edad)



    # Canvas central para cámara
    canvas_frame = tk.Frame(cam_window, bg="#1E1E1E")
    canvas_frame.pack(expand=True, fill="both", side="left")
    canvas = tk.Canvas(canvas_frame, bg="#1E1E1E", highlightthickness=0)
    canvas.pack(expand=True, fill="both")

    # Barra inferior con botón de foto
    barra_inferior = tk.Frame(canvas_frame, bg="#1E1E1E", height=80)
    barra_inferior.place(relx=0.5, rely=0.95, anchor="s")

    # Abrimos y redimensionamos el ícono
    icono_img = Image.open("C:/Users/marijo monteros/Desktop/Tercer Semestre/Proyecto Pis/Codigo_Pis/img/icono_camar.webp").resize((50,50))
    icono = ImageTk.PhotoImage(icono_img)

    # Botón de cámara completamente redondo
    btn_size = 80
    circulo_size = 70
    btn_foto = tk.Canvas(barra_inferior, width=btn_size, height=btn_size, bg="#1E1E1E", highlightthickness=0)
    btn_foto.pack()
    padding = (btn_size - circulo_size)//2
    circulo = btn_foto.create_oval(padding, padding, padding+circulo_size, padding+circulo_size, fill="#F0EBEB", outline="#ffffff", width=2)
    icono_id = btn_foto.create_image(btn_size//2, btn_size//2, image=icono)
    btn_foto.image = icono

    def click_btn(event):
        tomar_foto()
    btn_foto.tag_bind(circulo, "<Button-1>", click_btn)
    btn_foto.tag_bind(icono_id, "<Button-1>", click_btn)

    # ---------- Cámara ----------
    frame_global = None

    def tomar_foto():
        if frame_global is None:
            return
        
        frame_guardar = frame_global.copy()
        faces = detectar_caras(frame_guardar)

        for (x, y, w_face, h_face) in faces:
            cv2.rectangle(frame_guardar, (x, y), (x+w_face, y+h_face), (0,255,0), 2)
                
               
                # 🔹 Emoción
            if ultima_emocion:
                texto_con_fondo(
                    frame_guardar,
                    ultima_emocion,
                    x,
                    y - 40,
                    escala=0.9,
                    color_texto=(255,255,255),
                    color_fondo=(0,0,0),
                    alpha=0.6
                )

                    # 🔹 Edad
            if detectar_edad_activo and ultima_edad != "":
                    texto_con_fondo(
                    frame_guardar,
                    f"Edad: {ultima_edad}",
                    x,
                    y-10,
                    escala=0.75,
                    color_texto=(255,255,255),
                    color_fondo=(0,0,0),
                    alpha=0.6
                )
                        

                    # 🔹 Género
            if detectar_genero_activo and ultimo_genero:
                    texto_con_fondo(
                    frame_guardar,
                    ultimo_genero,
                    x,
                    y + h_face + 28,
                    escala=0.9,
                    color_texto=(255,255,255),
                    color_fondo=(0,0,0),
                    alpha=0.6
                )

                        

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Galeria/foto_{timestamp}.png"
        cv2.imwrite(filename, cv2.cvtColor(frame_guardar, cv2.COLOR_RGB2BGR))

        winsound.PlaySound("C:/Users/marijo monteros/Desktop/Tercer Semestre/Proyecto Pis/Codigo_Pis/sound/A-modern-camera-shutter-click.wav",
                        winsound.SND_FILENAME | winsound.SND_ASYNC)
            
        # Agregar esta línea para mostrar el mensaje en la parte inferior izquierda
        mostrar_mensaje(cam_window, "Foto guardada con éxito", 3000)  # Mostrar el mensaje por 10 segundos


    # Mostrar frame adaptativo

    def mostrar_frame():
        if not cam_window.winfo_exists():
            return  # La ventana ha sido cerrada
        
        nonlocal frame_global, frame_count
        nonlocal ultima_emocion, ultima_edad, ultimo_genero

        ret, frame = cap.read()
        if not ret:
            canvas.after(30, mostrar_frame)
            return

        frame_count += 1

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_global = frame_rgb.copy()

        # Detectar caras
        caras = detectar_caras(frame_rgb)

        # Si no hay rostro, limpiamos historial (evita saltos raros)
        if len(caras) == 0:
            hist_genero[0].clear()
            hist_edad[0].clear()
            ultimo_genero = ""
            ultima_edad = "Sin rostro"

        for (x, y, w_face, h_face) in caras:
            rostro = frame_rgb[y:y+h_face, x:x+w_face]

            # Detectar SOLO cada 6 frames (anti-lag)
            if frame_count % 6 == 0:
                try:
                    emotion = detectar_emocion(rostro)
                    ultima_emocion = emociones_es.get(str(emotion).lower(), "Desconocido")
                except:
                    pass

                if detectar_edad_activo:
                    try:
                        edad = detectar_edad(rostro)
                        print("EDAD RAW =>", edad, type(edad))

                        edad_num = None

                        if isinstance(edad, (int, float)):
                            edad_num = int(edad)

                        elif isinstance(edad, (list, tuple)) and len(edad) > 0:
                            if isinstance(edad[0], (int, float)):
                                edad_num = int(edad[0])

                        elif isinstance(edad, str):
                            edad = edad.replace("(", "").replace(")", "").strip()

                            if "-" in edad:
                                partes = edad.split("-")
                                if partes[0].strip().isdigit():
                                    edad_num = int(partes[0].strip())

                            elif edad.isdigit():
                                edad_num = int(edad)


                        # ✅ CONDICIÓN CORRECTA
                        if edad_num is not None and 0 < edad_num < 100:
                            hist_edad[0].append(edad_num)
                            print("Edad agregada al historial:", edad_num)

                        if len(hist_edad[0]) >= 4:
                            promedio = int(sum(hist_edad[0]) / len(hist_edad[0]))

                            if promedio <= 12:
                                ultima_edad = "8 - 12"
                            elif promedio <= 19:
                                ultima_edad = "13 - 19"
                            elif promedio <= 29:
                                ultima_edad = "20 - 29"
                            elif promedio <= 39:
                                ultima_edad = "30 - 39"
                            elif promedio <= 49:
                                ultima_edad = "40 - 49"
                            else:
                                ultima_edad = "50+"
                        else:
                            ultima_edad = "Calculando..."

                    except Exception as e:
                        print("ERROR EDAD:", e)


                if detectar_genero_activo:
                    try:
                        g = detectar_genero(rostro)
                        hist_genero[0].append(g)

                        conteo = Counter(hist_genero[0])
                        total = sum(conteo.values())

                        porcentaje = {
                            k: int((v / total) * 100)
                            for k, v in conteo.items()
                        }

                        # Obtener género con mayor porcentaje
                        genero_final = max(porcentaje, key=porcentaje.get)
                        confianza = porcentaje[genero_final]

                        ultimo_genero = f"{genero_final} {confianza}%"


                    except:
                        pass

            # Rectángulo del rostro
            cv2.rectangle(
                frame_rgb,
                (x, y),
                (x + w_face, y + h_face),
                (0, 255, 0),
                2
            )

            # EMOCIÓN (arriba)
            if ultima_emocion:
                texto_con_fondo(
                    frame_rgb,
                    ultima_emocion,
                    x,
                    y - 42,      # ⬆ un poco más arriba
                    escala=0.9,
                    color_texto=(255, 255, 255),
                    color_fondo=(0, 0, 0),
                    alpha=0.6
                )

            # EDAD
            if detectar_edad_activo:
                texto_con_fondo(
                    frame_rgb,
                    f"Edad: {ultima_edad}",
                    x,
                    y - 12,
                    escala=0.75,
                    color_texto=(255, 255, 255),
                    color_fondo=(0, 0, 0),
                    alpha=0.6
                )

            # GÉNERO (abajo, 2px más abajo)
            if detectar_genero_activo and ultimo_genero:
                texto_con_fondo(
                    frame_rgb,
                    ultimo_genero,
                    x,
                    y + h_face + 30,
                    escala=0.9,
                    color_texto=(255, 255, 255),
                    color_fondo=(0, 0, 0),
                    alpha=0.6
                )

        # Escalar al canvas
        canvas_w, canvas_h = canvas.winfo_width(), canvas.winfo_height()
        if canvas_w < 1 or canvas_h < 1:
            cam_window.after(50, mostrar_frame)
            return

        frame_h, frame_w = frame_rgb.shape[:2]
        scale = min(canvas_w / frame_w, canvas_h / frame_h)
        new_w = max(1, int(frame_w * scale))
        new_h = max(1, int(frame_h * scale))

        frame_resized = cv2.resize(frame_rgb, (new_w, new_h))
        imgtk = ImageTk.PhotoImage(Image.fromarray(frame_resized))

        canvas.imgtk = imgtk
        canvas.delete("all")
        canvas.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=imgtk,
            anchor="center"
        )

        canvas.after(30, mostrar_frame)

    def cerrar_camara_total():
        global cap
        if cap is not None and cap.isOpened():
            cap.release()  # Liberar cámara
            cap = None
        cam_window.destroy()  # Cierra la ventana de la cámara
        root.destroy()        # Cierra la ventana principal y termina el programa

    cam_window.protocol("WM_DELETE_WINDOW", cerrar_camara_total)

    mostrar_frame()