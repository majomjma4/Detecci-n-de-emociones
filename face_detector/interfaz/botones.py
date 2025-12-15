import tkinter as tk

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

    canvas.create_text(
        ancho//2,
        alto//2,
        text=canvas.texto,
        fill=canvas.color_fg,
        font=("Arial", fuente, "bold")
    )

    canvas.bind("<Button-1>", lambda e: canvas.comando())
