from flask_restful import Resource, request
from api.models.user import User
from sqlalchemy import exc

class UserResource(Resource):
    def post(self):
        json_payload = request.get_json()

        if json_payload['password'] != json_payload['password_confirmation']:
            return {'error': 'Password must match password confirmation.'}, 400

        try:
            user = User(json_payload)
            user.save()
        except exc.IntegrityError as err: 
            return {'error': err.orig.diag.message_detail}, 400

        return_payload =  { 
            'data': { 
                'type': 'users',
                'id': user.id,
                'attributes': { 
                    'email': user.email,
                    'api_key': user.api_key
                }
            }
        }

        return return_payload, 201