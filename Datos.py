import customtkinter as ctk

# Aqui se van a solicitar los datos de entrada del circuito

def entradas(inicio):

    frame_trabajo = ctk.CTkFrame(inicio, fg_color="transparent")
    frame_trabajo.pack(fill="both", expand=True, padx=20, pady=20)

    lbl_titulo = ctk.CTkLabel(
        frame_trabajo, 
        text="Entradas", 
        font=("Helvetica", 24, "bold")
    )
    
    lbl_titulo.pack(pady=20)
