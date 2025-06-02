from datetime import date
from utils.enums import TipoGasto, MedioPago

class Gasto:
    def __init__(self, fecha: date, valor: float, tipo: TipoGasto, medio: MedioPago, valor_cop: float):
        self.fecha = fecha
        self.valor = valor
        self.valor_cop = valor_cop  # Valor convertido a COP
        self.tipo = tipo
        self.medio = medio
