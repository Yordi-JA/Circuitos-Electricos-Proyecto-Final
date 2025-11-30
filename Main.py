import customtkinter as ctk
import Datos


class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nodos Equipo 2")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.construir_menu()

    def construir_menu(self):
        self.frame_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_menu.grid(row=0, column=0)

        self.label = ctk.CTkLabel(
            self.frame_menu, 
            text="Método de nodos", 
            font=("Helvetica", 20),
            text_color=("gray70") 
        )
        self.label.pack(pady=(0, 20))

        self.btn_inicio = ctk.CTkButton(
            self.frame_menu,
            text="INICIO",
            command=self.actividad, 
            width=200,
            height=40,
            corner_radius=20, 
            font=("Helvetica", 14),
            fg_color="#7167ff"
        )
        self.btn_inicio.pack()

    def actividad(self):
        self.frame_menu.destroy()
        Datos.entradas(self)

if __name__ == "__main__":
    app = Menu()
    app.mainloop()