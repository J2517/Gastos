
import unittest
from unittest.mock import patch, mock_open
from data.persistencia import guardar_viaje, cargar_viajes, viaje_to_dict
from models.viaje import Viaje
from datetime import date
import json

class TestPersistencia(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("data.persistencia.cargar_viajes", return_value=[])
    def test_guardar_viaje(self, mock_cargar, mock_file):
        viaje = Viaje(True, date(2024, 6, 1), date(2024, 6, 10), 50000, "cop")
        guardar_viaje(viaje)
        mock_file.assert_called_once_with("data/viajes.json", "w", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"destino_nacional": true, "fecha_inicio": "2024-06-01", "fecha_fin": "2024-06-10", "presupuesto_diario": 50000, "moneda": "cop", "finalizado": false, "gastos": []}]')
    def test_cargar_viajes_correctamente(self, mock_file):
        viajes = cargar_viajes()
        self.assertEqual(len(viajes), 1)
        self.assertEqual(viajes[0].moneda, "cop")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_cargar_viajes_archivo_no_existente(self, mock_file):
        viajes = cargar_viajes()
        self.assertEqual(viajes, [])
