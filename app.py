import sys
import os

import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')


class WeatherDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Погодный Дашборд')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText('Введите локацию')
        layout.addWidget(self.location_input)

        self.search_button = QPushButton('Поиск', self)
        self.search_button.clicked.connect(self.search_weather)
        layout.addWidget(self.search_button)

        self.weather_info = QLabel('Информация о погоде', self)
        layout.addWidget(self.weather_info)

        self.setLayout(layout)

    def search_weather(self):
        location = self.location_input.text()
        if location:
            current_weather = self.get_weather(location)
            forecast = self.get_forecast(location)
            self.display_weather_info(current_weather, forecast)

    def get_weather(self, location):
        url = f"{BASE_URL}weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()

    def get_forecast(self, location):
        url = f"{BASE_URL}forecast?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()

    def display_weather_info(self, current_weather, forecast):
        if current_weather.get('cod') != 200:
            self.weather_info.setText('Ошибка: не удалось получить данные.')
            return

        weather_description = current_weather['weather'][0]['description']
        temperature = current_weather['main']['temp']
        humidity = current_weather['main']['humidity']
        wind_speed = current_weather['wind']['speed']

        forecast_text = "Прогноз на 5 дней:\n"
        for i in range(0, 40, 8):
            day_forecast = forecast['list'][i]
            date = day_forecast['dt_txt']
            temp = day_forecast['main']['temp']
            desc = day_forecast['weather'][0]['description']
            forecast_text += f"{date}: {temp}°C, {desc}\n"

        self.weather_info.setText(
            f"Текущая погода: {weather_description}\n"
            f"Температура: {temperature}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с\n\n"
            f"{forecast_text}"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherDashboard()
    ex.show()
    sys.exit(app.exec_())