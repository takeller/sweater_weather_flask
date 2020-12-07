import os
import requests

class GeocodeService:
    url = "http://www.mapquestapi.com/geocoding/v1/address"

    def geocode_address(self, location):
        payload = { "key": os.getenv('MAPQUEST_API_KEY'), "location": location}
        return requests.get(self.url, params = payload)