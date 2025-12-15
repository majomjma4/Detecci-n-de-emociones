import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from interfaz.utils_ui import centrar_ventana
from interfaz.botones import crear_boton_redondo, dibujar_boton
from interfaz.ventana_camara import abrir_camara
from interfaz.ventana_galeria import ver_fotos
from interfaz.responsive import crear_responsive


def iniciar_app():
    root = tk.Tk()
    root.title("Detección de Emociones en Tiempo Real")

    BASE_W = 750
    BASE_H = 500
    centrar_ventana(root, BASE_W, BASE_H)
    root.configure(bg="#CFEFFF")

    # ---------- ESTILOS ----------
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Titulo.TLabel",
                    background="#CFEFFF",
                    foreground="#000000",
                    font=("Arial", 24, "bold"))

    # ---------- TÍTULO ----------
    titulo = ttk.Label(
        root,
        text="DETECCIÓN DE EMOCIONES EN TIEMPO REAL",
        style="Titulo.TLabel"
    )
    titulo.pack(pady=20)

    tk.Frame(root, bg="#03581E", height=3).pack(fill="x", padx=90)

    # ---------- IMAGEN ----------
    IMG_BASE_W = 319
    IMG_BASE_H = 270
    ruta_imagen = "img/logo_DS.png"

    frame_img = tk.Frame(root, bg="#CFEFFF")
    frame_img.pack(pady=10)

    try:
        img_original = Image.open(ruta_imagen)
    except:
        img_original = None

    label_img = tk.Label(frame_img, bg="#CFEFFF")
    label_img.pack()

    if img_original:
        label_img.image = ImageTk.PhotoImage(img_original)
        label_img.config(image=label_img.image)

    # ---------- BOTONES ----------
    frame_botones = tk.Frame(root, bg="#CFEFFF")
    frame_botones.pack(pady=20)

    btn_iniciar = crear_boton_redondo(
        frame_botones, "INICIAR",
        "#69E991", "black", "#97E0AE", "#69B4F1",
        lambda: (root.withdraw(), abrir_camara(root))
    )
    btn_iniciar.pack(side="left", padx=10)
    dibujar_boton(btn_iniciar, 1)

    btn_galeria = crear_boton_redondo(
        frame_botones, "GALERÍA",
        "#69B4F1", "black", "#A2C2DD", "#69B4F1",
        lambda: (root.withdraw(), ver_fotos(root))
    )
    btn_galeria.pack(side="left", padx=10)
    dibujar_boton(btn_galeria, 1)

    # ---------- RESPONSIVE ----------
    crear_responsive(
        root=root,
        style=style,
        base_w=BASE_W,
        base_h=BASE_H,
        img_original=img_original,
        label_img=label_img,
        img_base_w=IMG_BASE_W,
        img_base_h=IMG_BASE_H,
        botones=[btn_iniciar, btn_galeria],
        dibujar_boton=dibujar_boton
    )

    root.mainloop()
