
from pymongo import MongoClient,ASCENDING,DESCENDING
from weather_api import WeatherApiClient
from settings import MONGODB_URI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QCompleter
from PyQt5.QtCore import QStringListModel
from PyQt5.uic import loadUi



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('weather_app.ui', self)
        self.setWindowTitle("WeatherApp")
        self.connect_mongodb()
        self.populate_country_list()
        self.populate_city_list()
        self.country_list.currentIndexChanged.connect(self.populate_city_list)
        self.setup_completers()
        self.setup_styles()

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
                background-color: black; 
                color: white; 
                font-size: 20px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: black;
                color: white;
                selection-background-color: gray;
            }
            QComboBox QLineEdit {
                color: white;  # Placeholder text color
            }
        """
        self.country_list.setStyleSheet(style)
        self.city_list.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

