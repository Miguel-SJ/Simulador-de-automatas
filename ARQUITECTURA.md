# Arquitectura del Simulador y Verificador de Autómatas Finitos

## 1. Plan de arquitectura

### Organización y comunicación de módulos

El sistema utilizará una arquitectura basada en capas, separando la lógica de dominio de la capa de presentación. La comunicación entre módulos se realizará mediante estructuras de datos de Python, principalmente diccionarios que representan los autómatas.

### Responsabilidades

- **Capa de dominio:** contiene los algoritmos matemáticos y las operaciones de conversión, generación de expresiones regulares y verificación de equivalencia.
- **Capa de presentación:** utiliza Tkinter para capturar datos, dibujar grafos, mostrar tablas y presentar el paso a paso de los algoritmos.

### Separación entre interfaz y lógica

Ningún archivo de la lógica matemática importará `tkinter`. La interfaz gráfica se encargará de recibir los datos del usuario, enviarlos a los módulos correspondientes y mostrar los resultados obtenidos.

### Manejo de errores y validaciones

El modelo de datos validará los autómatas antes de ejecutar los algoritmos. Si se encuentra una inconsistencia, como una transición con un símbolo que no pertenece al alfabeto, se generará una excepción de Python. La interfaz gráfica capturará estos errores y mostrará mensajes comprensibles al usuario.

### Pruebas independientes

Se utilizará `unittest` para comprobar los algoritmos sin necesidad de abrir ventanas gráficas. Las pruebas utilizarán autómatas de ejemplo y verificarán los resultados de las conversiones, las expresiones regulares y la equivalencia de los lenguajes.

## 2. Estructura de carpetas

```text
simulador_automatas/
│
├── app.py
├── README.md
├── SPEC.md
├── ARQUITECTURA.md
│
├── gui/
│   ├── main_window.py
│   ├── editor_panel.py
│   ├── graph_renderer.py
│   └── step_viewer.py
│
├── modelos/
│   └── automata.py
│
├── conversion/
│   └── subconjuntos.py
│
├── expresiones/
│   ├── ecuaciones.py
│   └── algebra_arden.py
│
├── verificador/
│   └── probador_cadenas.py
│
└── pruebas/
    ├── test_conversion.py
    ├── test_expresiones.py
    └── test_verificador.py
```

### Descripción de los archivos y carpetas

| Archivo o carpeta | Responsabilidad |
|---|---|
| `app.py` | Punto de entrada de la aplicación e inicialización de Tkinter. |
| `README.md` | Instrucciones de instalación, ejecución y uso. |
| `SPEC.md` | Requisitos técnicos y funcionales del proyecto. |
| `ARQUITECTURA.md` | Documentación de la arquitectura y las decisiones técnicas. |
| `gui/` | Componentes de la interfaz gráfica. |
| `main_window.py` | Ventana principal y organización de los módulos visuales. |
| `editor_panel.py` | Formularios para ingresar los datos del AFND. |
| `graph_renderer.py` | Dibujo de estados y transiciones mediante Canvas. |
| `step_viewer.py` | Presentación de tablas, ecuaciones y pasos de los algoritmos. |
| `modelos/automata.py` | Representación y validación de los autómatas. |
| `conversion/subconjuntos.py` | Conversión de AFND a AFD y generación de la tabla de transiciones. |
| `expresiones/ecuaciones.py` | Construcción del sistema de ecuaciones regulares. |
| `expresiones/algebra_arden.py` | Resolución de ecuaciones mediante sustitución y el lema de Arden. |
| `verificador/probador_cadenas.py` | Generación de cadenas y comparación de resultados entre los modelos. |
| `pruebas/` | Pruebas unitarias automatizadas. |
| `test_conversion.py` | Pruebas del algoritmo de conversión. |
| `test_expresiones.py` | Pruebas de la generación de expresiones regulares. |
| `test_verificador.py` | Pruebas de equivalencia entre los autómatas y las expresiones regulares. |

## 3. Modelo de datos del autómata

Se utilizará un modelo de datos unificado basado en diccionarios de Python para representar tanto los autómatas finitos no deterministas (AFND) como los autómatas finitos deterministas (AFD).

### Ejemplo de estructura

```json
{
  "estados": ["q0", "q1", "q2"],
  "alfabeto": ["a", "b"],
  "inicial": "q0",
  "finales": ["q2"],
  "transiciones": {
    "q0": {
      "a": ["q0", "q1"],
      "b": []
    },
    "q1": {
      "a": [],
      "b": ["q2"]
    },
    "q2": {
      "a": [],
      "b": []
    }
  }
}
```

### Descripción de los campos

- `estados`: lista de estados que componen el autómata.
- `alfabeto`: lista de símbolos permitidos para las transiciones.
- `inicial`: estado desde el cual comienza el procesamiento.
- `finales`: lista de estados de aceptación.
- `transiciones`: diccionario que relaciona cada estado y símbolo con una lista de estados de destino.

### Identificación de estados en el AFD

Para representar los subconjuntos generados durante la conversión, los nombres de los estados compuestos se construirán ordenando los estados originales y uniéndolos mediante comas.

Por ejemplo, el subconjunto `{q0, q1}` se representará como `"q0,q1"`. De esta manera, los subconjuntos equivalentes conservarán una representación consistente.

### Estado pozo

Cuando una transición no tenga estados de destino, se utilizará el estado `"Ø"` para representar el conjunto vacío. Este estado tendrá transiciones hacia sí mismo para todos los símbolos del alfabeto.

## 4. Flujo de datos entre módulos

El flujo de información será secuencial, desde la entrada de los datos hasta la verificación de equivalencia.

1. **Entrada de datos:** la interfaz gráfica captura los estados, el alfabeto, el estado inicial, los estados finales y las transiciones del AFND.
2. **Conversión de AFND a AFD:** el módulo de subconjuntos recibe el AFND y devuelve el AFD, la tabla de transiciones y los pasos de la conversión.
3. **Generación de expresiones regulares:** el módulo de expresiones recibe el AFD, construye el sistema de ecuaciones y obtiene una expresión regular mediante el lema de Arden.
4. **Verificación de equivalencia:** el verificador recibe el AFND, el AFD, la expresión regular y la longitud máxima de las cadenas que se evaluarán.
5. **Presentación de resultados:** la interfaz muestra los resultados de las conversiones y el informe de verificación.

### Diagrama de flujo

```text
[ Interfaz gráfica ]
        |
        v
[ Entrada del AFND ]
        |
        v
[ M1: Construcción por subconjuntos ]
        |
        +------> Tabla de transiciones
        |
        v
[ Modelo AFD ]
        |
        v
[ M2: Sistema de ecuaciones y lema de Arden ]
        |
        v
[ Expresión regular ]
        |
        v
[ M3: Verificador de equivalencia ]
        ^
        |
[ AFND + AFD + ER + longitud máxima N ]
        |
        v
[ Informe de resultados ]
        |
        v
[ Interfaz gráfica ]
```

## 5. Decisiones técnicas y casos límite

### Estados inalcanzables

El algoritmo de conversión comenzará desde el estado inicial y explorará únicamente los estados alcanzables mediante las transiciones del autómata. Los estados que no se alcancen no se incluirán en el AFD generado.

### Estado pozo

Cuando una transición produzca un conjunto vacío de destinos, se incorporará el estado `"Ø"`. Este estado tendrá transiciones hacia sí mismo para cada símbolo del alfabeto.

### Alfabeto de un solo símbolo

Los algoritmos recorrerán el alfabeto mediante iteraciones, sin depender de una cantidad fija de símbolos. Esto permitirá trabajar con alfabetos de diferentes tamaños.

### Cadenas vacías

El verificador incluirá la cadena vacía, de longitud cero, en sus pruebas. Además, el sistema de ecuaciones deberá contemplar que el estado inicial sea también un estado final.

### Autómatas con ciclos

El módulo de expresiones regulares resolverá las ecuaciones mediante sustitución y el lema de Arden, considerando los ciclos y las dependencias entre estados.

### Verificación de expresiones regulares

Se evaluará si las cadenas generadas pertenecen al lenguaje definido por la expresión regular. Si se utiliza la librería `re` de Python, será necesario traducir correctamente la sintaxis de las expresiones regulares del proyecto a la sintaxis de Python y evitar que las cadenas coincidan solo parcialmente.

### Transiciones inválidas

El modelo validará que los estados de origen y destino existan, que los símbolos pertenezcan al alfabeto y que el estado inicial y los estados finales sean válidos. Si se detectan inconsistencias, se generará un error antes de ejecutar los algoritmos.

## 6. Plan de implementación

El desarrollo se realizará de abajo hacia arriba, implementando y verificando primero la lógica antes de construir la interfaz gráfica.

### Etapa 1. Modelo de datos

- Crear el modelo del autómata.
- Implementar validaciones de estados, alfabeto y transiciones.
- Crear pruebas para comprobar que se detectan datos inválidos.

**Criterio de aceptación:** el modelo rechaza autómatas inconsistentes.

### Etapa 2. Conversión de AFND a AFD

- Implementar el algoritmo de construcción por subconjuntos.
- Generar la tabla de transiciones.
- Manejar estados inalcanzables y el estado pozo.

**Criterio de aceptación:** las pruebas comprueban que la conversión produce un AFD correcto y equivalente al AFND de entrada.

### Etapa 3. Generación de expresiones regulares

- Construir el sistema de ecuaciones regulares.
- Implementar las operaciones algebraicas necesarias.
- Resolver las ecuaciones mediante sustitución y el lema de Arden.
- Registrar los pasos de la resolución.

**Criterio de aceptación:** las expresiones generadas representan el lenguaje del autómata en los casos de prueba.

### Etapa 4. Verificador de equivalencia

- Generar cadenas desde longitud cero hasta la longitud máxima establecida.
- Evaluar las cadenas en el AFND y el AFD.
- Evaluar las mismas cadenas en la expresión regular.
- Comparar los resultados y generar un informe.

**Criterio de aceptación:** todas las cadenas verificadas producen resultados coincidentes entre los tres modelos.

### Etapa 5. Interfaz gráfica

- Crear la ventana principal con Tkinter.
- Incorporar los formularios para ingresar autómatas.
- Dibujar estados y transiciones.
- Mostrar las tablas y los resultados de cada módulo.

**Criterio de aceptación:** la aplicación abre correctamente y permite ingresar y visualizar un autómata.

### Etapa 6. Visualización paso a paso

- Mostrar las etapas de la conversión por subconjuntos.
- Presentar las ecuaciones y las reglas aplicadas por el lema de Arden.
- Permitir avanzar por los pasos de cada algoritmo.

**Criterio de aceptación:** el usuario puede consultar los pasos intermedios y comprender cómo se obtienen los resultados.

## 7. Decisiones pendientes de aprobación

Antes de implementar la solución, el equipo deberá confirmar:

1. La utilización de un modelo de datos unificado mediante diccionarios.
2. La representación de estados compuestos mediante nombres ordenados y separados por comas.
3. La utilización del estado `"Ø"` para representar el conjunto vacío.
4. El uso de `re` de Python para evaluar las expresiones regulares o la implementación de un evaluador propio.
5. El desarrollo por etapas, comenzando por el modelo de datos y los algoritmos antes de construir la interfaz gráfica.

## 8. Criterios generales de aceptación

El proyecto deberá cumplir las siguientes condiciones:

- Los módulos matemáticos estarán separados de la interfaz gráfica.
- La conversión de AFND a AFD producirá resultados correctos.
- La generación de expresiones regulares contemplará los casos especiales definidos en los requisitos.
- El verificador comparará el comportamiento de los tres modelos.
- Las pruebas automáticas cubrirán los casos definidos en el Anexo A.
- La interfaz gráfica permitirá ingresar autómatas y consultar los resultados.
- La aplicación funcionará de manera local, sin depender de servicios externos.
- Los resultados se comprobarán mediante pruebas automáticas y ejemplos de referencia antes de considerar terminada cada etapa.
