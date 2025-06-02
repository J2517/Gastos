
import unittest
from unittest.mock import patch
from controllers.viaje_controller import ViajeController
from datetime import date
from models.viaje import Viaje

class TestCrearViaje(unittest.TestCase):
    def setUp(self):
        self.controller = ViajeController()

    @patch("builtins.input")
    @patch("controllers.viaje_controller.Viaje")
    def test_crear_viaje_exitosamente(self, mock_viaje, mock_input):
        mock_input.side_effect = [
            "s",                   # Es nacional
            "2024-06-01",          # Fecha inicio
            "2024-06-10",          # Fecha fin
            "50000"                # Presupuesto diario
        ]
        self.controller.crear_viaje()
        self.assertIsNotNone(self.controller.viaje_actual)
        mock_viaje.assert_called_once_with(True, date(2024, 6, 1), date(2024, 6, 10), 50000.0, "cop")

    @patch("builtins.input")
    def test_crear_viaje_con_error_entrada(self, mock_input):
        mock_input.side_effect = [
            "s",                   # Es nacional
            "fecha inválida",      # Fecha inicio errónea
            "2024-06-10",          # (no se usará)
            "50000"                # (no se usará)
        ] * 2 + [  # repetir errores
            "s", "2024-06-01", "2024-06-10", "50000"  # intento válido
        ]

        with patch("controllers.viaje_controller.Viaje") as mock_viaje:
            self.controller.crear_viaje()
            self.assertIsNotNone(self.controller.viaje_actual)
            self.assertEqual(mock_viaje.call_count, 1)
