import unittest
from unittest.mock import patch, MagicMock
from controllers.viaje_controller import ViajeController
from datetime import date
from models.viaje import Viaje

class TestRegistrarGasto(unittest.TestCase):
    """Conjunto de pruebas para el método registrar_gasto del controlador de viaje."""

    def setUp(self):
        """Crea un viaje de prueba antes de cada test."""
        self.controller = ViajeController()
        self.controller.viaje_actual = Viaje("Viaje1", True, date(2024, 6, 1), date(2024, 6, 10), 50000, "cop")

    @patch("builtins.input", side_effect=["2024-06-02", "30000", "1", "1"])
    @patch("controllers.viaje_controller.ExchangeService.convertir_a_cop", return_value=30000)
    def test_registrar_gasto_valido(self, mock_convertir, mock_input):
        """Debe agregar un gasto correctamente y calcular el presupuesto restante."""
        self.controller.registrar_gasto()
        self.assertEqual(len(self.controller.viaje_actual.gastos), 1)
        self.assertEqual(self.controller.viaje_actual.gastos[0].valor_cop, 30000)

    @patch("builtins.input", side_effect=["2024-07-01", "20000", "1", "1"])
    def test_gasto_fuera_de_rango(self, mock_input):
        """No debe agregar gasto si la fecha está fuera del rango del viaje."""
        with patch("builtins.print") as mock_print:
            self.controller.registrar_gasto()
            mock_print.assert_any_call("⚠️ Fecha fuera del rango del viaje. Intente con una fecha válida.")
            self.assertEqual(len(self.controller.viaje_actual.gastos), 0)

    @patch("builtins.input", side_effect=["2024-06-02", "abc", "1", "1"])
    def test_valor_no_numerico(self, mock_input):
        """Manejo de valor de gasto no numérico: debe imprimir error y no agregar gasto."""
        with patch("builtins.print") as mock_print:
            self.controller.registrar_gasto()
            self.assertEqual(len(self.controller.viaje_actual.gastos), 0)
            self.assertTrue(mock_print.called)

    @patch("builtins.input", side_effect=["2024-06-02", "10000", "99", "1", "1"])
    def test_medio_pago_invalido(self, mock_input):
        """Medio de pago inválido: debe imprimir mensaje y pedir nuevo input."""
        with patch("builtins.print") as mock_print:
            self.controller.registrar_gasto()
            mock_print.assert_any_call("❌ Opción inválida. Intente nuevamente.")

    @patch("builtins.input", side_effect=["2024-06-02", "10000", "1", "99", "1"])
    def test_tipo_gasto_invalido(self, mock_input):
        """Tipo de gasto inválido: debe imprimir mensaje y pedir nuevo input."""
        with patch("builtins.print") as mock_print:
            self.controller.registrar_gasto()
            mock_print.assert_any_call("❌ Opción inválida. Intente nuevamente.")

    def test_gasto_en_viaje_finalizado(self):
        """No debe agregar gasto si el viaje está marcado como finalizado."""
        self.controller.viaje_actual.finalizado = True
        with patch("builtins.input", side_effect=["2024-06-02", "30000", "1", "1"]):
            with patch("builtins.print") as mock_print:
                self.controller.registrar_gasto()
                self.assertEqual(len(self.controller.viaje_actual.gastos), 0)
                self.assertTrue(mock_print.called)

    @patch("builtins.input", side_effect=["02-06-2024", "2024-06-02", "30000", "1", "1"])
    def test_fecha_formato_invalido(self, mock_input):
        """Debe pedir la fecha nuevamente si el formato es inválido."""
        with patch("builtins.print") as mock_print:
            self.controller.registrar_gasto()
            mock_print.assert_any_call("⚠️ Fecha inválida. Formato correcto: YYYY-MM-DD")