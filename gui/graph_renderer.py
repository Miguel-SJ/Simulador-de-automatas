# gui/graph_renderer.py
import math
import tkinter as tk

class AutomataRenderer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.radius = 25  # Radio de los círculos de estado

    def render(self, automata):
        self.canvas.delete("all")
        if not automata or not automata.get("estados"):
            return

        estados = automata["estados"]
        # Inyectar el estado pozo si existe en las transiciones pero no en la lista explícita
        if "Ø" not in estados and any("Ø" in str(d) for t in automata["transiciones"].values() for d in t.values()):
            estados.append("Ø")

        n = len(estados)
        # Centrar el grafo en el Canvas
        cx, cy = int(self.canvas['width']) / 2, int(self.canvas['height']) / 2
        layout_radius = min(cx, cy) - 60

        # Calcular posiciones (Distribución Circular)
        posiciones = {}
        for i, estado in enumerate(estados):
            # Ajuste de ángulo para que el primer estado quede arriba a la izquierda
            angle = i * (2 * math.pi / max(n, 1)) + math.pi
            x = cx + layout_radius * math.cos(angle)
            y = cy + layout_radius * math.sin(angle)
            posiciones[estado] = (x, y)

        # 1. Dibujar Transiciones (Aristas)
        transiciones = automata.get("transiciones", {})
        for origen, rutas in transiciones.items():
            for simbolo, destinos in rutas.items():
                if isinstance(destinos, str): destinos = [destinos]
                for destino in destinos:
                    if origen in posiciones and destino in posiciones:
                        self._draw_edge(posiciones[origen], posiciones[destino], simbolo, is_loop=(origen == destino))

        # 2. Dibujar Estados (Nodos) por encima de las aristas
        for estado, (x, y) in posiciones.items():
            is_initial = (estado == automata.get("inicial"))
            is_final = (estado in automata.get("finales", []))
            self._draw_node(x, y, estado, is_initial, is_final)

    def _draw_node(self, x, y, label, is_initial, is_final):
        # Círculo base
        self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill="white", outline="black", width=2)
        
        # Doble círculo (Estado Final)
        if is_final:
            r2 = self.radius - 5
            self.canvas.create_oval(x - r2, y - r2, x + r2, y + r2, outline="black", width=1.5)
        
        # Flecha de entrada al vacío (Estado Inicial)
        if is_initial:
            self.canvas.create_line(x - self.radius - 40, y, x - self.radius, y, arrow=tk.LAST, width=2, fill="green")
        
        # Etiqueta
        self.canvas.create_text(x, y, text=label, font=("Arial", 10, "bold"))

    def _draw_edge(self, p1, p2, label, is_loop=False):
        if is_loop:
            cx, cy = p1
            # Dibujar un arco encima del nodo
            self.canvas.create_oval(cx - 15, cy - self.radius - 35, cx + 15, cy - self.radius, outline="blue", width=1.5)
            self.canvas.create_text(cx, cy - self.radius - 40, text=label, fill="red", font=("Arial", 9, "bold"))
            return

        # Calcular vector de dirección para no superponer la línea en el círculo
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        dist = math.hypot(dx, dy)
        if dist == 0: return

        nx, ny = dx / dist, dy / dist
        sx, sy = p1[0] + nx * self.radius, p1[1] + ny * self.radius
        ex, ey = p2[0] - nx * self.radius, p2[1] - ny * self.radius

        # Dibujar flecha
        self.canvas.create_line(sx, sy, ex, ey, arrow=tk.LAST, fill="blue", width=1.5)
        
        # Posicionar el texto un poco desplazado del centro
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        offset = 12
        self.canvas.create_text(mx - offset*ny, my + offset*nx, text=label, fill="red", font=("Arial", 9, "bold"))