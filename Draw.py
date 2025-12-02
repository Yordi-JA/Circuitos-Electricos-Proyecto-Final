import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class DraggableGraph:
    def __init__(self, frame, conexiones, callback_editar):
        self.frame = frame
        self.conexiones = conexiones
        self.callback_editar = callback_editar
        
        self.dragging_node = None 
        self.is_panning = False
        self.pan_start_x = None
        self.pan_start_y = None
        
        self.xlim = None
        self.ylim = None

        for widget in self.frame.winfo_children():
            widget.destroy()

        if not self.conexiones:
            self.mostrar_vacio()
            return

        self.setup_style()

        self.fig = plt.figure(figsize=(5, 4), dpi=100, facecolor="#2b2b2b")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#2b2b2b")
        self.ax.axis('off')

        self.G = nx.DiGraph()
        self.G.add_edges_from(self.conexiones)
        
        self.pos = nx.spring_layout(self.G, seed=42)
        
        self.actualizar_limites(force_init=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=10, pady=10, expand=True, fill="both")

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll) 

        self.dibujar()
        self.crear_botones()

    def setup_style(self):
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'

    def mostrar_vacio(self):
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=50, pady=40)

        ctk.CTkLabel(container, text="No hay conexiones.", font=("Helvetica", 16), text_color="white").pack(pady=(20, 30))

        ctk.CTkButton(
            container, text="Volver", command=self.callback_editar,
            width=160, height=35, corner_radius=18, font=("Helvetica", 13, "bold"),
            fg_color="#7167ff", hover_color="#5a52cc"
        ).pack(pady=(0, 20))

    def actualizar_limites(self, force_init=False):
        xs = [coords[0] for coords in self.pos.values()]
        ys = [coords[1] for coords in self.pos.values()]
        
        if not xs or not ys: return

        padding = 0.3 
        min_x, max_x = min(xs) - padding, max(xs) + padding
        min_y, max_y = min(ys) - padding, max(ys) + padding

        if force_init or self.xlim is None:
            self.xlim = [min_x, max_x]
            self.ylim = [min_y, max_y]
        
    def dibujar(self):
        self.ax.clear()
        self.ax.axis('off')
        
        if self.xlim and self.ylim:
            self.ax.set_xlim(self.xlim)
            self.ax.set_ylim(self.ylim)

        try:
            nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color='#7167ff', node_size=500)
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color='white', arrows=True, arrowsize=20, width=1.5)
            nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_color='white', font_weight='bold')
            self.canvas.draw_idle()
        except Exception as e:
            print(f"Error al dibujar: {e}")

    def aplicar_zoom(self, factor):
        if not self.xlim or not self.ylim: return
        width = self.xlim[1] - self.xlim[0]
        height = self.ylim[1] - self.ylim[0]
        cx = (self.xlim[0] + self.xlim[1]) / 2
        cy = (self.ylim[0] + self.ylim[1]) / 2
        new_width = width * factor
        new_height = height * factor
        self.xlim = [cx - new_width / 2, cx + new_width / 2]
        self.ylim = [cy - new_height / 2, cy + new_height / 2]
        self.dibujar()

    def on_scroll(self, event):
        if event.inaxes != self.ax: return
        base_scale = 1.15 
        if event.button == 'up':
            self.aplicar_zoom(1 / base_scale)
        elif event.button == 'down':
            self.aplicar_zoom(base_scale)

    def on_press(self, event):
        if event.xdata is None or event.ydata is None: return
        if event.button != 1: return 

        click_point = (event.xdata, event.ydata)
        min_dist = float('inf')
        closest_node = None
        
        current_width = self.xlim[1] - self.xlim[0]
        dynamic_threshold = current_width * 0.05 

        for node, (nx_x, nx_y) in self.pos.items():
            dist = math.sqrt((nx_x - click_point[0])**2 + (nx_y - click_point[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_node = node

        if closest_node is not None and min_dist < dynamic_threshold:
            self.dragging_node = closest_node
        else:
            self.is_panning = True
            self.pan_start_x = event.xdata
            self.pan_start_y = event.ydata

    def on_motion(self, event):
        if event.xdata is None or event.ydata is None: return

        if self.dragging_node is not None:
            self.pos[self.dragging_node] = (event.xdata, event.ydata)
            self.dibujar()

        elif self.is_panning and self.pan_start_x is not None:
            dx = event.xdata - self.pan_start_x
            dy = event.ydata - self.pan_start_y
            
            self.xlim[0] -= dx
            self.xlim[1] -= dx
            self.ylim[0] -= dy
            self.ylim[1] -= dy
            
            self.dibujar()

    def on_release(self, event):
        self.dragging_node = None
        self.is_panning = False
        self.pan_start_x = None
        self.pan_start_y = None

    def crear_botones(self):
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 15))

        ctk.CTkButton(
            btn_frame, 
            text="Guardar",
            command=lambda: self.fig.savefig("grafo.png", facecolor=self.fig.get_facecolor()),
            fg_color="#7167ff", 
            hover_color="#5a52cc", 
            width=110, 
            height=28
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="-", 
            command=lambda: self.aplicar_zoom(1.2),
            fg_color="#333", hover_color="#222", width=30, height=28
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame, text="+", 
            command=lambda: self.aplicar_zoom(0.8),
            fg_color="#333", hover_color="#222", width=30, height=28
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame, text="Editar Datos", command=self.callback_editar,
            fg_color="#444", hover_color="#333", width=110, height=28
        ).pack(side="left", padx=5)

def dibujar_grafo_en_frame(frame, conexiones, callback_editar):
    frame.grafo_app = DraggableGraph(frame, conexiones, callback_editar)