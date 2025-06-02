
import unittest
from unittest.mock import patch
from controllers.viaje_controller import ViajeController
from datetime import date

class TestMainFlow(unittest.TestCase):
    @patch("builtins.input", side_effect=[
        "s", "2024-06-01", "2024-06-10", "50000",  # crear viaje
        "1", "2024-06-02", "100", "1", "1",        # registrar gasto
        "2",                                       # mostrar reportes
        "3"                                        # finalizar viaje
    ])
    @patch("controllers.viaje_controller.guardar_viaje")
    def test_flujo_completo(self, mock_guardar, mock_input):
        controller = ViajeController()
        controller.iniciar_aplicacion()
        self.assertTrue(controller.viaje_actual.finalizado)
        mock_guardar.assert_called_once()
