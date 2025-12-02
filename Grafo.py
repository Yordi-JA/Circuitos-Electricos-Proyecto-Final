import customtkinter as ctk
import Draw

class GrafoInterface:
    def __init__(self, app, return_callback):
        self.app = app
        self.return_callback = return_callback
        self.conexiones = [] 

        self.frame_grafo = ctk.CTkFrame(
            self.app,
            fg_color="#2b2b2b",
            corner_radius=15,
            border_width=1,
            border_color="#444",
            bg_color="#1a1a1a"
        )
        self.frame_grafo.place(relx=0.5, rely=0.5, anchor="center")

        self.init_input_view()

        self.btn_regresar = ctk.CTkButton(
            self.app, text="Regresar", command=self.cerrar, width=80, height=28,
            fg_color="#2b2b2b", border_width=1, border_color="#444", hover_color="#3a3a3a", bg_color="#1a1a1a"
        )
        self.btn_regresar.place(relx=0.05, rely=0.95, anchor="sw")

    def init_input_view(self):
        for widget in self.frame_grafo.winfo_children():
            widget.destroy()

        self.label_titulo = ctk.CTkLabel(self.frame_grafo, text="Conexiones", font=("Helvetica", 16, "bold"), text_color="white")
        self.label_titulo.pack(padx=20, pady=(15, 10))

        self.input_frame = ctk.CTkFrame(self.frame_grafo, fg_color="transparent")
        self.input_frame.pack(padx=20, pady=(0, 10))

        self.entry_a = ctk.CTkEntry(self.input_frame, placeholder_text="A", width=50, justify="center", fg_color="#3a3a3a", border_color="#555")
        self.entry_a.grid(row=0, column=0, padx=2)
        
        ctk.CTkLabel(self.input_frame, text="→", font=("Helvetica", 16), text_color="gray").grid(row=0, column=1, padx=2)
        
        self.entry_b = ctk.CTkEntry(self.input_frame, placeholder_text="B", width=50, justify="center", fg_color="#3a3a3a", border_color="#555")
        self.entry_b.grid(row=0, column=2, padx=2)

        self.btn_agregar = ctk.CTkButton(self.input_frame, text="+", width=30, height=28, command=self.agregar_conexion, fg_color="#7167ff", hover_color="#5a52cc")
        self.btn_agregar.grid(row=0, column=3, padx=(10, 2))

        self.btn_eliminar = ctk.CTkButton(self.input_frame, text="-", width=30, height=28, command=self.eliminar_conexion, fg_color="#cf4444", hover_color="#a83232")
        self.btn_eliminar.grid(row=0, column=4, padx=(2, 0))

        self.lista_texto = ctk.CTkTextbox(self.frame_grafo, width=200, height=80, fg_color="#1a1a1a", text_color="#ddd", font=("Courier", 12), corner_radius=10)
        self.lista_texto.pack(padx=20, pady=(0, 15))
        self.lista_texto.configure(state="disabled")
        self.actualizar_lista_visual() 

        self.btn_mostrar = ctk.CTkButton(self.frame_grafo, text="Mostrar Grafo", command=self.mostrar_grafo_final, width=160, height=30, corner_radius=15, font=("Helvetica", 13, "bold"), fg_color="#7167ff", hover_color="#5a52cc")
        self.btn_mostrar.pack(padx=30, pady=(0, 20))

    def agregar_conexion(self):
        a, b = self.entry_a.get().strip(), self.entry_b.get().strip()
        if a.isdigit() and b.isdigit() and (a, b) not in self.conexiones:
            self.conexiones.append((a, b))
            self.actualizar_lista_visual()
            self.entry_a.delete(0, 'end'); self.entry_b.delete(0, 'end'); self.entry_a.focus()

    def eliminar_conexion(self):
        a, b = self.entry_a.get().strip(), self.entry_b.get().strip()
        if (a, b) in self.conexiones:
            self.conexiones.remove((a, b))
            self.actualizar_lista_visual()
            self.entry_a.delete(0, 'end'); self.entry_b.delete(0, 'end')

    def actualizar_lista_visual(self):
        self.lista_texto.configure(state="normal")
        self.lista_texto.delete("0.0", "end")
        for a, b in self.conexiones:
            self.lista_texto.insert("end", f" {a} -> {b}\n")
        self.lista_texto.configure(state="disabled")
        self.lista_texto.see("end")

    def mostrar_grafo_final(self):
        Draw.dibujar_grafo_en_frame(self.frame_grafo, self.conexiones, self.init_input_view)

    def cerrar(self):
        from matplotlib import pyplot as plt 
        plt.close('all') 
        
        self.frame_grafo.destroy()
        self.btn_regresar.destroy()
        self.return_callback()

def show_grafo(app, return_callback):
    GrafoInterface(app, return_callback)