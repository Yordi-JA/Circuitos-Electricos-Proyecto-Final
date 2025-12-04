import customtkinter as ctk
import cmath
import math
from Calculations import calculos
import Answers

entries_A = []
entries_Y = []
entries_Vsk = []
entries_Jsk = []

def show_matrix(app, return_callback):

    card_frame = ctk.CTkFrame(
        app, 
        width=560,             
        height=360,            
        corner_radius=15,
        fg_color="#2b2b2b",
        border_width=1,
        border_color="#444"
    )
    card_frame.place(relx=0.5, rely=0.5, anchor="center")

    card_frame.pack_propagate(False) 

    dims_frame = ctk.CTkFrame(card_frame, fg_color="transparent", height=40)
    dims_frame.pack(fill="x", padx=20, pady=(20, 10)) 

    lbl_m = ctk.CTkLabel(dims_frame, text="m:", text_color="white", font=("Arial", 12, "bold"))
    lbl_m.pack(side="left")
    entry_m = ctk.CTkEntry(dims_frame, width=35, placeholder_text="0")
    entry_m.pack(side="left", padx=5)

    lbl_n = ctk.CTkLabel(dims_frame, text="n:", text_color="white", font=("Arial", 12, "bold"))
    lbl_n.pack(side="left", padx=(5, 0))
    entry_n = ctk.CTkEntry(dims_frame, width=35, placeholder_text="0")
    entry_n.pack(side="left", padx=5)

    scroll_frame = ctk.CTkScrollableFrame(
        card_frame, 
        label_text="Matrices de entrada",
        fg_color="#212121",    
        corner_radius=15,      
        label_fg_color="#333",  
        height=200              
    )
    scroll_frame.pack(fill="both", expand=True, padx=40, pady=(5, 30))


    btn_generar = ctk.CTkButton(
        dims_frame, 
        text="Crear", 
        width=60,
        height=28,
        fg_color="#7167ff",
        hover_color="#5a52cc",
        command=lambda: generar_grids(entry_m.get(), entry_n.get(), scroll_frame)
    )
    btn_generar.pack(side="left", padx=10)

    btn_regresar = ctk.CTkButton(
        dims_frame, 
        text="Regresar", 
        fg_color="#c0392b", 
        hover_color="#a93226",
        width=70,
        height=28,
        command=lambda: cerrar_matrix(card_frame, return_callback)
    )
    btn_regresar.pack(side="right", padx=(5, 0)) 

    btn_calcular = ctk.CTkButton(
        dims_frame, 
        text="Calcular", 
        fg_color="#7167ff",
        hover_color="#5a52cc",
        width=70,
        height=28,
        command=lambda: procesar_datos(app, card_frame, return_callback) 
    )
    btn_calcular.pack(side="right") 


def cerrar_matrix(frame, callback):
    frame.destroy()
    callback()

def generar_grids(m_str, n_str, parent_frame):
    try:
        m = int(m_str)
        n = int(n_str)
        if m < 1 or n < 1: raise ValueError
    except ValueError:
        print("Error: Ingrese enteros > 0")
        return

    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    entries_A.clear()
    entries_Y.clear()
    entries_Vsk.clear()
    entries_Jsk.clear()
    
    crear_seccion_matriz(parent_frame, "A", m, n, entries_A)
    crear_seccion_matriz(parent_frame, "Y", n, n, entries_Y, es_diagonal=True)

    cd_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
    cd_container.pack(fill="x", pady=5)
    
    frame_left = ctk.CTkFrame(cd_container, fg_color="transparent")
    frame_left.pack(side="left", expand=True, fill="x")
    crear_seccion_matriz(frame_left, "V_sk", n, 1, entries_Vsk)

    frame_right = ctk.CTkFrame(cd_container, fg_color="transparent")
    frame_right.pack(side="right", expand=True, fill="x")
    crear_seccion_matriz(frame_right, "J_sk", n, 1, entries_Jsk)

def crear_seccion_matriz(parent, nombre, filas, cols, storage_list, es_diagonal=False):
    lbl = ctk.CTkLabel(parent, text=f"{nombre}", font=("Arial", 12, "bold"))
    lbl.pack(pady=(5, 0))
    
    grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
    grid_frame.pack(pady=2)

    for r in range(filas):
        row_data = []
        for c in range(cols):
            ph = "0"
            entry = ctk.CTkEntry(grid_frame, width=50, height=25, font=("Arial", 11), placeholder_text=ph)
            entry.grid(row=r, column=c, padx=1, pady=1)
            
            if es_diagonal:
                if r != c:
                    entry.insert(0, "0")
                    
            row_data.append(entry)
        storage_list.append(row_data)

def parse_input(texto):
    texto = str(texto).lower().replace(" ", "")
    if not texto: return 0j 

    try:
        if "<" in texto or "ang" in texto:
            separador = "<" if "<" in texto else "ang"
            if "angle" in texto: separador = "angle"
            partes = texto.split(separador)
            magnitud = float(partes[0])
            angulo_grados = float(partes[1])
            angulo_rad = math.radians(angulo_grados)
            return cmath.rect(magnitud, angulo_rad)
        
        texto = texto.replace("i", "j")
        return complex(texto)
    except Exception:
        return 0j

def procesar_datos(app, current_frame, main_menu_callback):
    try:
        mat_A = [[parse_input(e.get()).real for e in row] for row in entries_A]
        mat_Y = [[parse_input(e.get()) for e in row] for row in entries_Y]
        vec_Vsk = [[parse_input(e.get()) for e in row] for row in entries_Vsk]
        vec_Jsk = [[parse_input(e.get()) for e in row] for row in entries_Jsk]
        
        Y_n, e_n, V_k, J_k, A_T = calculos(mat_A, mat_Y, vec_Vsk, vec_Jsk)

        resultados = {
            "A_T": A_T,
            "Y_n": Y_n,
            "e_n": e_n,
            "V_k": V_k,
            "J_k": J_k
        }

        current_frame.place_forget() 
        
        Answers.mostrar_respuestas(
            app, 
            lambda: current_frame.place(relx=0.5, rely=0.5, anchor="center"), 
            resultados
        )

    except ValueError as ve:
        print(f"\nError de Valor: {ve}")
    except Exception as e:
        print(f"\nError Inesperado: {e}")