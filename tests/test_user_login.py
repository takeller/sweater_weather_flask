import unittest
import json

from api.models import db
from api import create_app
from . import assert_payload_type

class UserTest(unittest.TestCase):
    def setUp(self): 
        self.app = create_app('testing')
        self.app_context = self.app.app_context
        self.client = self.app.test_client()

        self.user_login =  { 
            'email': 'takeller@gmail.com',
            'password': 'password'
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()

class UserLoginTest(UserTest): 
    def test_happypath_user_login(self):
        response = self.client.post('api/v1/sessions', json = self.user_login, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})

        self.assertEqual(200, response.status_code)

        json_respoonse = json.loads(response.data)
        json_data = json_respoonse['data']

        self.assertEqual(json_data['type'], 'users')
        assert_payload_type(self, json_data, 'id', int)
        assert_payload_type(self, json_data, 'attributes', dict)
        assert_payload_type(self, json_data['attributes'], 'email', str)
        assert_payload_type(self, json_data['attributes'], 'api_key', str)

    def test_sadpath_user_login(self): 
        # Incorrect password
        json_payload = { 
            'email': 'takeller@gmail.com',
            'password': 'password1'
        }

        response = self.client.post('api/v1/sessions', json = self.user_login, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})

        self.assertEqual(401, response.status_code)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['error'], 'Incorrect username or password')

        # Incorrect Email
        json_payload = { 
            'email': 'takeller50@gmail.com',
            'password': 'password'
        }

        response = self.client.post('api/v1/sessions', json = self.user_login, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})

        self.assertEqual(401, response.status_code)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['error'], 'Incorrect username or password')