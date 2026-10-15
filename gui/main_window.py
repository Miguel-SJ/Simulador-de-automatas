# gui/main_window.py
import tkinter as tk
from tkinter import messagebox
from gui.editor_panel import EditorPanel
from gui.graph_renderer import AutomataRenderer
from conversion.subconjuntos import convertir_afnd_a_afd

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Gráfico de Autómatas")
        self.geometry("1000x600")
        self._build_ui()
        self.afnd_actual = None

    def _build_ui(self):
        # Panel Izquierdo (Editor)
        left_frame = tk.Frame(self, width=350, bg="#f0f0f0", relief=tk.SUNKEN, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.editor = EditorPanel(left_frame, on_render_callback=self.renderizar_afnd)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho (Visualización)
        right_frame = tk.Frame(self, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Barra de herramientas superior derecha
        toolbar = tk.Frame(right_frame, bg="#e0e0e0", pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(toolbar, text="AFND a AFD (Método Subconjuntos)", command=self.convertir_a_afd, bg="lightgreen", font=("Arial", 10, "bold")).pack()

        # Canvas para el grafo
        self.canvas = tk.Canvas(right_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Ajustar dinámicamente al cambiar el tamaño de la ventana
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(width=e.width, height=e.height))

        self.renderer = AutomataRenderer(self.canvas)

    def renderizar_afnd(self, afnd):
        self.afnd_actual = afnd
        self.renderer.render(afnd)

    def convertir_a_afd(self):
        if not self.afnd_actual:
            messagebox.showwarning("Aviso", "Primero debes configurar y dibujar un AFND.")
            return
        
        try:
            # Lógica pura inyectada desde la Fase 2 (sin modificarla)
            afd, tabla_pasos = convertir_afnd_a_afd(self.afnd_actual)
            # Dibujamos el AFD resultante reutilizando el motor gráfico
            self.renderer.render(afd)
            messagebox.showinfo("Conversión Exitosa", "Se ha generado el AFD. El grafo ha sido actualizado.")
        except Exception as e:
            messagebox.showerror("Error en Conversión", f"Falló el algoritmo matemático:\n{e}")