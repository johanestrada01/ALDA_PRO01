import unittest
from unittest.mock import patch
import importlib
import os
import sys
import tempfile

class TestScriptVIH(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        script_dir = os.path.abspath(os.path.dirname(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        with patch('builtins.input', side_effect=['', '']):
            cls.module = importlib.import_module('data')  

    def test_obtener_promedio_historico(self):
        promedio = self.module.obtener_promedio_historico("Contagios")
        self.assertIsInstance(promedio, float)
        self.assertGreater(promedio, 0)

    def test_obtener_tendencia_historica(self):
        tendencia = self.module.obtener_tendencia_historica("Contagios")
        self.assertIsInstance(tendencia, float)

    def test_generar_contagios_pasado(self):
        for año in [1981, 1985, 1995]:
            valor = self.module.generar_contagios(año)
            self.assertIsInstance(valor, int)
            self.assertGreaterEqual(valor, 50)

    def test_generar_contagios_futuro(self):
        self.module.datos_gen["Contagios"][2024] = self.module.datos_reales[2024][0]
        for año in [2025, 2026, 2030]:
            valor = self.module.generar_contagios(año)
            self.assertIsInstance(valor, int)
            self.assertGreater(valor, 0)

    def test_ajustar_complementarias_binaria(self):
        self.module.datos_gen["%Hombres"][2025] = 80.0
        self.module.datos_gen["%Mujeres"].pop(2025, None)
        self.module.ajustar_complementarias("%Hombres", ["%Mujeres"], 2025)
        self.assertAlmostEqual(self.module.datos_gen["%Mujeres"][2025], 20.0, places=2)

    def test_ajustar_complementarias_multiple(self):
        self.module.datos_gen["%Hetero"][2025] = 50.0
        self.module.datos_gen["%Homo"].pop(2025, None)
        self.module.datos_gen["%Bi"].pop(2025, None)
        self.module.ajustar_complementarias("%Hetero", ["%Homo", "%Bi"], 2025)
        suma = (self.module.datos_gen["%Hetero"][2025] +
                self.module.datos_gen["%Homo"][2025] +
                self.module.datos_gen["%Bi"][2025])
        self.assertAlmostEqual(suma, 100.0, delta=0.1)
    
    def test_datos_gen_inicializado_correctamente(self):
        self.assertIn("Contagios", self.module.datos_gen)
        self.assertIsInstance(self.module.datos_gen["Contagios"], dict)

    def test_generacion_intervalo_valido(self):
        for año in range(1981, 2024):
            if año not in self.module.datos_gen["Contagios"]:
                valor = self.module.generar_contagios(año)
                self.assertIsInstance(valor, int)
                self.assertGreaterEqual(valor, 0)


if __name__ == '__main__':
    unittest.main()
