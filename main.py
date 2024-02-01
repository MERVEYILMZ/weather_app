import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QCompleter, QLabel
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from datetime import datetime
from PyQt5 import QtGui, QtCore
import requests
from pymongo import MongoClient, DESCENDING
from weather_api import WeatherApiClient
from settings import MONGODB_URI

############################################################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('weather_app.ui', self)
        self.setWindowTitle("WeatherApp")
        self.connect_mongodb()
        self.populate_country_list()
        self.country_list.currentIndexChanged.connect(self.populate_city_list)
        self.city_list.currentIndexChanged.connect(self.city_changed)
        self.setup_completers()
        self.setup_styles()
        self.weather_api_client = WeatherApiClient()
############################################################################################################
    def city_changed(self):
        city_name = self.city_list.currentText()
        if city_name:
            city_data = self.collection.find_one({"city_municipality": city_name})
            if city_data:
                lat = city_data.get('lat')
                lon = city_data.get('lon')
                self.retrieve_weather_data(lat, lon)
############################################################################################################
    def retrieve_weather_data(self, lat, lon):
        try:
            result = self.weather_api_client.get_weather_data(lat, lon)
            weather_data = result['weather_data']['current']
            hourly_data = result['weather_data']['hourly']
            daily_data = result['weather_data']['daily']
            self.update_current_weather(weather_data)
            self.update_hourly_forecast(hourly_data)
            self.update_daily_forecast(daily_data)
        except KeyError as e:
            print(f"Key error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
############################################################################################################
    def update_current_weather(self, weather_data):
        temperature_c = weather_data['temp'] - 273.15
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        sunrise = weather_data['sunrise']
        weather_description = weather_data['weather'][0]['description']
        weather_icon = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"

        self.temparature_label.setText(f"{temperature_c:.2f}°C")
        self.humidity_label.setText(f"{humidity}%")
        self.wind_label.setText(f"{wind_speed} m/s")
        sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
        self.sunrise_label.setText(sunrise_time)
        self.current_weather_label.setText(weather_description)
        self.set_icon(self.current_weather_icon, icon_url)
############################################################################################################
    def update_hourly_forecast(self, hourly_data):
        for i in range(1, 5):
            temp_label = getattr(self, f"forecast_temp{i}")
            icon_label = getattr(self, f"forecast_icon{i}")
            data = hourly_data[i * 3 - 3]  # 0, 3, 6, 9 for +3, +6, +9, +12 hours
            temp_c = data['temp'] - 273.15
            icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
            temp_label.setText(f"{temp_c:.1f}°C")
            self.set_icon(icon_label, icon_url)
############################################################################################################
    def update_daily_forecast(self, daily_data):
        for day_index in range(1, 4):  # For +1, +2, and +3 days
            temp_label = getattr(self, f"forecast_temp1_{day_index}")
            hum_label = getattr(self, f"forecast_hum1_{day_index}")
            wind_label = getattr(self, f"forecast_wind1_{day_index}")

            # Get data for the corresponding day
            data = daily_data[day_index]
            temp_day = data['temp']['day'] - 273.15
            humidity = data['humidity']
            wind_speed = data['wind_speed']

            # Update labels with forecast data
            temp_label.setText(f"{temp_day:.1f}°C")
            hum_label.setText(f"Humidity: {humidity}%")
            wind_label.setText(f"Wind: {wind_speed} m/s")
############################################################################################################    
    
    def set_icon(self, label, icon_url):
        response = requests.get(icon_url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            label.setPixmap(pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio))

    def connect_mongodb(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client["weather_database"]
        self.collection = self.db['city_data']

    def populate_country_list(self):
        self.country_list.clear()
        countries = self.collection.distinct("country")
        self.country_list.addItems(countries)
        self.country_list_model = QStringListModel(countries)
        self.country_completer = QCompleter(self.country_list_model, self)
        self.country_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.country_list.setCompleter(self.country_completer)
        self.country_list.setEditable(True)
        self.country_list.setPlaceholderText("Search countries...")

############################################################################################################

    def populate_city_list(self):
        self.city_list.clear()
        filter_statu = self.country_list.currentText()
        filter = {'country': filter_statu}
        cities = self.db['city_data'].find(filter=filter).sort("population", DESCENDING)
        city_names = [city["city_municipality"] for city in cities]
        self.city_list.addItems(city_names)
        self.city_list_model = QStringListModel(city_names)
        self.city_completer = QCompleter(self.city_list_model, self)
        self.city_completer.setCaseSensitivity(False)
        self.city_list.setCompleter(self.city_completer)
        self.city_list.setEditable(True)
        self.city_list.setPlaceholderText("Search cities...")
############################################################################################################

    def setup_completers(self):
        self.populate_country_list()
        self.populate_city_list()
############################################################################################################

    def setup_styles(self):
        style = """
            QComboBox { 
                background-color: white; 
                color: black; 
                font-size: 20px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: gray;
                font-size: 18px;

            }
            QComboBox QLineEdit {
                color: black;  # Placeholder text color
                font-size: 20px;

            }
        """
        self.country_list.setStyleSheet(style)
        self.city_list.setStyleSheet(style)
############################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

