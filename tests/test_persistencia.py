import unittest
from unittest.mock import MagicMock, patch
from controllers.viaje_controller import ViajeController
from models.viaje import Viaje
from datetime import date

class TestMostrarReportes(unittest.TestCase):

    def setUp(self):
        self.controller = ViajeController()
        self.controller.viaje_actual = Viaje(True, date(2024, 1, 1), date(2024, 1, 10), 100000, "cop")

    @patch("controllers.viaje_controller.ReporteService.reporte_por_dia")
    @patch("controllers.viaje_controller.ReporteService.reporte_por_tipo")
    def test_mostrar_reportes_llama_servicio(self, mock_tipo, mock_dia):
        # Simula los valores devueltos por los reportes
        mock_dia.return_value = {}
        mock_tipo.return_value = {}

        self.controller.mostrar_reportes()

        mock_dia.assert_called_once_with(self.controller.viaje_actual)
        mock_tipo.assert_called_once_with(self.controller.viaje_actual)
