from flask_restful import Resource, request

class UserResource(Resource):
    def post(self):
        json_payload = request.get_json()

        # return { 
        #     'data': { 
        #         'id': ,
        #         'attributes': { 
        #             'email': ,
        #             'api_key': 
        #         }
        #     }
        # }