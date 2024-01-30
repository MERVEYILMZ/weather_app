from pymongo import MongoClient,ASCENDING,DESCENDING
from settings import MONGODB_URI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox
from PyQt5.uic import loadUi
from weather_api import WeatherApiClient


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        loadUi('weather_app.ui', self)
        self.setWindowTitle("WeatherApp")
        self.connect_mongodb()
        self.populate_country_list()
        self.populate_city_list()
        self.country_list.currentIndexChanged.connect(self.populate_city_list)

        #generate weatherapiclient with init
        self.weather_api_client = WeatherApiClient()

        # call this function whenever needed, preferably currentindexchanged for city
        self.retrieve_weather_data(lat=50.8676041, lon=4.3737121)


    def retrieve_weather_data(self,lat,lon):
        result = self.weather_api_client.get_weather_data(lat, lon)
        print (result)

    def connect_mongodb(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client["weather_database"]
        self.collection = self.db['city_data']

    def populate_country_list(self):
        countries = self.db['city_data'].distinct("country")
        for country in countries:
            self.country_list.addItem(country)
        
        

    def populate_city_list(self):
        
        self.filter_statu = self.country_list.currentText()
        self.city_list.clear()
        filter={
        'country': self.filter_statu
        }
      
        cities = self.db['city_data'].find(filter=filter).sort("population",DESCENDING)                                

        for city in cities:
            self.city_list.addItem(city["city_municipality"])

        # it = db.classuc.find({"age":{"$in":[25,35]}})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())