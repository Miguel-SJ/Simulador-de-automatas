import unittest
import sys
import os

# Esto permite importar módulos desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conversion.subconjuntos import convertir_afnd_a_afd
from expresiones.algebra_arden import obtener_expresion_regular
from verificador.probador_cadenas import verificar_equivalencia

class TestSimulador(unittest.TestCase):

    def setUp(self):
        self.caso1_afnd = {
            "estados": ["q0", "q1", "q2"],
            "alfabeto": ["a", "b"],
            "inicial": "q0",
            "finales": ["q2"],
            "transiciones": {
                "q0": {"a": ["q0", "q1"]},
                "q1": {"b": ["q2"]},
                "q2": {}
            }
        }
        
        self.caso2_afd = {
            "estados": ["q0", "q1", "q2"],
            "alfabeto": ["x", "y"],
            "inicial": "q0",
            "finales": ["q1"],
            "transiciones": {
                "q0": {"x": "q1", "y": "Ø"},
                "q1": {"x": "q2", "y": "Ø"},
                "q2": {"y": "q2", "x": "q1"}
            }
        }

    def test_caso1_afnd_a_afd(self):
        afd, tabla = convertir_afnd_a_afd(self.caso1_afnd)
        self.assertIn("Ø", afd["estados"])
        self.assertIn("q2", afd["finales"])
        self.assertEqual(afd["transiciones"]["q0"]["a"], "q0,q1")
        self.assertEqual(afd["transiciones"]["q0"]["b"], "Ø")
        
        equiv, cad_fallo, _ = verificar_equivalencia(self.caso1_afnd, afd, "a*ab", n=6)
        self.assertTrue(equiv, f"Falló equivalencia en AFND->AFD. Cadena: {cad_fallo}")

    def test_caso2_afd_a_regex(self):
        er, pasos = obtener_expresion_regular(self.caso2_afd)
        self.assertTrue(len(er) > 0)
        
        equiv, cad_fallo, _ = verificar_equivalencia(self.caso2_afd, self.caso2_afd, er, n=6)
        self.assertTrue(equiv, f"La ER generada {er} no equivale al AFD. Cadena fallo: {cad_fallo}")

    def test_caso_limite_estado_pozo(self):
        afnd_pozo = {
            "estados": ["q0"], "alfabeto": ["a", "b"], "inicial": "q0", "finales": ["q0"],
            "transiciones": {"q0": {"a": ["q0"]}}
        }
        afd, _ = convertir_afnd_a_afd(afnd_pozo)
        self.assertEqual(afd["transiciones"]["Ø"]["a"], "Ø")
        self.assertEqual(afd["transiciones"]["Ø"]["b"], "Ø")
        
        er, _ = obtener_expresion_regular(afd)
        equiv, _, _ = verificar_equivalencia(afnd_pozo, afd, er, n=6)
        self.assertTrue(equiv)

    def test_caso_limite_alfabeto_monosimbolo(self):
        afnd_mono = {
            "estados": ["q0", "q1"], "alfabeto": ["x"], "inicial": "q0", "finales": ["q1"],
            "transiciones": {"q0": {"x": ["q1"]}, "q1": {"x": ["q1"]}}
        }
        afd, _ = convertir_afnd_a_afd(afnd_mono)
        er, _ = obtener_expresion_regular(afd)
        
        equiv, cad, _ = verificar_equivalencia(afnd_mono, afd, er, n=8)
        self.assertTrue(equiv)

if __name__ == '__main__':
    unittest.main(verbosity=2)