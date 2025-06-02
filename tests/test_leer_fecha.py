
import unittest
from unittest.mock import patch
from controllers.viaje_controller import ViajeController
from datetime import date

class TestLeerFecha(unittest.TestCase):
    def setUp(self):
        self.controller = ViajeController()

    @patch("builtins.input", side_effect=["2024-06-01"])
    def test_leer_fecha_valida(self, mock_input):
        resultado = self.controller._leer_fecha("Ingrese la fecha: ")
        self.assertEqual(resultado, date(2024, 6, 1))

    @patch("builtins.input", side_effect=["fecha incorrecta", "otra mal", "2024-06-05"])
    def test_leer_fecha_reintento_hasta_valida(self, mock_input):
        resultado = self.controller._leer_fecha("Ingrese la fecha: ")
        self.assertEqual(resultado, date(2024, 6, 5))
