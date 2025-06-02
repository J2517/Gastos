from datetime import date
from utils.enums import TipoGasto, MedioPago

class Gasto:
    """
    Representa un gasto realizado en un día específico durante un viaje.
    Incluye el valor original, el valor en COP, el tipo y el medio de pago.
    """
    def __init__(self, fecha: date, valor: float, tipo: TipoGasto, medio: MedioPago, valor_cop: float):
        self.fecha = fecha
        self.valor = valor
        self.valor_cop = valor_cop  # Valor convertido a COP
        self.tipo = tipo
        self.medio = medio
