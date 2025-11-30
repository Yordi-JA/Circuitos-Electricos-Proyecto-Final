import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class GrafoInteractivo:
    def __init__(self, ventana, lista_componentes):
        self.ventana = ventana
        
        # Frame para el gráfico
        self.frame_plot = ctk.CTkFrame(ventana, fg_color="white")
        self.frame_plot.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. PREPARACIÓN DE DATOS
        self.G = self.crear_grafo_simplificado(lista_componentes)
        
        # 2. CONFIGURACIÓN MATPLOTLIB
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # 3. ESTADO INICIAL
        # Usamos seed fija para que empiece siempre igual
        self.pos = nx.spring_layout(self.G, seed=42, k=1.5)
        self.nodo_seleccionado = None

        # 4. CONECTAR EVENTOS DEL MOUSE
        # Guardamos los IDs de conexión por seguridad
        self.cid_press = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # Dibujar por primera vez
        self.dibujar()

    def crear_grafo_simplificado(self, lista_componentes):
        G_temp = nx.MultiDiGraph()
        
        # Construir grafo
        for comp in lista_componentes:
            nA, nB = str(comp['nodoA']), str(comp['nodoB'])
            G_temp.add_edge(nA, nB, label=comp['tipo'][0])

        # Eliminar auxiliares
        nodos_aux = [n for n in G_temp.nodes() if "aux" in str(n)]
        while nodos_aux:
            for nodo in nodos_aux:
                if nodo in G_temp:
                    preds = list(G_temp.predecessors(nodo))
                    succs = list(G_temp.successors(nodo))
                    if preds and succs:
                        G_temp.add_edge(preds[0], succs[0], label="Rama")
                        G_temp.remove_node(nodo)
            nodos_aux = [n for n in G_temp.nodes() if "aux" in str(n)]
        
        return G_temp

    def dibujar(self):
        self.ax.clear() 

        # A) Dibujar Nodos
        nx.draw_networkx_nodes(
            self.G, self.pos, ax=self.ax,
            node_color='#3498DB', node_size=800, edgecolors='black'
        )
        
        # B) Etiquetas
        nx.draw_networkx_labels(
            self.G, self.pos, ax=self.ax, 
            font_color="white", font_weight="bold", font_size=10
        )

        # C) Flechas Curvas
        for u, v, key, data in self.G.edges(keys=True, data=True):
            if u not in self.pos or v not in self.pos: continue
            
            xa, ya = self.pos[u]
            xb, yb = self.pos[v]
            rad = 0.15 + (key * 0.15) 
            
            color = "#E74C3C" if "Rama" in data.get('label','') else "black"
            
            self.ax.annotate("",
                xy=(xb, yb), xycoords='data',
                xytext=(xa, ya), textcoords='data',
                arrowprops=dict(
                    arrowstyle="-|>", color=color,
                    shrinkA=18, shrinkB=18,
                    connectionstyle=f"arc3,rad={rad}",
                    lw=2, alpha=0.8
                )
            )

        self.ax.set_title("Grafo orientado", fontsize=12)
        
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect('equal')
        self.ax.axis("off")
        
        self.canvas.draw()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        for nodo, (x, y) in self.pos.items():
            dist = math.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)
            if dist < 0.2: 
                self.nodo_seleccionado = nodo
                return

    def on_motion(self, event):
        if self.nodo_seleccionado is None or event.inaxes != self.ax: return
        self.pos[self.nodo_seleccionado] = (event.xdata, event.ydata)
        self.dibujar()

    def on_release(self, event):
        self.nodo_seleccionado = None


# --- FUNCIÓN PUENTE ---
def circuito(lista_componentes):
    ventana = ctk.CTkToplevel()
    ventana.title("Editor Visual de Topología")
    ventana.geometry("800x650")
    ventana.attributes('-topmost', True)
    
    if not lista_componentes:
        ctk.CTkLabel(ventana, text="Sin datos").pack()
        return

    ventana.app_grafo = GrafoInteractivo(ventana, lista_componentes)

    ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy, fg_color="#FF5555").pack(pady=10)