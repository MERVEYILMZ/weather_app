import requests
from settings import OPENWEATHER_KEY, MONGODB_URI
from pymongo import MongoClient

class WeatherApiClient:
    def __init__(self):
        self.api_key = OPENWEATHER_KEY
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['weather_database']
        self.collection = self.db['city_data']
        self.exclude = "minutely,alerts"

    def get_weather_data(self, lat, lon):
        city_data = self.collection.find_one({"lat": lat, "lon": lon})

        if city_data:
            city = city_data["city_municipality"]
            country = city_data["country"]
            api_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={self.exclude}&appid={self.api_key}'
            response = requests.get(api_url)

            if response.status_code == 200:
                weather_data = response.json()
                return {"city": city, "country": country, "weather_data": weather_data}
            else:
                print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")

        else:
            print(f"Error: City data not found for lat={lat}, lon={lon}")
