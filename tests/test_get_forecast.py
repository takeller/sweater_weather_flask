import json 
import unittest 

from api import create_app 
from . import assert_payload_type

class ForecastTest(unittest.TestCase):

    def setUp(self): 
        self.app = create_app('testing')
        self.app_context = self.app.app_context
        # self.app_context.push()
        self.client = self.app.test_client()

class GetForecastTest(ForecastTest):
    def test_happypath_get_forecast(self):
        response = self.client.get('/api/v1/forecast?location=denver,co', headers={'Content-Type': 'application/json'})

        self.assertEqual(200, response.status_code)

        json_response = json.loads(response.data)
        json_data = json_response['data']

        self.assertEqual(json_data['id'], None)
        self.assertEqual(json_data['type'], 'forecast')

        # Forecast Attributes
        self.assertIn('attributes', json_data)

        forecast_attributes = json_data['attributes']

        self.assertIn('current_weather', forecast_attributes)
        assert_payload_type(self, forecast_attributes, 'daily_weather', list)
        assert_payload_type(self, forecast_attributes, 'hourly_weather', list)
        
        # 5 Days of daily weather
        self.assertEqual(len(forecast_attributes['daily_weather']), 6)
        # 8 Hours of hourly weather
        # self.assertEqual(len(forecast_attributes['hourly_weather']), 8)

        # Current Weather
        current_weather = forecast_attributes['current_weather']

        assert_payload_type(self, current_weather, 'datetime', str)
        assert_payload_type(self, current_weather, 'sunrise', str)
        assert_payload_type(self, current_weather, 'sunset', str)
        assert_payload_type(self, current_weather, 'temperature', float)
        assert_payload_type(self, current_weather, 'feels_like', float)
        assert_payload_type(self, current_weather, 'humidity', int)
        assert_payload_type(self, current_weather, 'uvi', float)
        assert_payload_type(self, current_weather, 'visibility', int)
        assert_payload_type(self, current_weather, 'conditions', str)
        assert_payload_type(self, current_weather, 'icon', str)

        # Daily Weather
        daily_weather = forecast_attributes['daily_weather']

        for day in daily_weather: 
            assert_payload_type(self, day, 'date', str)
            assert_payload_type(self, day, 'sunrise', str)
            assert_payload_type(self, day, 'sunset', str)
            assert_payload_type(self, day, 'max_temp', float)
            assert_payload_type(self, day, 'min_temp', float)
            assert_payload_type(self, day, 'conditions', str)
            assert_payload_type(self, day, 'icon', str)
        
        # Hourly Weather
        hourly_weather = forecast_attributes['hourly_weather']
        for hour in hourly_weather:
            assert_payload_type(self, hour, 'time', str)
            assert_payload_type(self, hour, 'wind_speed', str)
            assert_payload_type(self, hour, 'wind_direction', str)
            assert_payload_type(self, hour, 'conditions', str)
            assert_payload_type(self, hour, 'icon', str)