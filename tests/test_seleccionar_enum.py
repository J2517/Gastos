
import unittest
from unittest.mock import patch
from controllers.viaje_controller import ViajeController
from utils.enums import TipoGasto

class TestSeleccionarEnum(unittest.TestCase):
    def setUp(self):
        self.controller = ViajeController()

    @patch("builtins.input", side_effect=["3"])
    def test_seleccion_valida(self, mock_input):
        resultado = self.controller._seleccionar_enum(TipoGasto, "Tipo de gasto")
        self.assertEqual(resultado, list(TipoGasto)[2])

    @patch("builtins.input", side_effect=["abc", "10", "1"])
    def test_seleccion_con_reintentos(self, mock_input):
        resultado = self.controller._seleccionar_enum(TipoGasto, "Tipo de gasto")
        self.assertEqual(resultado, list(TipoGasto)[0])
