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

    def get_hourly_weather_info(api_response,base_time, hours, max_time_window=3600):
        result = {}
        for hour in hours:
            target_time = base_time + timedelta(hours=hour)
            target_timestamp = target_time.timestamp()
            time_window = 0
            while time_window <= max_time_window:
                for entry in api_response['weather_data']['hourly']:
                    entry_timestamp = entry['dt']
                    if abs(entry_timestamp - target_timestamp) <= time_window:
                        result[hour] = entry
                        break
                if hour in result:
                    break
                time_window += 300  # Increase time window by 5 minutes
        return result
    
    def get_daily_weather_info(api_response, base_time, days, max_time_window=86400):
        result = {}
        for day in days:
            target_time = base_time + timedelta(days=day)
            target_timestamp = target_time.timestamp()
            time_window = 0
            while time_window <= max_time_window:
                for entry in api_response['weather_data']['daily']:
                    entry_timestamp = entry['dt']
                    if abs(entry_timestamp - target_timestamp) <= time_window:
                        result[day] = entry
                        break
                if day in result:
                    break
                time_window += 1800  # Increase time window by 30 minutes
        return result