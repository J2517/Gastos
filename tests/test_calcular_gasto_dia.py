
import unittest
from datetime import date
from models.gasto import Gasto
from models.viaje import Viaje
from utils.enums import TipoGasto, MedioPago
from controllers.viaje_controller import ViajeController

class TestCalcularGastoDia(unittest.TestCase):
    def setUp(self):
        self.controller = ViajeController()
        self.controller.viaje_actual = Viaje(True, date(2024, 6, 1), date(2024, 6, 10), 100000, "cop")
        self.controller.viaje_actual.gastos = [
            Gasto(date(2024, 6, 2), 10000, TipoGasto.ALIMENTACION, MedioPago.EFECTIVO, 10000),
            Gasto(date(2024, 6, 2), 20000, TipoGasto.ALIMENTACION, MedioPago.TARJETA, 20000),
            Gasto(date(2024, 6, 3), 5000, TipoGasto.TRANSPORTE, MedioPago.EFECTIVO, 5000)
        ]

    def test_calcular_gasto_en_dia(self):
        total = self.controller.calcular_gasto_dia(date(2024, 6, 2))
        self.assertEqual(total, 30000)

    def test_calcular_gasto_dia_sin_gastos(self):
        total = self.controller.calcular_gasto_dia(date(2024, 6, 5))
        self.assertEqual(total, 0)
