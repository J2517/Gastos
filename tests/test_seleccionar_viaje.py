import unittest
from unittest.mock import patch, MagicMock
from controllers.viaje_controller import ViajeController
from models.viaje import Viaje
from datetime import date

class TestSeleccionarViajeExistente(unittest.TestCase):

    """Conjunto de pruebas para seleccionar viajes existentes en el sistema."""

    def setUp(self):
        """Inicializa el controlador antes de cada prueba."""
        self.controller = ViajeController()

    @patch("controllers.viaje_controller.cargar_viajes")
    @patch("builtins.input", side_effect=["MiViaje"])

    def test_seleccion_viaje_existente_valido(self, mock_input, mock_cargar):
        """Debe asignar el viaje correcto al seleccionar por nombre exacto."""
        mock_cargar.return_value = [
            Viaje("MiViaje", True, date(2024, 6, 1), date(2024, 6, 10), 50000, "cop")
        ]
        self.controller.seleccionar_viaje_existente()
        self.assertEqual(self.controller.viaje_actual.nombre, "MiViaje")

    @patch("controllers.viaje_controller.cargar_viajes")
    @patch("builtins.input", side_effect=["OtroNombre", "ViajeX"])

    def test_nombre_inexistente(self, mock_input, mock_cargar):

        """Si el nombre no existe debe volver a pedir entrada."""
        mock_cargar.return_value = [
            Viaje("ViajeX", True, date(2024, 6, 1), date(2024, 6, 10), 50000, "cop")
        ]
        with patch("builtins.print") as mock_print:
            self.controller.seleccionar_viaje_existente()
            mock_print.assert_any_call("❌ No se encontró un viaje con ese nombre. Intente de nuevo.")
            self.assertEqual(self.controller.viaje_actual.nombre, "ViajeX")

    @patch("controllers.viaje_controller.cargar_viajes")
    @patch("builtins.input", side_effect=["miviaje"])

    def test_nombre_insensible_a_mayusculas(self, mock_input, mock_cargar):
        """Debe aceptar nombres insensibles a mayúsculas y minúsculas."""
        mock_cargar.return_value = [
            Viaje("MiViaje", True, date(2024, 6, 1), date(2024, 6, 10), 50000, "cop")
        ]
        self.controller.seleccionar_viaje_existente()
        self.assertEqual(self.controller.viaje_actual.nombre, "MiViaje")

    @patch("controllers.viaje_controller.cargar_viajes")

    def test_sin_viajes_activos(self, mock_cargar):
        """Si no hay viajes activos, se debe crear uno nuevo."""
        mock_cargar.return_value = [
            Viaje("Finalizado1", True, date(2024, 6, 1), date(2024, 6, 10), 50000, "cop")
        ]
        mock_cargar.return_value[0].finalizado = True
        with patch.object(self.controller, "crear_viaje") as mock_crear:
            with patch("builtins.print") as mock_print:
                self.controller.seleccionar_viaje_existente()
                mock_print.assert_any_call("⚠️ No hay viajes activos disponibles.")
                mock_crear.assert_called_once()

    @patch("controllers.viaje_controller.cargar_viajes", return_value=[])
    
    def test_lista_vacia_de_viajes(self, mock_cargar):
        """Debe crear un nuevo viaje si no hay ninguno registrado en el archivo."""
        with patch.object(self.controller, "crear_viaje") as mock_crear:
            with patch("builtins.print") as mock_print:
                self.controller.seleccionar_viaje_existente()
                mock_print.assert_any_call("⚠️ No hay viajes activos disponibles.")
                mock_crear.assert_called_once()