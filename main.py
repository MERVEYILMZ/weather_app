from pymongo import MongoClient
from settings import MONGODB_URI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('weather_app.ui', self)
        self.setWindowTitle("WeatherApp")
        self.connect_mongodb()
        self.populate_country_list()
        self.populate_city_list()

    def connect_mongodb(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client["weather_database"]
        self.collection = self.db['city_data']

    def populate_country_list(self):
        countries = self.db['city_data'].distinct("country")
        for country in countries:
            self.country_list.addItem(country)

    def populate_city_list(self):
        cities = self.db['city_data'].distinct("city_municipality")
        for city in cities:
            self.city_list.addItem(city)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())