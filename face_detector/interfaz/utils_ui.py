import cv2
import tkinter as tk

# =========================
# Diccionario de emociones
# =========================
emociones_es = {
    "anger": "Enojado",
    "disgust": "Disgustado",
    "fear": "Asustado",
    "happiness": "Feliz",
    "neutral": "Neutral",
    "sadness": "Triste",
    "surprise": "Sorprendido"
}

# =========================================
# Texto con fondo semitransparente (OpenCV)
# =========================================
def texto_con_fondo(
    img,
    texto,
    x,
    y,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    escala=0.7,
    grosor=2,
    color_texto=(255, 255, 255),
    color_fondo=(0, 0, 0),
    alpha=0.6,
    padding=6
):
    (w, h), _ = cv2.getTextSize(texto, font, escala, grosor)

    overlay = img.copy()

    cv2.rectangle(
        overlay,
        (x - padding, y - h - padding),
        (x + w + padding, y + padding),
        color_fondo,
        -1
    )

    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    cv2.putText(
        img,
        texto,
        (x, y),
        font,
        escala,
        color_texto,
        grosor,
        cv2.LINE_AA
    )

# ======================
# Centrar ventana Tk
# ======================
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ======================
# Mensaje flotante UI
# ======================
def mostrar_mensaje(ventana, texto, duracion=3000):
    mensaje = tk.Label(
        ventana,
        text=texto,
        bg="#7BC0D9",
        fg="black",
        font=("Arial", 14, "bold"),
        bd=2,
        relief="solid",
        padx=10,
        pady=5
    )

    mensaje.place(x=10, y=10)

    def posicionar():
        if not ventana.winfo_exists():
            return
        mensaje.update_idletasks()
        ventana_h = ventana.winfo_height()
        label_h = mensaje.winfo_height()
        mensaje.place(x=10, y=ventana_h - label_h - 10)


    ventana.after(50, posicionar)
    ventana.after(duracion, mensaje.destroy)

# ======================
# Aclarar / oscurecer color
# ======================
def shade_color(color, factor):
    color = color.lstrip('#')
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    r = min(int(r * factor), 255)
    g = min(int(g * factor), 255)
    b = min(int(b * factor), 255)

    return f"#{r:02x}{g:02x}{b:02x}"
