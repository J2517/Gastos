
import unittest
from unittest.mock import patch, MagicMock
from controllers.viaje_controller import ViajeController
from datetime import date
from models.viaje import Viaje
from utils.enums import TipoGasto, MedioPago
from models.gasto import Gasto

class TestRegistrarGasto(unittest.TestCase):
    def setUp(self):
        self.controller = ViajeController()
        self.controller.viaje_actual = Viaje(False, date(2024, 6, 1), date(2024, 6, 10), 100000, "usd")

    @patch("builtins.input")
    @patch("controllers.viaje_controller.ExchangeService.convertir_a_cop")
    @patch("controllers.viaje_controller.Viaje.agregar_gasto")
    def test_registrar_gasto_exitosamente(self, mock_agregar, mock_convertir, mock_input):
        mock_input.side_effect = [
            "2024-06-02",  # Fecha del gasto
            "50",          # Valor
            "1",           # Medio de pago (efectivo)
            "2"            # Tipo de gasto (alojamiento)
        ]
        mock_convertir.return_value = 200000

        self.controller.registrar_gasto()

        mock_convertir.assert_called_once_with(50.0, "usd")
        self.assertTrue(mock_agregar.called)

    @patch("builtins.input")
    def test_fecha_fuera_de_rango_no_agrega_gasto(self, mock_input):
        mock_input.side_effect = [
            "2024-07-01",  # Fecha fuera de rango
            "100",         # Valor
            "1",           # Medio de pago
            "1"            # Tipo de gasto
        ]
        with patch.object(self.controller.viaje_actual, 'agregar_gasto') as mock_agregar:
            self.controller.registrar_gasto()
            mock_agregar.assert_not_called()

    @patch("builtins.input", side_effect=["2024-06-03", "valor no numérico", "1", "1"])
    def test_valor_invalido_lanza_error(self, mock_input):
        with patch("controllers.viaje_controller.ExchangeService.convertir_a_cop", return_value=0):
            self.controller.registrar_gasto()  # Debe imprimir error pero no lanzar excepción
