import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from interfaz.utils_ui import centrar_ventana


def ver_fotos(root):
    gal_window = tk.Toplevel(root)
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
        command=lambda: (gal_window.destroy(), root.deiconify())
    )
    btn_regresar.pack(side="left", padx=15, pady=10)

    frame_titulo = tk.Frame(barra_superior, bg="#003B70")
    frame_titulo.pack(expand=True, fill="both")

    titulo = tk.Label(
        frame_titulo,
        text="GALERÍA DE FOTOS",
        bg="#003B70",
        fg="white",
        font=("Arial", 18, "bold")
    )

    x_proporcion = 190 / 900
    titulo.place(x=int(x_proporcion * 900), rely=0.5, anchor="w")

    def actualizar_posicion_titulo(event=None):
        ancho_actual = gal_window.winfo_width()
        x = int(x_proporcion * ancho_actual)
        titulo.place(x=x, rely=0.5, anchor="w")

    gal_window.bind("<Configure>", actualizar_posicion_titulo)

    # ---------------------- CANVAS ----------------------
    canvas_frame = tk.Frame(gal_window, bg="white")
    canvas_frame.pack(expand=True, fill="both")

    canvas = tk.Canvas(canvas_frame, bg="#F2F2F2", highlightthickness=0)
    canvas.pack(expand=True, fill="both", padx=20, pady=20)

    if not os.path.exists("Galeria"):
        os.makedirs("Galeria")

    fotos = sorted(os.listdir("Galeria"), reverse=True)
    idx = [0]
    ultimo_tamano = {"w": 0, "h": 0}

    def mostrar_imagen():
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if ultimo_tamano["w"] == w and ultimo_tamano["h"] == h:
            return

        ultimo_tamano["w"] = w
        ultimo_tamano["h"] = h
        canvas.delete("all")

        if fotos:
            ruta = os.path.join("Galeria", fotos[idx[0]])
            img = Image.open(ruta)

            max_w = w - 20
            max_h = h - 20

            img_w, img_h = img.size
            ratio = min(max_w / img_w, max_h / img_h)
            new_size = (int(img_w * ratio), int(img_h * ratio))

            img = img.resize(new_size, Image.LANCZOS)
            imgtk = ImageTk.PhotoImage(img)

            canvas.imgtk = imgtk
            canvas.create_image(w // 2, h // 2, image=imgtk)
        else:
            canvas.create_text(
                w // 2,
                h // 2,
                text="No hay fotos guardadas",
                fill="#003B70",
                font=("Arial", 20, "bold")
            )

    def siguiente():
        if idx[0] < len(fotos) - 1:
            idx[0] += 1
            ultimo_tamano["w"] = 0
            mostrar_imagen()

    def anterior():
        if idx[0] > 0:
            idx[0] -= 1
            ultimo_tamano["w"] = 0
            mostrar_imagen()

    def borrar():
        if fotos:
            ruta = os.path.join("Galeria", fotos[idx[0]])
            os.remove(ruta)
            fotos.pop(idx[0])

            if idx[0] >= len(fotos):
                idx[0] = len(fotos) - 1

            ultimo_tamano["w"] = 0
            mostrar_imagen()

    # ---------------------- BOTONES ----------------------
    barra_botones = tk.Frame(gal_window, bg="white")
    barra_botones.pack(pady=15)

    style = ttk.Style(gal_window)
    style.theme_use("clam")

    style.configure("BotonAzul.TButton",
                    background="#319BF1",
                    font=("Arial", 13, "bold"),
                    padding=8)

    style.configure("BotonVerde.TButton",
                    background="#58F389",
                    font=("Arial", 13, "bold"),
                    padding=8)

    ttk.Button(barra_botones, text="⟵ Anterior",
               style="BotonAzul.TButton", command=anterior).grid(row=0, column=0, padx=10)

    ttk.Button(barra_botones, text="Siguiente ⟶",
               style="BotonAzul.TButton", command=siguiente).grid(row=0, column=1, padx=10)

    ttk.Button(barra_botones, text="🗑 Borrar Foto",
               style="BotonVerde.TButton", command=borrar).grid(row=0, column=2, padx=10)

    canvas.bind("<Configure>", lambda e: mostrar_imagen())
    gal_window.after(100, mostrar_imagen)

    gal_window.protocol("WM_DELETE_WINDOW", root.destroy)

