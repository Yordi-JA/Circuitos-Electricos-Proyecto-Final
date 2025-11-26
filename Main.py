import customtkinter as ctk


ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("dark-blue") 

class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nodos Equipo 2")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0)

        self.label = ctk.CTkLabel(
            self.main_frame, 
            text="Método de nodos", 
            font=("Helvetica", 20),
            text_color=("gray70") 
        )
        self.label.pack(pady=(0, 20))

        # Botón de inicio
        self.btn_inicio = ctk.CTkButton(
            self.main_frame,
            text="INICIO",
            command=self.iniciar_accion,
            width=200,
            height=40,
            corner_radius=20, 
            font=("Helvetica", 14),
            fg_color="#7167ff"
        )
        self.btn_inicio.pack()

    def iniciar_accion(self):
        print("A")

if __name__ == "__main__":
    app = Menu()
    app.mainloop()