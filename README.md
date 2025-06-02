
# 📊 Registro de Gastos de Viaje

Esta aplicación permite registrar y consultar los gastos diarios durante un viaje nacional o internacional. Se realiza la conversión automática de moneda a pesos colombianos (COP) y se generan reportes por día y por tipo de gasto.


## 🚀 Cómo ejecutar la aplicación

```bash
python main.py
```

## 🧪 Cómo ejecutar las pruebas

Desde la raíz del proyecto, ejecuta:

```bash
python -m unittest discover tests
```

Esto buscará automáticamente todos los archivos que comiencen con `test_*.py` dentro de la carpeta `tests/` y ejecutará las pruebas unitarias e integradas.


## 🛠️ Dependencias

- Python 3.10+
- `requests` (para la conversión de moneda)


## 📌 Notas técnicas

- El método `_leer_fecha` y `_seleccionar_enum` están prefijados con guión bajo por convención de Python para indicar que son de uso interno.
- Se utiliza el archivo `data/viajes.json` para guardar los viajes.
- Se emplea `unittest.mock` para simular entradas, conversiones de moneda y persistencia, permitiendo así pruebas controladas sin efectos colaterales.

---

## 👨‍🔬 Autores

Desarrollado por [Jackeline Rivera] y [Manuel Carmona] – Ingeniería de Software I
