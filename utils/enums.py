from enum import Enum

class TipoGasto(Enum):
    TRANSPORTE = "Transporte"
    ALOJAMIENTO = "Alojamiento"
    ALIMENTACION = "Alimentación"
    ENTRETENIMIENTO = "Entretenimiento"
    COMPRAS = "Compras"

class MedioPago(Enum):
    EFECTIVO = "Efectivo"
    TARJETA = "Tarjeta"
