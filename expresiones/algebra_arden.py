# expresiones/algebra_arden.py

def _union(a, b):
    if a == "Ø" or a == "": return b
    if b == "Ø" or b == "": return a
    if a == b: return a
    a_clean = "λ" if a == "" else a
    b_clean = "λ" if b == "" else b
    return f"({a_clean}+{b_clean})"

def _concat(a, b):
    if a == "Ø" or b == "Ø": return "Ø"
    if a == "" or a == "λ": return b
    if b == "" or b == "λ": return a
    return f"{a}{b}"

def _kleene(a):
    if a == "Ø" or a == "" or a == "λ": return ""
    if len(a) == 1 or (a.startswith("(") and a.endswith(")")):
        return f"{a}*"
    return f"({a})*"

def obtener_expresion_regular(afd):
    """
    Convierte un AFD en Expresión Regular utilizando el método de eliminación
    de estados (basado en el Lema de Arden / GNFA).
    """
    # 1. Recopilar todos los nodos internos (incluyendo 'Ø' si existe en transiciones)
    nodos_internos = list(afd["estados"])
    for q, trans_q in afd["transiciones"].items():
        if q not in nodos_internos:
            nodos_internos.append(q)
        for sim, dest in trans_q.items():
            if dest not in nodos_internos:
                nodos_internos.append(dest)

    # Nodos super inicial y final
    S = "S_SUPER"
    F = "F_SUPER"
    todos_los_nodos = [S] + nodos_internos + [F]

    # 2. Inicializar matriz de transiciones (garantiza cero KeyErrors)
    W = {u: {v: "Ø" for v in todos_los_nodos} for u in todos_los_nodos}

    # Transición inicial de S al estado inicial del AFD
    W[S][afd["inicial"]] = "λ"

    # Transición de estados finales del AFD hacia F
    for f in afd["finales"]:
        if f in todos_los_nodos:
            W[f][F] = "λ"

    # Cargar transiciones del autómata
    for q in nodos_internos:
        if q in afd["transiciones"]:
            for sim, dest in afd["transiciones"][q].items():
                if dest in todos_los_nodos:
                    W[q][dest] = _union(W[q][dest], sim)

    pasos = []
    nodos_activos = set(todos_los_nodos)

    # 3. Eliminar nodos internos uno a uno (Lema de Arden / Eliminación)
    for k in nodos_internos:
        nodos_activos.remove(k)
        pasos.append(f"Eliminando estado {k}")

        for i in nodos_activos:
            if i == F: continue  # F no tiene salidas
            for j in nodos_activos:
                if j == S: continue  # S no tiene entradas

                r_ik = W[i][k]
                r_kk = W[k][k]
                r_kj = W[k][j]

                if r_ik != "Ø" and r_kj != "Ø":
                    bucle = _kleene(r_kk)
                    camino = _concat(_concat(r_ik, bucle), r_kj)
                    W[i][j] = _union(W[i][j], camino)
                    pasos.append(f"  R({i}->{j}) = {W[i][j]}")



    er_final = W[S][F]
    if er_final == "Ø":
        er_final = "Ø"

    return er_final, pasos