import customtkinter as ctk
import random
import math
import Option
import Info

class Nodo:
    def __init__(self, ancho, alto):
        self.x = random.randint(0, ancho)
        self.y = random.randint(0, alto)
        self.vx = random.uniform(-1.0, 1.5) 
        self.vy = random.uniform(-1.0, 1.5)
        self.radio = 3

    def mover(self, ancho, alto):
        self.x += self.vx
        self.y += self.vy

        if self.x <= 0:
            self.x = 0
            self.vx *= -1
        elif self.x >= ancho:
            self.x = ancho
            self.vx *= -1

        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        elif self.y >= alto:
            self.y = alto
            self.vy *= -1

class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nodos Equipo 2")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.canvas = ctk.CTkCanvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.nodos = [Nodo(600, 400) for _ in range(30)]
        self.animar_fondo() 

        self.construir_menu()

    def animar_fondo(self):
        try:
            self.canvas.delete("all") 
            w_real = self.canvas.winfo_width()
            h_real = self.canvas.winfo_height()

            if w_real < 50: w_real = 600
            if h_real < 50: h_real = 400

            for i, nodo_a in enumerate(self.nodos):
                for nodo_b in self.nodos[i+1:]:
                    dx = nodo_a.x - nodo_b.x
                    dy = nodo_a.y - nodo_b.y
                    distancia = math.hypot(dx, dy)

                    if distancia < 100: 
                        color = "#444444" if distancia > 60 else "#777777"
                        self.canvas.create_line(nodo_a.x, nodo_a.y, nodo_b.x, nodo_b.y, fill=color, width=1)

            for nodo in self.nodos:
                nodo.mover(w_real, h_real)
                self.canvas.create_oval(
                    nodo.x - nodo.radio, nodo.y - nodo.radio,
                    nodo.x + nodo.radio, nodo.y + nodo.radio,
                    fill="#7167ff", outline=""
                )

            self.after(30, self.animar_fondo)
        except Exception:
            pass

    def construir_menu(self):
        self.fondo_controles = ctk.CTkFrame(
            self, 
            fg_color="#2b2b2b",       
            corner_radius=20,
            border_width=1,
            border_color="#444",
            bg_color="#1a1a1a"        
        )
        self.fondo_controles.place(relx=0.5, rely=0.5, anchor="center")

        self.label = ctk.CTkLabel(
            self.fondo_controles, 
            text="Método de nodos", 
            font=("Helvetica", 24, "bold"),
            text_color=("white") 
        )
        self.label.pack(padx=40, pady=(30, 10)) 

        self.btn_inicio = ctk.CTkButton(
            self.fondo_controles,
            text="INICIO",
            command=self.actividad, 
            width=200,
            height=45,
            corner_radius=25,
            font=("Helvetica", 15, "bold"),
            fg_color="#7167ff",
            hover_color="#5a52cc"
        )
        self.btn_inicio.pack(padx=40, pady=(10, 30))

        self.btn_acerca = ctk.CTkButton(
            self,
            text="Acerca de",
            command=lambda: Info.show_about(self),
            width=100,
            height=30,
            fg_color="#2b2b2b",
            border_width=1,
            border_color="#444",
            hover_color="#3a3a3a",
            bg_color="#1a1a1a"
        )
        self.btn_acerca.place(relx=0.05, rely=0.95, anchor="sw")

        self.btn_ayuda = ctk.CTkButton(
            self,
            text="Ayuda",
            command=lambda: Info.show_help(self),
            width=100,
            height=30,
            fg_color="#2b2b2b",
            border_width=1,
            border_color="#444",
            hover_color="#3a3a3a",
            bg_color="#1a1a1a"
        )
        self.btn_ayuda.place(relx=0.95, rely=0.95, anchor="se")

    def ocultar_menu_principal(self):
        self.fondo_controles.place_forget()
        self.btn_acerca.place_forget()
        self.btn_ayuda.place_forget()

    def mostrar_menu_principal(self):
        self.fondo_controles.place(relx=0.5, rely=0.5, anchor="center")
        self.btn_acerca.place(relx=0.05, rely=0.95, anchor="sw")
        self.btn_ayuda.place(relx=0.95, rely=0.95, anchor="se")

    def actividad(self):
        Option.option(self)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Menu()
    app.mainloop()