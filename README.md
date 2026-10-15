# Simulador y verificador de autómatas finitos

Aplicación gráfica de escritorio desarrollada en Python que permite simular, convertir, obtener expresiones regulares y verificar formalmente autómatas finitos mediante una interfaz interactiva con explicación paso a paso.

---

## Funcionalidades Principales

1. **Editor y renderizador gráfico de autómatas:**
   - Creación y edición de la 5-tupla de un AFND ($Q, \Sigma, q_0, F, \delta$)
   - Dibujo automático de grafos en `Tkinter Canvas` siguiendo la notación estándar de clase (óvalos, doble círculo en finales, flecha al aire para el estado inicial y bucles dirigidos).
2. **Módulo 1: Conversión de AFND a AFD:**
   - Algoritmo de construcción por subconjuntos
   - Creación y manejo dinámico del Estado Pozo ($\emptyset$)
   - Traza paso a paso detallando la unión de transiciones por subconjunto
3. **Módulo 2: Autómata finito a expresión Regular (AF a ER):**
   - Eliminación de estados mediante el Grafo Autómata Finito Generalizado (GNFA)
   - Aplicación estricta del **Lema de Arden** ($R = Q + RP \implies R = QP^*$) y sustitución algebraica
   - Traza analítica indicando la regla matemática empleada en cada iteración
4. **Módulo 3: Verificador de equivalencia:**
   - Generación exhaustiva de cadenas sobre $\Sigma^*$ hasta una longitud $N$ configurable ($N \ge 6$)
   - Evaluación tripartita en paralelo (AFND vs. AFD vs. ER)
   - Reporte inmediato de coincidencias y resaltado de la primera cadena divergente

---

## Requisitos del Sistema

- **Lenguaje:** Python 3.10 o superior
- **Interfaz gráfica:** `tkinter` (Incluido en la instalación estándar de Python)
- **Librerías externa:** Utiliza exclusivamente módulos nativos de la librería estándar (`math`, `re`, `itertools`, `unittest`, `sys`, `os`)
- **No requiere conexión a internet**

---

## Instalación y ejecución

1. **Extraer el repositorio:**

2. **Ejecutar la aplicación:**
   Abre una terminal o consola de comandos en la carpeta raíz del proyecto y ejecuta:

   ```bash
   python app.py
