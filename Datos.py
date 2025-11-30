import customtkinter as ctk
import Circuito

PREFIJOS = {
    "x1 (Base)": 1.0, "p (pico)": 1e-12, "n (nano)": 1e-9, 
    "µ (micro)": 1e-6, "m (mili)": 1e-3, "k (kilo)": 1e3, 
    "M (mega)": 1e6, "G (giga)": 1e9
}

def entradas(ventana):
    lista_componentes = []
    
    # --- COLA TEMPORAL PARA SERIE ---
    cola_serie = [] 

    frame_global = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_global.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(frame_global, text="Definir Circuito", font=("Helvetica", 24, "bold")).pack(pady=10)

    # --- INPUTS ---
    frame_inputs = ctk.CTkFrame(frame_global)
    frame_inputs.pack(fill="x", pady=10)

    # Fila 1: Selección de Componente
    ctk.CTkLabel(frame_inputs, text="Componente:").grid(row=0, column=0, padx=5, pady=10)
    combo_tipo = ctk.CTkOptionMenu(frame_inputs, values=["Resistencia", "Fuente V", "Fuente I", "Capacitor", "Inductor"], width=120)
    combo_tipo.grid(row=0, column=1, padx=5)

    ctk.CTkLabel(frame_inputs, text="Valor:").grid(row=0, column=2, padx=5)
    entry_valor = ctk.CTkEntry(frame_inputs, width=70)
    entry_valor.grid(row=0, column=3, padx=5)
    
    combo_prefijo = ctk.CTkOptionMenu(frame_inputs, values=list(PREFIJOS.keys()), width=100)
    combo_prefijo.grid(row=0, column=4, padx=5)
    combo_prefijo.set("x1 (Base)")

    # Fila 2: Nodos y Modo Serie
    ctk.CTkLabel(frame_inputs, text="Nodos Extremos (A->B):").grid(row=1, column=0, padx=5, pady=10)
    entry_nA = ctk.CTkEntry(frame_inputs, width=40, placeholder_text="A")
    entry_nA.grid(row=1, column=1, padx=2, sticky="w")
    entry_nB = ctk.CTkEntry(frame_inputs, width=40, placeholder_text="B")
    entry_nB.grid(row=1, column=1, padx=2, sticky="e") # Truco visual para ponerlos juntos

    # SWITCH DE MODO SERIE
    switch_serie = ctk.CTkSwitch(frame_inputs, text="Modo Rama Serie (Multiples componentes)")
    switch_serie.grid(row=1, column=2, columnspan=3, padx=10, pady=10, sticky="w")

    # --- PREVISUALIZACIÓN DE LA COLA (SOLO PARA MODO SERIE) ---
    lbl_preview_serie = ctk.CTkLabel(frame_global, text="Cola Serie: [Vacía]", text_color="gray", anchor="w")
    lbl_preview_serie.pack(fill="x", padx=20)

    # --- BOTONES DE ACCIÓN ---
    frame_botones = ctk.CTkFrame(frame_global, fg_color="transparent")
    frame_botones.pack(fill="x", pady=5)

    frame_lista = ctk.CTkScrollableFrame(frame_global) 
    frame_lista.pack(fill="both", expand=True, pady=5)

    # ================= LÓGICA =================
    
    def obtener_valor_real():
        try:
            val = float(entry_valor.get())
            mult = PREFIJOS[combo_prefijo.get()]
            pref = combo_prefijo.get().split()[0]
            if pref == "x1": pref = ""
            return val * mult, f"{entry_valor.get()}{pref}"
        except:
            return None, None

    def procesar_agregar():
        # 1. Obtener datos del componente actual
        tipo = combo_tipo.get()
        v_real, v_str = obtener_valor_real()
        
        if v_real is None: 
            print("Error: Valor inválido")
            return

        # 2. Verificar en qué modo estamos
        if switch_serie.get() == 1:
            # === MODO SERIE: ACUMULAR ===
            cola_serie.append({
                "tipo": tipo,
                "valor_real": v_real,
                "valor_str": v_str
            })
            # Actualizar etiqueta visual
            resumen = " + ".join([f"{c['tipo'][0]}({c['valor_str']})" for c in cola_serie])
            lbl_preview_serie.configure(text=f"Cola Serie (Pendiente de guardar): {resumen}", text_color="#FFA500") # Naranja
            
            # Limpiar valor para el siguiente, PERO NO LOS NODOS (se usan al final)
            entry_valor.delete(0, 'end')

        else:
            # === MODO SIMPLE (NORMAL) ===
            nA, nB = entry_nA.get(), entry_nB.get()
            if not nA or not nB: return
            
            # Guardar directo
            comp = {
                "tipo": tipo, "valor_real": v_real, "valor_str": v_str,
                "nodoA": nA, "nodoB": nB
            }
            lista_componentes.append(comp)
            mostrar_en_lista(comp)
            entry_valor.delete(0, 'end')

    def finalizar_rama_serie():
        # Verifica que haya algo en la cola y que existan nodos destino
        nA_final = entry_nA.get()
        nB_final = entry_nB.get()

        if not cola_serie or not nA_final or not nB_final:
            return

        print(f"Procesando rama de {len(cola_serie)} elementos entre {nA_final} y {nB_final}")

        # === ALGORITMO DE GENERACIÓN DE NODOS INTERMEDIOS ===
        
        nodo_actual = nA_final # Empezamos en el Nodo A del usuario
        
        for i, comp in enumerate(cola_serie):
            # Determinar cuál es el nodo siguiente
            if i == len(cola_serie) - 1:
                # Si es el último componente, conecta al destino final (B)
                nodo_siguiente = nB_final
            else:
                # Si no, crea un nodo intermedio único
                # Usamos un contador global basado en el total de componentes ya creados para que sea unico
                nodo_siguiente = f"aux_{len(lista_componentes)}_{i}"
            
            # Crear el componente con los nodos calculados
            nuevo_comp = {
                "tipo": comp["tipo"],
                "valor_real": comp["valor_real"],
                "valor_str": comp["valor_str"],
                "nodoA": nodo_actual,       # Conecta del anterior
                "nodoB": nodo_siguiente     # Al nuevo (o final)
            }
            
            lista_componentes.append(nuevo_comp)
            mostrar_en_lista(nuevo_comp, es_rama=True)
            
            # Avanzar: el nodo siguiente se vuelve el actual para el próximo componente
            nodo_actual = nodo_siguiente

        # Limpiar cola y resetear UI
        cola_serie.clear()
        lbl_preview_serie.configure(text="Cola Serie: [Vacía]", text_color="gray")
        entry_valor.delete(0, 'end')

    def mostrar_en_lista(comp, es_rama=False):
        uni = "Ω" if "Resistencia" in comp['tipo'] else "F" if "Capacitor" in comp['tipo'] else "H" if "Inductor" in comp['tipo'] else "V" if "Voltaje" in comp['tipo'] else "A"
        
        # Si es parte de una rama automatica, lo pintamos de otro color o agregamos un icono
        icono = "🔗" if es_rama else "🔹"
        texto = f"{icono} {comp['tipo']} | {comp['valor_str']}{uni} | {comp['nodoA']} -> {comp['nodoB']}"
        ctk.CTkLabel(frame_lista, text=texto, anchor="w").pack(fill="x", padx=10, pady=2)

    # --- BOTONES ---
    
    # Este botón cambia de función visualmente o usamos dos botones
    btn_accion = ctk.CTkButton(frame_botones, text="Agregar Componente", command=procesar_agregar)
    btn_accion.pack(side="left", padx=10, expand=True, fill="x")

    # Botón exclusivo para terminar la serie
    btn_terminar_serie = ctk.CTkButton(frame_botones, text="Guardar Rama", fg_color="#D35400", command=finalizar_rama_serie)
    
    # Lógica para mostrar/ocultar el botón de "Guardar Rama" según el switch
    def toggle_mode():
        if switch_serie.get() == 1:
            btn_terminar_serie.pack(side="left", padx=10)
            btn_accion.configure(text="Agregar Componente")
        else:
            btn_terminar_serie.pack_forget()
            btn_accion.configure(text="Agregar Componente")

    switch_serie.configure(command=toggle_mode)

    btn_ver = ctk.CTkButton(frame_botones, text="Grafo Orientado", fg_color="green", command=lambda: Circuito.circuito(lista_componentes))
    btn_ver.pack(side="right", padx=10)