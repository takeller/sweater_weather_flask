import os 
import requests

class WeatherService:
    url = 'https://api.openweathermap.org/data/2.5/onecall'

    def get_weather(self, coordinates):
        payload = { 'appid': os.getenv('OPENWEATHER_API_KEY'), 'lat': coordinates['lat'], 'lon': coordinates['lng'], 'exclude': 'minutely,alerts'}
        response = requests.get(self.url, params = payload)
        return response