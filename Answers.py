import customtkinter as ctk
import math
import cmath
import numpy as np

def mostrar_respuestas(app, callback_regresar, resultados):
    
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

    header_frame = ctk.CTkFrame(card_frame, fg_color="transparent", height=40)
    header_frame.pack(fill="x", padx=20, pady=(20, 10))

    btn_regresar = ctk.CTkButton(
        header_frame, 
        text="Regresar", 
        fg_color="#c0392b", 
        hover_color="#a93226",
        width=70,
        height=28,
        command=lambda: cerrar_respuestas(card_frame, callback_regresar)
    )
    btn_regresar.pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(
        card_frame, 
        label_text="Matrices de salida",
        fg_color="#212121",    
        corner_radius=15,      
        label_fg_color="#333",
        height=200
    )
    scroll_frame.pack(fill="both", expand=True, padx=40, pady=(5, 30))

    for nombre, matriz in resultados.items():
        mostrar_matriz_resultado(scroll_frame, nombre, matriz)

def cerrar_respuestas(frame, callback):
    frame.destroy()
    callback()

def formatear_complejo(valor):
    try:
        val = complex(valor)
        if abs(val.imag) < 1e-6:
            return f"{val.real:.4g}"
        r, phi = cmath.polar(val)
        grad = math.degrees(phi)
        return f"{r:.2f}<{grad:.1f}°"
    except Exception:
        return str(valor)

def mostrar_matriz_resultado(parent, nombre, matriz):
    lbl = ctk.CTkLabel(parent, text=f"{nombre}", font=("Helvetica", 12, "bold"))
    lbl.pack(pady=(10, 2))

    grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
    grid_frame.pack(pady=2)

    if np.ndim(matriz) == 0:
        val_str = formatear_complejo(matriz)
        crear_celda_resultado(grid_frame, val_str, 0, 0)
        return
    
    filas = matriz.shape[0]
    cols = matriz.shape[1] if matriz.ndim > 1 else 1

    for r in range(filas):
        for c in range(cols):
            if matriz.ndim > 1:
                val = matriz[r, c]
            else:
                val = matriz[r]
            
            texto = formatear_complejo(val)
            crear_celda_resultado(grid_frame, texto, r, c)

def crear_celda_resultado(parent, texto, r, c):

    entry = ctk.CTkEntry(
        parent, 
        width=80,   
        height=25, 
        font=("Arial", 11),
        justify="center",
        text_color="white",
        fg_color="#343638",
        border_color="#565b5e"
    )
    entry.insert(0, texto)
    entry.configure(state="disabled") 
    entry.grid(row=r, column=c, padx=2, pady=2)