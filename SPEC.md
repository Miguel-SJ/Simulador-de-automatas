## Simulador y Verificador de Autómatas Finitos

### 1. Visión General y Restricciones Tecnológicas

- **Lenguaje:** Python 3.x.
- **Interfaz gráfica:** `tkinter`, utilizando la librería estándar de Python.
- **Lógica computacional:** Librería estándar de Python, incluyendo módulos como `itertools`, `re` y `collections` cuando sean necesarios.
- **Arquitectura:** Aplicación de escritorio monolítica, ejecutada desde `app.py`, con un hilo principal para la interfaz gráfica.
- **Conectividad:** Funcionamiento 100 % offline. No se utilizarán conexiones a internet, APIs externas ni arquitecturas cliente-servidor.
- **Separación de responsabilidades:** La lógica de los algoritmos deberá mantenerse separada de la interfaz gráfica para facilitar las pruebas y el mantenimiento del sistema.

---

### 2. Requisitos Funcionales

#### 2.1. Módulo 1: Conversión de AFND a AFD

- **Ingreso de datos:** La interfaz deberá permitir ingresar los estados, el alfabeto, el estado inicial, los estados finales y las transiciones de un Autómata Finito No Determinista (AFND).
- **Validación de datos:** Se deberá verificar que los estados, el alfabeto, el estado inicial, los estados finales y las transiciones sean coherentes con la definición del autómata.
- **Algoritmo de conversión:** Se implementará el método de construcción por subconjuntos para convertir el AFND en un Autómata Finito Determinista (AFD).
- **Representación de estados:** Cada estado del AFD representará un subconjunto de estados del AFND original. Para identificarlos, se utilizará una etiqueta legible y única, evitando confusiones entre subconjuntos diferentes.
- **Visualización:** Se deberá representar el autómata original y el resultante mediante `tkinter.Canvas`, utilizando círculos para los estados y flechas dirigidas para las transiciones.
- **Tabla de transiciones:** Se mostrará una tabla con los estados del AFD y sus transiciones para cada símbolo del alfabeto.
- **Modo paso a paso:** El sistema deberá mostrar el estado o subconjunto evaluado, el símbolo procesado y el conjunto de destino obtenido en cada iteración.
- **Estados finales:** Un estado del AFD será final cuando su subconjunto contenga al menos un estado final del AFND original.

#### 2.2. Módulo 2: Autómata Finito a Expresión Regular (AF a ER)

- **Punto de entrada:** Recibirá el AFD generado por el Módulo 1.
- **Identificación de estados accesibles:** El motor recorrerá el grafo desde el estado inicial para identificar los estados que pueden alcanzarse mediante las transiciones.
- **Generación de ecuaciones:** Se construirá un sistema de ecuaciones que represente los caminos de aceptación del autómata. Las ecuaciones podrán contener expresiones como `aR1`, `bR2`, uniones de expresiones y la cadena vacía `λ` cuando corresponda.
- **Resolución algebraica:** Se aplicarán sustituciones y el Lema de Arden para despejar las ecuaciones y obtener una expresión regular equivalente al autómata.
- **Condición del Lema de Arden:** Para una ecuación de la forma `R = Q + RP`, se podrá obtener `R = QP*` cuando `P` no contenga la cadena vacía `λ`. Si se utiliza una forma algebraica diferente, se deberá aplicar la regla correspondiente con sus condiciones.
- **Trazabilidad:** Se mostrará cada paso del despeje algebraico, la regla aplicada y el resultado intermedio hasta obtener la expresión regular final.
- **Resultado:** Se entregará una cadena de texto con la expresión regular equivalente, utilizando una notación consistente para la unión, la concatenación, la estrella de Kleene y la cadena vacía.

#### 2.3. Módulo 3: Verificador de Equivalencia

- **Generador de cadenas:** Generará todas las cadenas posibles del alfabeto hasta una longitud máxima `N`, configurable por el usuario.
- **Inclusión de la cadena vacía:** El generador deberá incluir `λ`, representada computacionalmente como `""`, correspondiente a la cadena de longitud cero.
- **Validación en paralelo:** Cada cadena generada se evaluará en los tres modelos:
  1. AFND original.
  2. AFD obtenido mediante la conversión.
  3. Expresión regular generada por el Módulo 2.
- **Evaluación del AFND:** Una cadena será aceptada si existe al menos un recorrido válido que termine en un estado final después de consumir todos sus símbolos.
- **Evaluación del AFD:** Una cadena será aceptada si, después de procesar todos sus símbolos, el autómata termina en un estado final.
- **Evaluación de la expresión regular:** La expresión regular deberá evaluarse sobre la cadena completa, sin aceptar coincidencias parciales. Se deberá contemplar la diferencia entre la notación matemática utilizada por el Módulo 2 y la sintaxis admitida por el motor de expresiones regulares de Python.
- **Reporte:** El sistema mostrará el número de cadenas probadas y el resultado de la verificación. Si encuentra una discrepancia, deberá informar la cadena exacta que produjo el fallo y los resultados de cada modelo.
- **Finalización:** La verificación podrá detenerse al encontrar la primera discrepancia. Si todas las cadenas generadas producen el mismo resultado, se informará que no se encontraron discrepancias dentro del límite probado.

---

### 3. Estructuras de Datos (Entradas y Salidas)

#### 3.1. Estructura de Entrada (Modelo Interno del Autómata)

El modelo de datos central será un diccionario estándar de Python. Esto permitirá trabajar con el autómata en memoria y facilitará su serialización a JSON sin utilizar librerías de terceros.

La estructura de entrada para representar un AFND será la siguiente:

```python
{
    "estados": ["q0", "q1", "q2"],
    "alfabeto": ["a", "b"],
    "inicial": "q0",
    "finales": ["q1"],
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

**Descripción de los campos:**

- `estados`: Lista de identificadores de los estados del autómata.
- `alfabeto`: Lista de símbolos que pueden utilizarse para las transiciones.
- `inicial`: Identificador del estado inicial.
- `finales`: Lista de estados de aceptación.
- `transiciones`: Diccionario que relaciona cada estado con los símbolos del alfabeto y sus correspondientes estados de destino.

En el AFND, una transición podrá conducir a varios estados o a ninguno. Por ello, los valores de las transiciones serán listas de estados.

Para esta especificación, las transiciones se definen sobre símbolos individuales del alfabeto. Las transiciones epsilon o `λ` no forman parte de la entrada definida para este proyecto.

#### 3.2. Salidas Esperadas

- **Del Módulo 1:** Un diccionario que represente el AFD resultante. Cada estado representará un subconjunto de estados del AFND original y cada transición tendrá un único estado de destino por símbolo del alfabeto. Se actualizará el objeto `Canvas` para visualizar el autómata convertido y se mostrará su tabla de transiciones.
- **Del Módulo 2:** Una cadena de texto con la expresión regular equivalente al autómata y un arreglo de cadenas (`list[str]`) que contenga la bitácora paso a paso del proceso algebraico.
- **Del Módulo 3:** Un resumen de texto con el número de cadenas probadas y el resultado de la verificación. El formato esperado será: `Total cadenas probadas: X. Equivalencia: EXITOSA/FALLIDA`. En caso de fallo, se incluirá la cadena que causó la discrepancia y el resultado obtenido por cada modelo.

---

### 4. Manejo de Casos Límite

#### 4.1. Estado Pozo

- Cuando el procesamiento de un subconjunto de estados con un símbolo del alfabeto produzca un conjunto vacío, el sistema deberá representar dicho resultado mediante un estado pozo identificado como `Ø`.
- El estado pozo deberá contar con una transición hacia sí mismo para cada símbolo del alfabeto.
- Si el estado pozo ya fue creado, deberá reutilizarse en lugar de generar duplicados.
- El estado pozo no será final, salvo que una regla explícita de la aplicación establezca lo contrario. Para la construcción por subconjuntos definida en este documento, el conjunto vacío no contiene estados finales y, por tanto, no es un estado de aceptación.
- La tabla de transiciones deberá reflejar todas las transiciones del estado pozo.

#### 4.2. Estados Inalcanzables

- **Módulo 1:** El algoritmo de construcción por subconjuntos deberá comenzar desde el subconjunto que contiene únicamente al estado inicial del AFND y procesar iterativamente los nuevos subconjuntos encontrados. De esta manera, solo se generarán estados del AFD alcanzables desde el estado inicial.
- **Módulo 2:** El motor deberá recorrer el grafo del AFD desde su estado inicial y generar las ecuaciones necesarias únicamente para los estados accesibles. Los estados inaccesibles no deberán incorporarse al sistema de ecuaciones.
- La identificación de estados accesibles deberá evitar procesamientos repetidos y prevenir ciclos infinitos durante los recorridos del grafo.

#### 4.3. Alfabetos de un Solo Símbolo

- La lógica de iteración deberá funcionar con cualquier cantidad de símbolos en el alfabeto.
- Los bucles deberán recorrer directamente los elementos del alfabeto, por ejemplo, mediante `for char in alfabeto`, sin depender de índices fijos como `alfabeto[0]` o `alfabeto[1]`.
- El generador de cadenas deberá funcionar correctamente cuando el alfabeto tenga un único símbolo. Para el alfabeto `["a"]`, las cadenas generadas serán `""`, `"a"`, `"aa"`, `"aaa"` y así sucesivamente hasta la longitud máxima configurada.
- La generación de cadenas deberá funcionar también cuando el alfabeto contenga varios símbolos, sin modificar la lógica principal del verificador.
- Si se permite un alfabeto vacío, el sistema deberá definir explícitamente su comportamiento: únicamente podrá generarse la cadena vacía. Si el sistema requiere al menos un símbolo, deberá rechazar la entrada mediante una validación.

---

### 5. Criterios de Aceptación (Verificación Teórica)

Para comprobar la lógica computacional antes de integrarla con la interfaz gráfica, se realizarán pruebas de escritorio con los siguientes escenarios.

#### Criterio 1: Prueba del Estado Pozo

**Escenario**

Se define un AFND con las siguientes características:

- Alfabeto: \(\Sigma = \{a, b\}\).
- Estados: \(Q = \{q_0\}\).
- Estado inicial: \(q_0\).
- Estados finales: \(F = \{q_0\}\).
- Transiciones: \(q_0\) tiene una transición hacia sí mismo al leer `a`, pero no tiene una transición definida para `b`.

**Validación teórica**

1. El Módulo 1 deberá generar el estado inicial del AFD a partir del subconjunto \(\{q_0\}\).
2. La transición de \(\{q_0\}\) con el símbolo `a` deberá conducir a \(\{q_0\}\).
3. La transición de \(\{q_0\}\) con el símbolo `b` deberá conducir al conjunto vacío, representado por el estado pozo `Ø`.
4. El estado `Ø` deberá tener transiciones hacia sí mismo tanto con `a` como con `b`.
5. El estado pozo no deberá ser final.
6. El Módulo 2 deberá producir una expresión regular equivalente a `a*`, que representa todas las cadenas formadas por cero o más repeticiones del símbolo `a`.
7. El Módulo 3 deberá comprobar que las cadenas `""`, `"a"`, `"aa"` y `"aaa"` son aceptadas por los tres modelos, mientras que las cadenas `"b"`, `"ab"` y `"ba"` son rechazadas por los tres modelos.

**Resultado esperado:** La conversión deberá ser determinista y completa, y los tres modelos deberán coincidir en las cadenas evaluadas.

#### Criterio 2: Prueba de Alfabeto de un Solo Símbolo

**Escenario**

Se define un autómata con las siguientes características:

- Alfabeto: \(\Sigma = \{x\}\).
- Estados: \(Q = \{q_0, q_1\}\).
- Estado inicial: \(q_0\).
- Estado final: \(F = \{q_1\}\).
- Transiciones: \(q_0\) va a \(q_1\) leyendo `x`, y \(q_1\) va a sí mismo leyendo `x`.

**Validación teórica**

1. El Módulo 1 deberá realizar la conversión sin producir errores de índice fuera de rango.
2. La tabla del AFD deberá incluir una columna para el estado evaluado y una columna para la transición con el símbolo `x`.
3. El Módulo 3 deberá generar, para una longitud máxima de `N = 6`, las siguientes cadenas:

   - `""` (cadena vacía, \(\lambda\)).
   - `"x"`.
   - `"xx"`.
   - `"xxx"`.
   - `"xxxx"`.
   - `"xxxxx"`.
   - `"xxxxxx"`.

4. La cadena vacía deberá ser rechazada por los tres modelos, ya que el estado inicial no es final.
5. Todas las cadenas desde `"x"` hasta `"xxxxxx"` deberán ser aceptadas por los tres modelos.
6. El Módulo 2 deberá producir una expresión regular equivalente a `xx*`, que representa una o más repeticiones del símbolo `x`.
7. El generador deberá poder producir las cadenas de prueba sin depender de índices fijos ni de permutaciones específicas para alfabetos de varios símbolos.

**Resultado esperado:** Los tres modelos deberán coincidir para todas las cadenas generadas hasta la longitud máxima configurada.

---

### 6. Consideraciones de Implementación y Verificación

- La lógica de los tres módulos deberá poder probarse de manera independiente de la interfaz gráfica.
- Los resultados intermedios de los algoritmos deberán mantenerse en estructuras de datos claras y consistentes.
- Las etiquetas de los estados del AFD deberán ser únicas y no deberán confundirse con identificadores de estados originales.
- La expresión regular generada deberá conservar su significado al convertirse al formato utilizado por el evaluador de Python.
- El verificador deberá comparar los resultados de aceptación de los tres modelos para cada cadena probada.
- Una verificación exitosa indicará que no se encontraron discrepancias en el conjunto finito de cadenas generado hasta la longitud máxima seleccionada. Esto no constituye, por sí solo, una demostración matemática de equivalencia para todas las cadenas posibles.
- Las pruebas de aceptación deberán realizarse primero sobre la lógica computacional y posteriormente sobre su integración con `tkinter`.
