from flask_restful import Resource, request
from api.services.geocode_service import GeocodeService

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

        return {
            "current_weather": {}, 
            "daily_weather": [],
            "hourly_weather": []
        }

    def _get_current_weather(self, location): 
        return 

    def _location_to_coordinates(self, location): 
        geocode_service = GeocodeService()
        response = geocode_service.geocode_address(location)
        coordinates = response.json()['results'][0]['locations'][0]['displayLatLng']
        return coordinates