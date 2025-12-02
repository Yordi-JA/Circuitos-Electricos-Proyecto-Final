import customtkinter as ctk

def option(app):
    # 1. Crear el Marco Central
    frame_opciones = ctk.CTkFrame(
        app,
        fg_color="#2b2b2b",
        corner_radius=20,
        border_width=1,
        border_color="#444",
        bg_color="#1a1a1a"
    )
    frame_opciones.place(relx=0.5, rely=0.5, anchor="center")

    label_titulo = ctk.CTkLabel(
        frame_opciones,
        text="Seleccione una opción",
        font=("Helvetica", 18, "bold"),
        text_color="white"
    )
    label_titulo.pack(padx=40, pady=(30, 20))

    # Botón 1
    btn_grafo = ctk.CTkButton(
        frame_opciones,
        text="Grafo dirigido",
        command=lambda: print("Ir a Grafo"),
        width=200,
        height=45,
        corner_radius=25,
        font=("Helvetica", 15, "bold"),
        fg_color="#7167ff",
        hover_color="#5a52cc"
    )
    btn_grafo.pack(padx=40, pady=(0, 15))

    # Botón 2
    btn_datos = ctk.CTkButton(
        frame_opciones,
        text="Datos",
        command=lambda: print("Ir a Datos"),
        width=200,
        height=45,
        corner_radius=25,
        font=("Helvetica", 15, "bold"),
        fg_color="#7167ff",
        hover_color="#5a52cc"
    )
    btn_datos.pack(padx=40, pady=(0, 30))

    # --- BOTÓN REGRESAR (Estilo "Acerca de") ---
    btn_regresar = ctk.CTkButton(
        app, 
        text="Regresar",
        command=lambda: cerrar_opciones(app, frame_opciones, btn_regresar),
        # --- AQUÍ ESTÁ EL CAMBIO DE ESTILO ---
        width=100,              # Más pequeño (como el de Acerca de)
        height=30,
        fg_color="#2b2b2b",     # Fondo oscuro
        border_width=1,         # Borde delgado
        border_color="#444",    # Color del borde gris
        hover_color="#3a3a3a",  # Color al pasar el mouse
        bg_color="#1a1a1a"      # Coincide con el fondo del canvas
    )
    # Posición izquierda inferior
    btn_regresar.place(relx=0.05, rely=0.95, anchor="sw")

def cerrar_opciones(app, frame, boton):
    frame.destroy()
    boton.destroy()
    app.mostrar_menu_principal()