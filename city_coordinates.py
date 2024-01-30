from settings import MONGODB_URI
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import json
import logging

logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

geolocator = Nominatim(user_agent="Infotech")

client = MongoClient(MONGODB_URI)
db = client["weather_database"]
collection = db['city_data']

json_data = []

for document in collection.find():
    city = document["city_municipality"]
    state = document["state_province"]
    country = document["country"]

    try:
        loc = geolocator.geocode(city + ',' + state + ',' + country)

        if loc:
            json = {
                "city": city,
                "country": country,
                "latitude": loc.latitude,
                "longitude": loc.longitude
            }
            collection.update_one(
                                {"_id": document["_id"]},
                                {
                                    "$set": {
                                        "lat": loc.latitude,
                                        "lon": loc.longitude
                                    }
                                }
                            )
            print(f"Updated document with city: {city}, {json}")
        else:
            logging.error(f"Failed to geocode coordinates for city: {city}, state: {state}, country: {country}")

    except Exception as e:
        logging.error(f"Error while geocoding coordinates for city: {city}, state: {state}, country: {country}. Error: {str(e)}")

print("Geocoding and update complete")
