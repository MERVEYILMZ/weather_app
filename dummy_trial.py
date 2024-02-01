import json
from datetime import datetime, timedelta
from weather_api import WeatherApiClient

weather_api_client = WeatherApiClient()

lat = 40.7127281
lon = -74.0060152

weather_data = weather_api_client.get_weather_data(lat, lon)

# weather_data = {
#     'city': 'Tilburg',
#     'country': 'Netherlands',
#     'weather_data': {
#         'lat': 51.5856,
#         'lon': 5.0661,
#         'timezone': 'Europe/Amsterdam',
#         'timezone_offset': 3600,
#         'current': {
#             'dt': 1706790538,
#             'sunrise': 1706771963,
#             'sunset': 1706804816,
#             'temp': 281.92,
#             'feels_like': 279.35,
#             'pressure': 1031,
#             'humidity': 76,
#             'dew_point': 277.93,
#             'uvi': 0.78,
#             'clouds': 75,
#             'visibility': 10000,
#             'wind_speed': 4.63,
#             'wind_deg': 270,
#             'weather': [
#                 {'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}
#             ]
#         },
#         'hourly': [
#             {
#                 'dt': 1706788800,
#                 'temp': 281.92,
#                 'feels_like': 279.34,
#                 'pressure': 1031,
#                 'humidity': 76,
#                 'dew_point': 277.93,
#                 'uvi': 0.78,
#                 'clouds': 75,
#                 'visibility': 10000,
#                 'wind_speed': 4.67,
#                 'wind_deg': 299,
#                 'wind_gust': 6.63,
#                 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}],
#                 'pop': 0
#             },
#             # Add more hourly data entries here
#         ]
#     }
# }

# Function to retrieve weather information for specific hours
def get_hourly_weather_info(base_time, hours, max_time_window=3600):
    result = {}
    for hour in hours:
        target_time = base_time + timedelta(hours=hour)
        target_timestamp = target_time.timestamp()
        time_window = 0
        while time_window <= max_time_window:
            for entry in weather_data['weather_data']['hourly']:
                entry_timestamp = entry['dt']
                if abs(entry_timestamp - target_timestamp) <= time_window:
                    result[hour] = entry
                    break
            if hour in result:
                break
            time_window += 300  # Increase time window by 5 minutes
    return result

# Current time in the dataset
#print (weather_data)
current_time = datetime.utcfromtimestamp(weather_data['weather_data']['current']['dt'])
print (current_time)


# Hours relative to the current time
hours_relative_to_current = [3, 6, 9, 12]

# Retrieve weather information for +3, +6, +9, and +12 hours
result_json = get_hourly_weather_info(current_time, hours_relative_to_current)

# Print the result
print(json.dumps(result_json, indent=2))