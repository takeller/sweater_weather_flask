from flask_restful import Resource, request
class ForecastResource(Resource):
    def get(self):
        location = request.args
        return {'data': {
            'id': None, 
            'type': 'forecast', 
            'attributes': _forecast_payload(location)
        }}

# Call Service
def _forecast_payload(location): 
    return {}