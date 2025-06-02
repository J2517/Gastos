import requests

class ExchangeService:
    BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"

    def convertir_a_cop(self, valor: float, moneda_origen: str) -> float:
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
