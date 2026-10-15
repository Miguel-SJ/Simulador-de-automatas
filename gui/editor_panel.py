# gui/editor_panel.py
import tkinter as tk
from tkinter import messagebox
from modelos.automata import validar_automata

class EditorPanel(tk.Frame):
    def __init__(self, parent, on_render_callback):
        super().__init__(parent)
        self.on_render_callback = on_render_callback
        self.config(padx=10, pady=10)
        self._build_ui()

    def _build_ui(self):
        # Campos básicos
        tk.Label(self, text="Estados (ej: q0,q1,q2):").grid(row=0, column=0, sticky="w")
        self.ent_estados = tk.Entry(self, width=30)
        self.ent_estados.grid(row=0, column=1, pady=2)

        tk.Label(self, text="Alfabeto (ej: a,b):").grid(row=1, column=0, sticky="w")
        self.ent_alfabeto = tk.Entry(self, width=30)
        self.ent_alfabeto.grid(row=1, column=1, pady=2)

        tk.Label(self, text="Estado Inicial (ej: q0):").grid(row=2, column=0, sticky="w")
        self.ent_inicial = tk.Entry(self, width=30)
        self.ent_inicial.grid(row=2, column=1, pady=2)

        tk.Label(self, text="Estados Finales (ej: q2):").grid(row=3, column=0, sticky="w")
        self.ent_finales = tk.Entry(self, width=30)
        self.ent_finales.grid(row=3, column=1, pady=2)

        # Transiciones
        frame_trans = tk.LabelFrame(self, text="Transiciones", padx=5, pady=5)
        frame_trans.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        tk.Label(frame_trans, text="Origen").grid(row=0, column=0)
        tk.Label(frame_trans, text="Símbolo").grid(row=0, column=1)
        tk.Label(frame_trans, text="Destino").grid(row=0, column=2)

        self.ent_origen = tk.Entry(frame_trans, width=8)
        self.ent_origen.grid(row=1, column=0)
        self.ent_simbolo = tk.Entry(frame_trans, width=8)
        self.ent_simbolo.grid(row=1, column=1)
        self.ent_destino = tk.Entry(frame_trans, width=8)
        self.ent_destino.grid(row=1, column=2)

        tk.Button(frame_trans, text="Agregar", command=self.agregar_transicion).grid(row=1, column=3, padx=5)

        self.list_trans = tk.Listbox(frame_trans, height=6)
        self.list_trans.grid(row=2, column=0, columnspan=3, pady=5, sticky="ew")
        
        tk.Button(frame_trans, text="Eliminar Seleccionada", command=self.eliminar_transicion).grid(row=2, column=3, padx=5)

        # Botones de Acción
        tk.Button(self, text="Cargar Caso 1 (Clase)", command=self.cargar_ejemplo).grid(row=5, column=0, pady=10)
        tk.Button(self, text="Dibujar AFND", command=self.renderizar, bg="lightblue").grid(row=5, column=1, pady=10)

    def agregar_transicion(self):
        origen = self.ent_origen.get().strip()
        simbolo = self.ent_simbolo.get().strip()
        destino = self.ent_destino.get().strip()
        if origen and simbolo and destino:
            self.list_trans.insert(tk.END, f"{origen} --({simbolo})--> {destino}")
            self.ent_destino.delete(0, tk.END)

    def eliminar_transicion(self):
        seleccion = self.list_trans.curselection()
        if seleccion:
            self.list_trans.delete(seleccion)

    def obtener_modelo_afnd(self):
        estados = [s.strip() for s in self.ent_estados.get().split(",") if s.strip()]
        alfabeto = [s.strip() for s in self.ent_alfabeto.get().split(",") if s.strip()]
        inicial = self.ent_inicial.get().strip()
        finales = [s.strip() for s in self.ent_finales.get().split(",") if s.strip()]

        transiciones = {}
        for item in self.list_trans.get(0, tk.END):
            partes = item.split(" --(")
            origen = partes[0]
            simbolo = partes[1].split(")--> ")[0]
            destino = partes[1].split(")--> ")[1]

            if origen not in transiciones:
                transiciones[origen] = {}
            if simbolo not in transiciones[origen]:
                transiciones[origen][simbolo] = []
            if destino not in transiciones[origen][simbolo]:
                transiciones[origen][simbolo].append(destino)

        afnd = {
            "estados": estados,
            "alfabeto": alfabeto,
            "inicial": inicial,
            "finales": finales,
            "transiciones": transiciones
        }
        return afnd

    def renderizar(self):
        try:
            afnd = self.obtener_modelo_afnd()
            if validar_automata(afnd):
                self.on_render_callback(afnd)
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))

    def cargar_ejemplo(self):
        self.ent_estados.delete(0, tk.END); self.ent_estados.insert(0, "q0,q1,q2")
        self.ent_alfabeto.delete(0, tk.END); self.ent_alfabeto.insert(0, "a,b")
        self.ent_inicial.delete(0, tk.END); self.ent_inicial.insert(0, "q0")
        self.ent_finales.delete(0, tk.END); self.ent_finales.insert(0, "q2")
        self.list_trans.delete(0, tk.END)
        for t in ["q0 --(a)--> q0", "q0 --(a)--> q1", "q1 --(b)--> q2"]:
            self.list_trans.insert(tk.END, t)