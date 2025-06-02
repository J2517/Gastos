import unittest
from unittest.mock import patch, MagicMock
from controllers.viaje_controller import ViajeController
from datetime import date
from models.viaje import Viaje
from utils.enums import TipoGasto, MedioPago
from models.gasto import Gasto

class TestRegistrarGastoConMock(unittest.TestCase):

    def setUp(self):
        self.controller = ViajeController()
        self.controller.viaje_actual = Viaje(False, date(2024, 6, 1), date(2024, 6, 10), 100000, "usd")

    @patch("controllers.viaje_controller.ExchangeService.convertir_a_cop")
    @patch("builtins.input")
    @patch("controllers.viaje_controller.Viaje.agregar_gasto")
    def test_registrar_gasto_internacional_convierte_y_agrega(self, mock_agregar, mock_input, mock_convertir):
        # Simular entradas de usuario
        mock_input.side_effect = [
            "2024-06-02",  # Fecha del gasto
            "50",          # Valor del gasto en moneda original
            "1",           # Medio de pago -> EFECTIVO
            "2"            # Tipo de gasto -> ALOJAMIENTO
        ]

        # Simular tasa de cambio
        mock_convertir.return_value = 200000  # Valor convertido a COP

        # Ejecutar el método
        self.controller.registrar_gasto()

        # Verifica que se haya intentado convertir
        mock_convertir.assert_called_once_with(50.0, "usd")

        # Verifica que se haya agregado un gasto
        self.assertTrue(mock_agregar.called)
