import requests
from settings import OPENWEATHER_KEY, MONGODB_URI
from pymongo import MongoClient
from datetime import datetime, timedelta

class WeatherApiClient:
    def __init__(self):
        self.api_key = OPENWEATHER_KEY
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['weather_database']
        self.collection = self.db['city_data']
        self.exclude = "minutely,alerts"

    def get_weather_data(self, lat, lon):
        """
        Retrieves weather data for a given latitude and longitude using the OpenWeatherMap API.

        Args:
            lat (float): The latitude coordinate of the location.
            lon (float): The longitude coordinate of the location.

        Returns:
            dict: A dictionary containing the following keys:
                - 'city': The name of the city corresponding to the latitude and longitude.
                - 'country': The name of the country corresponding to the latitude and longitude.
                - 'weather_data': A dictionary containing weather data retrieved from the OpenWeatherMap API.
                This dictionary structure follows the format specified by the OpenWeatherMap API documentation.

        Prints an error message if city data is not found in the MongoDB collection for the provided latitude and longitude.
        Prints an error message if there is an issue fetching weather data from the OpenWeatherMap API.
        """
        city_data = self.collection.find_one({"lat": lat, "lon": lon})

        if city_data:
            city = city_data["city_municipality"]
            country = city_data["country"]
            api_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={self.exclude}&appid={self.api_key}'
            
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                weather_data = response.json()
                return {"city": city, "country": country, "weather_data": weather_data}

            except requests.RequestException as e:
                print(f"Error: Unable to fetch weather data. {e}")

        else:
            print(f"Error: City data not found in MondoDB for lat={lat}, lon={lon}")

