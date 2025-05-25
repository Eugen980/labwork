import aiohttp
import asyncio


class APIClient:
    def init(self, base_url: str):
        self.base_url = base_url


    async def fetch_weather(self, location: str):
       url = f"{self.base_url}/{location}"
       params = {"format": "j1"}
       async with aiohttp.ClientSession() as session:
           async with session.get(url, params=params) as response:
               if response.status != 200:
                   raise Exception("Ошибка при получении данных")
               data = await response.json()
               return data