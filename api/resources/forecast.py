from flask_restful import Resource, request
from datetime import datetime
import json
from api.services.geocode_service import GeocodeService
from api.services.weather_service import WeatherService

class ForecastResource(Resource):
    def get(self):
        location = request.args.getlist('location')
        return {'data': {
            'id': None, 
            'type': 'forecast', 
            'attributes': self._forecast_payload(location)
        }}

    # Call Service
    def _forecast_payload(self, location): 
        # convert location to coordinates
        coordinates = self._location_to_coordinates(location)
        raw_forecast = self._get_weather_forecast(coordinates)

        return {
            "current_weather": self._format_current_weather(raw_forecast), 
            "daily_weather": [],
            "hourly_weather": []
        }

    def _format_current_weather(self, forecast): 
        current_forecast = forecast['current']
        timezone_offset = forecast['timezone_offset']
        
        { 
            'datetime': self._time_converter(current_forecast['dt'], timezone_offset),
            'sunrise': self._time_converter(current_forecast['sunrise'], timezone_offset),
            'sunset': self._time_converter(current_forecast['sunset'], timezone_offset),
            'temperature': current_forecast['temp'],
            'feels_like': current_forecast['feels_like'],
            'humidity': current_forecast['humidity'],
            'uvi': current_forecast['uvi'],
            'visibility': current_forecast['visibility'],
            'conditions': current_forecast['weather'][0]['description'],
            'icon': current_forecast['weather'][0]['icon']
        }

    def _location_to_coordinates(self, location): 
        geocode_service = GeocodeService()
        response = geocode_service.geocode_address(location)
        coordinates = response.json()['results'][0]['locations'][0]['displayLatLng']
        return coordinates

    def _get_weather_forecast(self, coordinates):
        weather_service = WeatherService()
        forecast = weather_service.get_weather(coordinates)
        return json.loads(forecast.text)

    def _time_converter(self, unix_time_stamp, timezone_offset):
        dt = datetime.utcfromtimestamp(unix_time_stamp + timezone_offset)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

# pretty = json.loads(forecast.text)
# print(json.dumps(pretty, indent=2))