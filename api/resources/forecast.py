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
            "daily_weather": self._format_daily_weather(raw_forecast),
            "hourly_weather": self._format_hourly_weather(raw_forecast)
        }

    def _get_weather_forecast(self, coordinates):
        weather_service = WeatherService()
        forecast = weather_service.get_weather(coordinates)
        return json.loads(forecast.text)
        
    def _format_current_weather(self, forecast): 
        current_forecast = forecast['current']
        timezone_offset = forecast['timezone_offset']
        
        return { 
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

    def _format_daily_weather(self, forecast): 
        timezone_offset = forecast['timezone_offset']
        daily_forecasts = forecast['daily'][0:6]

        for i, daily_forecast in enumerate(daily_forecasts): 
            formatted_forecast = { 
            'date': self._time_converter(daily_forecast['dt'], timezone_offset),
            'sunrise': self._time_converter(daily_forecast['sunrise'], timezone_offset),
            'sunset': self._time_converter(daily_forecast['sunset'], timezone_offset),
            'max_temp': daily_forecast['temp']['max'],
            'min_temp': daily_forecast['temp']['min'],
            'conditions': daily_forecast['weather'][0]['description'],
            'icon': daily_forecast['weather'][0]['icon']
            }
            daily_forecasts[i] = formatted_forecast

        return daily_forecasts

    def _format_hourly_weather(self, forecast): 
        timezone_offset = forecast['timezone_offset']
        hourly_forecasts = forecast['hourly'][0:9]

        for i, hourly_forecast in enumerate(hourly_forecasts): 
            formatted_forecast = { 
                'time': self._time_converter(hourly_forecast['dt'], timezone_offset, True),
                'temperature': hourly_forecast['temp'],
                'wind_speed': str(hourly_forecast['wind_speed']) + ' mph',
                'wind_direction': self._deg_to_cardinal(hourly_forecast['wind_deg']),
                'conditions': hourly_forecast['weather'][0]['description'],
                'icon': hourly_forecast['weather'][0]['icon']
            }
            hourly_forecasts[i] = formatted_forecast
        return hourly_forecasts

    def _location_to_coordinates(self, location): 
        geocode_service = GeocodeService()
        response = geocode_service.geocode_address(location)
        coordinates = response.json()['results'][0]['locations'][0]['displayLatLng']
        return coordinates


    def _time_converter(self, unix_time_stamp, timezone_offset, time_only = False):
        dt = datetime.utcfromtimestamp(unix_time_stamp + timezone_offset)
        if time_only == True: 
            return dt.strftime('%-I:%M %p')

        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def _deg_to_cardinal(self, deg):
        if deg > 360 or deg < 0: 
            return 'Degrees out of bounds'
        elif deg > 337.5 or deg <= 22.5:
            return 'N'
        elif deg > 22.5 and deg <= 67.5:
            return 'NE'
        elif deg > 67.5 and deg <= 112.5:
            return 'E'
        elif deg > 112.5 and deg <= 157.5:
            return 'SE'
        elif deg >  157.5 and deg <= 202.5:
            return 'S'
        elif deg > 202.5 and deg <= 247.5:
            return 'SW'
        elif deg > 247.5 and deg <= 292.5:
            return 'W'
        elif deg > 292.5 and deg <= 337.5:
            return 'NW'

# pretty = json.loads(forecast.text)
# print(json.dumps(pretty, indent=2))