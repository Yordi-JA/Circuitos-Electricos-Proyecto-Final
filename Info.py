import customtkinter as ctk

def show_about(app):
    # Separamos el título del cuerpo del texto
    titulo = "ACERCA DE"
    texto = (
        "Método de nodos\n"
        "Equipo 2\n\n"
        "Desarrollado por:\n\n"
        "Araiza Valdés Diego Antonio\n"
        "Ayala Hernández María Fernanda\n"
        "Jiménez Ayala Yordi Josué\n"
        "Membrilla Ramos Isaias Iñaki\n"
        "Portilla Hermenegildo Elizabeth"
    )
    _create_card(app, titulo, texto)

def show_help(app):
    titulo = "AYUDA"
    texto = (
        "Aca se pone como funciona el programa\n"
        "(lo que se debe meter y lo que entrega)"
    )
    _create_card(app, titulo, texto)

def _create_card(app, title, content):
    app.ocultar_menu_principal()

    info_frame = ctk.CTkFrame(
        app,
        fg_color="#2b2b2b",
        corner_radius=20,
        border_width=1,
        border_color="#444",
        bg_color="#1a1a1a"
    )
    info_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(
        info_frame,
        text=title,
        font=("Helvetica", 20, "bold"), 
        text_color="white"
    )

    title_label.pack(padx=40, pady=(30, 10))

    content_label = ctk.CTkLabel(
        info_frame,
        text=content,
        font=("Helvetica", 14), 
        justify="center",
        text_color="white"
    )
    content_label.pack(padx=40, pady=(0, 30))

    back_button = ctk.CTkButton(
        info_frame,
        text="Regresar",
        command=lambda: close_info(app, info_frame),
        fg_color="#7167ff",
        hover_color="#5a52cc",
        width=150,
        corner_radius=25
    )
    back_button.pack(pady=(0, 20))

def close_info(app, frame):
    frame.destroy()
    app.mostrar_menu_principal()