from PIL import ImageTk

def crear_responsive(root, style, base_w, base_h,
                     img_original=None,
                     label_img=None,
                     img_base_w=0,
                     img_base_h=0,
                     botones=None,
                     dibujar_boton=None):

    pending = {"job": None}

    def adaptar(event=None):
        if pending["job"]:
            root.after_cancel(pending["job"])
        pending["job"] = root.after(80, aplicar_cambios)

    def aplicar_cambios():
        pending["job"] = None

        w = root.winfo_width()
        h = root.winfo_height()

        escala = min(w / base_w, h / base_h)

        # Título
        nueva_fuente = max(10, int(24 * escala))
        style.configure("Titulo.TLabel",
                        font=("Arial", nueva_fuente, "bold"))

        # Imagen
        if img_original and label_img:
            new_w = max(50, int(img_base_w * escala))
            new_h = max(50, int(img_base_h * escala))
            img_resized = img_original.resize((new_w, new_h))
            tk_img = ImageTk.PhotoImage(img_resized)
            label_img.config(image=tk_img)
            label_img.image = tk_img

        # Botones redondos
        if botones and dibujar_boton:
            for btn in botones:
                dibujar_boton(btn, escala)

    root.bind("<Configure>", adaptar)
