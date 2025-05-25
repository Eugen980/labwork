from api_client import APIClient


class WeatherDashboardAPI:
    def init(self, api_client: APIClient):
        self.api_client = api_client


    async def get_current_weather(self, location: str):
        data = await self.api_client.fetch_weather(location)
        # Пример адаптации данных – извлечение текущей погоды из полученного JSON
        current = data.get("current_condition", [{}])[0]
        return {
            "temperature": current.get("temp_C"),
            "feels_like": current.get("FeelsLikeC"),
            "condition": current.get("weatherDesc", [{}])[0].get("value"),
            "humidity": current.get("humidity"),
            "wind_speed": current.get("windspeedKmph")
        }

    async def get_forecast(self, location: str, days: int = 5):
        data = await self.api_client.fetch_weather(location)
        # Пример извлечения прогноза – обычно ключ другой (forecast)
        forecast = data.get("weather", [])
        # Приведение к нужному формату и выбор нужных дней
        return forecast[:days]