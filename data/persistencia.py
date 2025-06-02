import json
from datetime import datetime, date
from models.viaje import Viaje
from models.gasto import Gasto
from utils.enums import TipoGasto, MedioPago

ARCHIVO_DATOS = "data/viajes.json"

def viaje_to_dict(viaje: Viaje) -> dict:
    return {
        "destino_nacional": viaje.destino_nacional,
        "fecha_inicio": viaje.fecha_inicio.isoformat(),
        "fecha_fin": viaje.fecha_fin.isoformat(),
        "presupuesto_diario": viaje.presupuesto_diario,
        "moneda": viaje.moneda,
        "finalizado": viaje.finalizado,
        "gastos": [
            {
                "fecha": gasto.fecha.isoformat(),
                "valor": gasto.valor,
                "valor_cop": gasto.valor_cop,
                "tipo": gasto.tipo.name,
                "medio": gasto.medio.name
            }
            for gasto in viaje.gastos
        ]
    }

def dict_to_viaje(data: dict) -> Viaje:
    viaje = Viaje(
        destino_nacional=data["destino_nacional"],
        fecha_inicio=date.fromisoformat(data["fecha_inicio"]),
        fecha_fin=date.fromisoformat(data["fecha_fin"]),
        presupuesto_diario=data["presupuesto_diario"],
        moneda=data["moneda"]
    )

    # Agregamos los gastos directamente (evitamos el método que valida)
    viaje.gastos = [
        Gasto(
            fecha=date.fromisoformat(g["fecha"]),
            valor=g["valor"],
            valor_cop=g["valor_cop"],
            tipo=TipoGasto[g["tipo"]],
            medio=MedioPago[g["medio"]]
        )
        for g in data["gastos"]
    ]

    # Solo después marcamos si está finalizado
    viaje.finalizado = data["finalizado"]
    return viaje

def guardar_viaje(viaje: Viaje):
    viajes = cargar_viajes()
    actualizado = False

    # Buscar si ya existe un viaje con mismas fechas y moneda
    for i, v in enumerate(viajes):
        if (
            v.fecha_inicio == viaje.fecha_inicio and
            v.fecha_fin == viaje.fecha_fin and
            v.moneda == viaje.moneda
        ):
            viajes[i] = viaje
            actualizado = True
            break

    # Si no está, agregarlo
    if not actualizado:
        viajes.append(viaje)

    # Convertir todos a dicts para guardar
    viajes_dict = [viaje_to_dict(v) for v in viajes]

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(viajes_dict, f, indent=4)


def cargar_viajes() -> list:
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [dict_to_viaje(d) for d in datos]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
