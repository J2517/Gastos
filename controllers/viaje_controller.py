from datetime import datetime
from models.viaje import Viaje
from models.gasto import Gasto
from utils.enums import TipoGasto, MedioPago
from services.exchange_service import ExchangeService
from services.reporte_service import ReporteService
from data.persistencia import guardar_viaje, cargar_viajes

class ViajeController:
    def __init__(self):
        self.viaje_actual: Viaje | None = None
        self.exchange_service = ExchangeService()
        self.reporte_service = ReporteService()

    def iniciar_aplicacion(self):
        """
        Inicia la aplicación desde consola.
        Permite crear o cargar un viaje y mantener al usuario en el menú principal mientras el viaje esté activo.
        """
        print("--- Bienvenido ---")
        print("1. Crear nuevo viaje")
        print("2. Cargar viaje existente")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            self.crear_viaje()
        elif opcion == "2":
            self.seleccionar_viaje_existente()
        else:
            print("❌ Opción inválida.")
            return

        while not self.viaje_actual.finalizado:
            self.menu()

    def crear_viaje(self):
        """
        Solicita al usuario los datos para crear un viaje nuevo.
        Reintenta ante entradas inválidas y evita duplicados por nombre.
        """
        viajes_existentes = cargar_viajes()
        nombres_existentes = [v.nombre.strip().lower() for v in viajes_existentes]

        while True:
            try:
                nombre = input("Ponle un nombre a tu viaje: ").strip()
                if nombre.lower() in nombres_existentes:
                    print("❌ Ya existe un viaje con ese nombre. Intente con uno diferente.\n")
                    continue

                nacional = input("¿El viaje es nacional? (s/n): ").strip().lower() == 's'
                fecha_inicio = self._leer_fecha("Fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = self._leer_fecha("Fecha de fin (YYYY-MM-DD): ")
                presupuesto = float(input("Presupuesto diario (en COP): "))
                moneda = "cop" if nacional else input("Moneda del país visitado (ej. usd, eur): ").strip().lower()

                self.viaje_actual = Viaje(nombre, nacional, fecha_inicio, fecha_fin, presupuesto, moneda)
                break
            except Exception as e:
                print(f"[ERROR] Entrada inválida: {e}. Intente nuevamente.\n")


    def seleccionar_viaje_existente(self):
        """
        Permite al usuario seleccionar un viaje existente por nombre si aún no ha finalizado.
        """
        viajes = cargar_viajes()
        viajes_activos = [v for v in viajes if not v.finalizado]

        if not viajes_activos:
            print("⚠️ No hay viajes activos disponibles.")
            self.crear_viaje()
            return

        print("\n📋 Viajes activos disponibles:")
        for v in viajes_activos:
            print(f"- {v.nombre} ({v.fecha_inicio} a {v.fecha_fin}, {v.moneda.upper()})")

        while True:
            nombre = input("🔎 Escriba el nombre exacto del viaje que desea cargar: ").strip()
            seleccionados = [v for v in viajes_activos if v.nombre.lower() == nombre.lower()]
            if seleccionados:
                self.viaje_actual = seleccionados[0]
                break
            else:
                print("❌ No se encontró un viaje con ese nombre. Intente de nuevo.")

    def menu(self):
        """
        Muestra las opciones principales durante un viaje activo:
        1. Registrar un gasto
        2. Ver reportes
        3. Finalizar viaje (y guardar)
        4. Salir sin finalizar (se guarda el progreso)
        """
        print("\n--- Menú ---")
        print("1. Registrar gasto")
        print("2. Ver reportes")
        print("3. Finalizar viaje")
        print("4. Salir sin finalizar")

        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            self.registrar_gasto()
        elif opcion == "2":
            self.mostrar_reportes()
        elif opcion == "3":
            self.viaje_actual.finalizar()
            guardar_viaje(self.viaje_actual)
            print("✅ Viaje finalizado y guardado.")
        elif opcion == "4":
            guardar_viaje(self.viaje_actual)
            print("📁 Progreso guardado. Puedes continuar este viaje más adelante.")
            exit()
        else:
            print("❌ Opción no válida.")

    def registrar_gasto(self):
        """
        Permite registrar un gasto en el viaje actual:
        - Valida que la fecha esté dentro del rango del viaje.
        - Convierte el valor a COP si es necesario.
        - Muestra la diferencia frente al presupuesto diario.
        """
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
        """
        Solicita una fecha al usuario en formato YYYY-MM-DD.
        Si la entrada es inválida, la vuelve a pedir hasta obtener un valor correcto.
        """
        while True:
            try:
                fecha_str = input(mensaje).strip()
                return datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                print("⚠️ Fecha inválida. Formato correcto: YYYY-MM-DD")

    def _seleccionar_enum(self, enum_cls, titulo: str):
        """
        Muestra un listado de opciones basado en un enumerado.
        Valida que la opción seleccionada por el usuario sea válida.
        """
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
        """
        Suma todos los gastos en COP realizados en una fecha específica del viaje.
        Se usa para calcular la diferencia con el presupuesto diario.
        """
        return sum(g.valor_cop for g in self.viaje_actual.gastos if g.fecha == fecha)

    def mostrar_reportes(self):
        """
        Muestra por consola dos reportes generados:
        - Reporte diario: total por día, separado por efectivo y tarjeta.
        - Reporte por tipo de gasto: agrupado por categorías y medios de pago.
        """
        print("\n📊 Reporte por día:")
        diario = self.reporte_service.reporte_por_dia(self.viaje_actual)
        for dia, valores in diario.items():
            print(f"{dia}: Efectivo={valores[MedioPago.EFECTIVO]:.2f}, Tarjeta={valores[MedioPago.TARJETA]:.2f}")

        print("\n📊 Reporte por tipo:")
        tipos = self.reporte_service.reporte_por_tipo(self.viaje_actual)
        for tipo, valores in tipos.items():
            print(f"{tipo.value}: Efectivo={valores[MedioPago.EFECTIVO]:.2f}, Tarjeta={valores[MedioPago.TARJETA]:.2f}")
      