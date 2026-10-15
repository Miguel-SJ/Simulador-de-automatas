# modelos/automata.py

def validar_automata(afnd):
    """
    Valida la integridad estructural y lógica de un autómata (AFND o AFD).
    Lanza ValueError si encuentra inconsistencias.
    """
    if not afnd.get("estados"):
        raise ValueError("El autómata debe tener al menos un estado definido.")
    if not afnd.get("alfabeto"):
        raise ValueError("El autómata debe tener un alfabeto definido.")
    
    inicial = afnd.get("inicial")
    if inicial not in afnd["estados"]:
        raise ValueError(f"El estado inicial '{inicial}' no pertenece al conjunto de estados.")
    
    for f in afnd.get("finales", []):
        if f not in afnd["estados"]:
            raise ValueError(f"El estado final '{f}' no pertenece al conjunto de estados.")
    
    for origen, trans in afnd.get("transiciones", {}).items():
        if origen not in afnd["estados"]:
            raise ValueError(f"Transición desde estado desconocido: '{origen}'")
        for sim, destinos in trans.items():
            if sim not in afnd["alfabeto"]:
                raise ValueError(f"El símbolo '{sim}' en la transición de '{origen}' no pertenece al alfabeto.")
            
            # Soporta tanto AFND (listas de destinos) como AFD (strings de destino)
            if isinstance(destinos, str):
                destinos = [destinos]
            for d in destinos:
                # 'Ø' es el estado pozo del motor, permitimos su trazabilidad visual
                if d not in afnd["estados"] and d != "Ø":
                    raise ValueError(f"Transición hacia estado desconocido: '{d}'")

    return True