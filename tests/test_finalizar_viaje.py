
import unittest
from models.viaje import Viaje
from datetime import date

class TestFinalizarViaje(unittest.TestCase):
    def test_finaliza_viaje_correctamente(self):
        viaje = Viaje(True, date(2024, 6, 1), date(2024, 6, 10), 100000, "cop")
        self.assertFalse(viaje.finalizado)
        viaje.finalizar()
        self.assertTrue(viaje.finalizado)
