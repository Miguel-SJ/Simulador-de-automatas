def convertir_afnd_a_afd(afnd):
    """
    Convierte un AFND a AFD usando el método de subconjuntos.
    Retorna el AFD resultante y la tabla de transiciones para el paso a paso.
    """
    alfabeto = afnd["alfabeto"]
    inicial = afnd["inicial"]
    finales_afnd = set(afnd["finales"])
    trans_afnd = afnd["transiciones"]

    q0_set = frozenset([inicial])
    q0_str = ",".join(sorted(q0_set))

    afd = {
        "estados": [],
        "alfabeto": alfabeto,
        "inicial": q0_str,
        "finales": [],
        "transiciones": {}
    }

    pendientes = [q0_set]
    procesados = set()
    tabla_pasos = []

    while pendientes:
        actual_set = pendientes.pop(0)
        actual_str = ",".join(sorted(actual_set)) if actual_set else "Ø"

        if actual_str in procesados:
            continue

        procesados.add(actual_str)
        afd["estados"].append(actual_str)
        afd["transiciones"][actual_str] = {}

        if actual_set.intersection(finales_afnd):
            afd["finales"].append(actual_str)

        fila_tabla = {"estado": actual_str, "transiciones": {}}

        for sim in alfabeto:
            destinos = set()
            for q in actual_set:
                if q in trans_afnd and sim in trans_afnd[q]:
                    destinos.update(trans_afnd[q][sim])
            
            destino_str = ",".join(sorted(destinos)) if destinos else "Ø"
            afd["transiciones"][actual_str][sim] = destino_str
            fila_tabla["transiciones"][sim] = destino_str

            if destino_str not in procesados and frozenset(destinos) not in pendientes:
                pendientes.append(frozenset(destinos))
        
        tabla_pasos.append(fila_tabla)

    return afd, tabla_pasos