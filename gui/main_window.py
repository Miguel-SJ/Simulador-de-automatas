# gui/main_window.py
import tkinter as tk
from tkinter import messagebox
from gui.editor_panel import EditorPanel
from gui.graph_renderer import AutomataRenderer
from conversion.subconjuntos import convertir_afnd_a_afd
from expresiones.algebra_arden import obtener_expresion_regular
from modelos.automata import validar_automata

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Gráfico de Autómatas")
        self.geometry("1000x650")
        self.afnd_actual = None
        self.afd_actual = None
        self._build_ui()

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
        toolbar = tk.Frame(right_frame, bg="#e0e0e0", pady=5, padx=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(
            toolbar,
            text="1. AFND a AFD (Subconjuntos)",
            command=self.convertir_a_afd,
            bg="lightgreen",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="2. Generar Expresión Regular (ER)",
            command=self.generar_er,
            bg="#ffd966",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)

        # Panel para mostrar la Expresión Regular resultante
        er_frame = tk.Frame(right_frame, bg="#f9f9f9", pady=8, padx=10, relief=tk.GROOVE, borderwidth=1)
        er_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(er_frame, text="Expresión Regular (ER):", bg="#f9f9f9", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        
        self.var_er = tk.StringVar(value="---")
        self.ent_er_resultado = tk.Entry(
            er_frame,
            textvariable=self.var_er,
            font=("Consolas", 12, "bold"),
            fg="darkblue",
            state="readonly",
            readonlybackground="white"
        )
        self.ent_er_resultado.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Canvas para el grafo
        self.canvas = tk.Canvas(right_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(width=e.width, height=e.height))

        self.renderer = AutomataRenderer(self.canvas)

    def _actualizar_afnd_desde_editor(self):
        """Obtiene y valida siempre los datos más recientes escritos en el panel izquierdo."""
        afnd = self.editor.obtener_modelo_afnd()
        if validar_automata(afnd):
            self.afnd_actual = afnd
            return True
        return False

    def renderizar_afnd(self, afnd):
        self.afnd_actual = afnd
        self.afd_actual = None
        self.var_er.set("---")
        self.renderer.render(afnd)

    def convertir_a_afd(self):
        try:
            # Leemos los datos actuales del formulario para no quedarnos con datos viejos
            if not self._actualizar_afnd_desde_editor():
                return
            
            afd, tabla_pasos = convertir_afnd_a_afd(self.afnd_actual)
            self.afd_actual = afd
            self.renderer.render(afd)
            
            # Calculamos y mostramos también la ER automáticamente al convertir
            er_final, pasos_er = obtener_expresion_regular(afd)
            self.var_er.set(er_final if er_final else "Ø")
            
            messagebox.showinfo("Conversión Exitosa", f"Se ha generado el AFD y su ER:\n{er_final}")
        except Exception as e:
            messagebox.showerror("Error en Conversión", f"Verifica los datos ingresados:\n{e}")

    def generar_er(self):
        try:
            if not self._actualizar_afnd_desde_editor():
                return
            
            # Si aún no se había convertido el AFND actual a AFD, lo convertimos primero
            afd, _ = convertir_afnd_a_afd(self.afnd_actual)
            self.afd_actual = afd
            
            er_final, pasos_er = obtener_expresion_regular(afd)
            self.var_er.set(er_final if er_final else "Ø")
        except Exception as e:
            messagebox.showerror("Error al generar ER", f"Falló el cálculo de la Expresión Regular:\n{e}")