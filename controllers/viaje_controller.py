from datetime import datetime
from models.viaje import Viaje
from models.gasto import Gasto
from utils.enums import TipoGasto, MedioPago
from services.exchange_service import ExchangeService
from services.reporte_service import ReporteService
from data.persistencia import guardar_viaje
   
class ViajeController:
    def __init__(self):
        self.viaje_actual: Viaje | None = None
        self.exchange_service = ExchangeService()
        self.reporte_service = ReporteService()

    def iniciar_aplicacion(self):
        self.crear_viaje()
        while not self.viaje_actual.finalizado:
            self.menu()

    def crear_viaje(self):
        while True:
            try:
                nacional = input("¿El viaje es nacional? (s/n): ").strip().lower() == 's'
                fecha_inicio = self._leer_fecha("Fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = self._leer_fecha("Fecha de fin (YYYY-MM-DD): ")
                presupuesto = float(input("Presupuesto diario (en COP): "))
                moneda = "cop" if nacional else input("Moneda del país visitado (ej. usd, eur): ").strip().lower()
                self.viaje_actual = Viaje(nacional, fecha_inicio, fecha_fin, presupuesto, moneda)
                break
            except Exception as e:
                print(f"[ERROR] Entrada inválida: {e}. Intente nuevamente.\n")

    def menu(self):
        print("\n--- Menú ---")
        print("1. Registrar gasto")
        print("2. Ver reportes")
        print("3. Finalizar viaje")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            self.registrar_gasto()
        elif opcion == "2":
            self.mostrar_reportes()
        elif opcion == "3":
            self.viaje_actual.finalizar()
            guardar_viaje(self.viaje_actual)
            print("✅ Viaje finalizado y guardado.")

    def registrar_gasto(self):
        try:
            fecha = self._leer_fecha("Fecha del gasto (YYYY-MM-DD): ")
            if not (self.viaje_actual.fecha_inicio <= fecha <= self.viaje_actual.fecha_fin):
                print("⚠️ Fecha fuera del rango del viaje. Intente con una fecha válida.")
                return

            valor = float(input("Valor del gasto: "))
            medio = self._seleccionar_enum(MedioPago, "Medio de pago")
            tipo = self._seleccionar_enum(TipoGasto, "Tipo de gasto")

            valor_cop = self.exchange_service.convertir_a_cop(valor, self.viaje_actual.moneda)
            gasto = Gasto(fecha, valor, tipo, medio, valor_cop)
            self.viaje_actual.agregar_gasto(gasto)

            diferencia = self.viaje_actual.presupuesto_diario - self.calcular_gasto_dia(fecha)
            print(f"Diferencia respecto al presupuesto diario: {diferencia:.2f} COP")
        except Exception as e:
            print(f"[ERROR] No se pudo registrar el gasto: {e}. Intente nuevamente.\n")

    def _leer_fecha(self, mensaje: str) -> datetime.date:
        while True:
            try:
                fecha_str = input(mensaje).strip()
                return datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                print("⚠️ Fecha inválida. Formato correcto: YYYY-MM-DD")

    def _seleccionar_enum(self, enum_cls, titulo: str):
        print(f"\nSeleccione {titulo}:")
        for idx, item in enumerate(enum_cls, start=1):
            print(f"{idx}. {item.value}")
        while True:
            try:
                opcion = int(input("Opción: "))
                return list(enum_cls)[opcion - 1]
            except (ValueError, IndexError):
                print("❌ Opción inválida. Intente nuevamente.")

    def calcular_gasto_dia(self, fecha):
        return sum(g.valor_cop for g in self.viaje_actual.gastos if g.fecha == fecha)

    def mostrar_reportes(self):
        print("\n📊 Reporte por día:")
        diario = self.reporte_service.reporte_por_dia(self.viaje_actual)
        for dia, valores in diario.items():
            print(f"{dia}: Efectivo={valores[MedioPago.EFECTIVO]:.2f}, Tarjeta={valores[MedioPago.TARJETA]:.2f}")

        print("\n📊 Reporte por tipo:")
        tipos = self.reporte_service.reporte_por_tipo(self.viaje_actual)
        for tipo, valores in tipos.items():
            print(f"{tipo.value}: Efectivo={valores[MedioPago.EFECTIVO]:.2f}, Tarjeta={valores[MedioPago.TARJETA]:.2f}")
            