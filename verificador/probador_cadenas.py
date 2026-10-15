# verificador/probador_cadenas.py
import itertools
import re

def evaluar_afnd(afnd, cadena):
    actuales = set([afnd["inicial"]])
    for sim in cadena:
        siguientes = set()
        for q in actuales:
            if q in afnd["transiciones"] and sim in afnd["transiciones"][q]:
                dest = afnd["transiciones"][q][sim]
                # Si la transición es un string (AFD) en lugar de una lista (AFND)
                if isinstance(dest, str):
                    if dest != "Ø":
                        siguientes.add(dest)
                else:
                    siguientes.update(dest)
        actuales = siguientes
        if not actuales:
            break
    return bool(actuales.intersection(afnd["finales"]))

def evaluar_afd(afd, cadena):
    actual = afd["inicial"]
    for sim in cadena:
        if actual in afd["transiciones"] and sim in afd["transiciones"][actual]:
            actual = afd["transiciones"][actual][sim]
        else:
            return False
    return actual in afd["finales"]

def evaluar_regex(regex, cadena):
    if not regex:
        return cadena == ""
    # Reemplazamos notación algebraica '+' por '|' para el motor 're' de Python
    py_regex = regex.replace("+", "|").replace("λ", "")
    try:
        return bool(re.fullmatch(py_regex, cadena))
    except re.error:
        return False

def verificar_equivalencia(afnd, afd, regex, n=6):
    """
    Genera combinaciones y compara en paralelo los tres modelos.
    """
    for i in range(n + 1):
        for prod in itertools.product(afnd["alfabeto"], repeat=i):
            cad = "".join(prod)
            r_afnd = evaluar_afnd(afnd, cad)
            r_afd = evaluar_afd(afd, cad)
            r_reg = evaluar_regex(regex, cad)
            
            if not (r_afnd == r_afd == r_reg):
                return False, cad, (r_afnd, r_afd, r_reg)
    return True, None, None