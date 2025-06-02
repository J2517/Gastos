
import unittest
from unittest.mock import patch, MagicMock
from controllers.viaje_controller import ViajeController
from datetime import date
from models.viaje import Viaje

class TestMostrarReportes(unittest.TestCase):
    def setUp(self):
        self.controller = ViajeController()
        self.controller.viaje_actual = Viaje(True, date(2024, 6, 1), date(2024, 6, 10), 100000, "cop")

    @patch("controllers.viaje_controller.ReporteService.reporte_por_dia")
    @patch("controllers.viaje_controller.ReporteService.reporte_por_tipo")
    def test_mostrar_reportes_salida_correcta(self, mock_tipo, mock_dia):
        mock_dia.return_value = {}
        mock_tipo.return_value = {}
        self.controller.mostrar_reportes()
        mock_dia.assert_called_once()
        mock_tipo.assert_called_once()
