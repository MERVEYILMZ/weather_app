
from pymongo import MongoClient,ASCENDING,DESCENDING
from weather_api import WeatherApiClient
from settings import MONGODB_URI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QCompleter
from PyQt5.QtCore import QStringListModel
from PyQt5.uic import loadUi
from datetime import datetime
from PyQt5 import QtGui, QtCore
import requests
from datetime import datetime
from PyQt5.QtCore import QTimer, QDateTime



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('weather_app.ui', self)
        self.setWindowTitle("WeatherApp")
        self.connect_mongodb()
        self.populate_country_list()
        #self.populate_city_list()
        self.country_list.currentIndexChanged.connect(self.populate_city_list)
        self.city_list.currentIndexChanged.connect(self.city_changed)  # Connect signal to the new slot
        self.setup_completers()
        self.setup_styles()

        # Display the current time and date.
        self.update_datetime_label()
        timer = QTimer(self)
        # Set QTimer to trigger every second.
        timer.timeout.connect(self.update_datetime_label)
        timer.start(1000)  # The duration in milliseconds

        # Generate WeatherApiClient with init
        self.weather_api_client = WeatherApiClient()

        # Call this function whenever needed, preferably currentIndexChanged for city
        # self.retrieve_weather_data(lat=50.8676041, lon=4.3737121)

    def update_datetime_label(self):
        bugun = QDateTime.currentDateTime()
        tarih_ve_saat = bugun.toString("dd-MM-yyyy HH:mm")
        self.date_label.setText(tarih_ve_saat)


    def city_changed(self):
        # Get the selected city name
        city_name = self.city_list.currentText()
        if city_name:
            # Fetch the latitude and longitude from your MongoDB database
            city_data = self.collection.find_one({"city_municipality": city_name})
            if city_data:
                lat = city_data.get('lat')
                lon = city_data.get('lon')
                # Call the method to update the weather information
                self.retrieve_weather_data(lat, lon)


    def retrieve_weather_data(self, lat, lon):
        try:
            result = self.weather_api_client.get_weather_data(lat, lon)
            print(result)
            
            # Navigate through the nested dictionary to get the required data
            weather_data = result['weather_data']['current']
            temperature_k = weather_data['temp']  # Temperature in Kelvin
            humidity = weather_data['humidity']
            wind_speed = weather_data['wind_speed']
            sunrise = weather_data['sunrise']
            weather_description = weather_data['weather'][0]['description']
            weather_icon = weather_data['weather'][0]['icon']

            # Convert Kelvin to Celsius for display
            temperature_c = temperature_k - 273.15
            
            weather_description = weather_data['weather'][0]['description']
            
            # Set the weather description
            self.current_weather_label.setText(weather_description)

            # Update the labels with the data
            self.temparature_label.setText(f"{temperature_c:.2f}°C")  # Display temperature in Celsius
            self.humidity_label.setText(f"{humidity}%")
            self.wind_label.setText(f"{wind_speed} m/s")
            
            # Convert the sunrise UNIX timestamp to a readable format
            sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
            self.sunrise_label.setText(sunrise_time)

            # Set the weather icon
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"  # Example URL, adjust as needed
            self.current_weather_icon.setPixmap(QtGui.QPixmap(icon_url))

            # Set the weather description
            self.current_weather_label.setText(weather_description)
            
            weather_icon = weather_data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"
            
            
            try:
                response = requests.get(icon_url)
                response.raise_for_status()  # Raise an error on a bad status
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(response.content)
                self.current_weather_icon.setPixmap(pixmap)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download icon: {e}")
                
            
        except KeyError as e:
            print(f"Key error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

            
    


    def connect_mongodb(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client["weather_database"]
        self.collection = self.db['city_data']

    def populate_country_list(self):
        self.country_list.clear()
        countries = self.db['city_data'].distinct("country")
        for country in countries:
            self.country_list.addItem(country)
        self.country_list_model = QStringListModel(countries)
        self.country_completer = QCompleter(self.country_list_model, self)
        self.country_completer.setCaseSensitivity(False)
        self.country_list.setCompleter(self.country_completer)
        self.country_list.setEditable(True)
        self.country_list.setPlaceholderText("Search countries...")

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

    def setup_completers(self):
        self.populate_country_list()
        self.populate_city_list()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

