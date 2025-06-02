import requests

class ExchangeService:
    """
    Servicio que consulta una API externa de tasas de cambio (Currency API de Fawaz Ahmed)
    para convertir valores monetarios desde una divisa extranjera a pesos colombianos (COP).
    """
    BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"

    def convertir_a_cop(self, valor: float, moneda_origen: str) -> float:
        """
        Convierte un valor monetario desde la moneda de origen especificada a pesos colombianos (COP),
        utilizando la tasa de cambio actual obtenida desde la API Currency API (https://github.com/fawazahmed0/currency-api).

        Parámetros:
        - valor (float): el valor numérico en la moneda original.
        - moneda_origen (str): el código de moneda (ej. "usd", "eur", "brl").

        Retorna:
        - float: el valor convertido a COP. Si no se puede obtener la tasa, devuelve el valor original como fallback.

        Esta función asume que si la moneda ya es "cop", no se requiere conversión.
        """
        if moneda_origen.lower() == "cop":
            return valor
        try:
            url = f"{self.BASE_URL}/{moneda_origen.lower()}.json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            tasa = data[moneda_origen.lower()]['cop']
            return valor * tasa
        except Exception as e:
            print(f"[ERROR] No se pudo obtener tasa de cambio: {e}")
            return valor  # como fallback retornamos el mismo valor
