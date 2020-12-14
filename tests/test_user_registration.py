import json
import unittest

from random import randint
from api.models import db
from api import create_app 
from . import assert_payload_type
class UserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context
        self.client = self.app.test_client()

        self.user_registration_payload = { 
            'email': 'taylor@gmail.com',
            'password': 'password', 
            'password_confirmation': 'password'
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()
    
class PostUserTest(UserTest): 
    def test_happypath_post_user(self):
        response = self.client.post('api/v1/users', json = self.user_registration_payload, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})

        self.assertEqual(201, response.status_code)

        json_response = json.loads(response.data)
        json_data = json_response['data']

        self.assertEqual(json_data['type'], 'users')
        assert_payload_type(self, json_data, 'id', int)
        assert_payload_type(self, json_data, 'attributes', dict)
        assert_payload_type(self, json_data['attributes'], 'email', str)
        assert_payload_type(self, json_data['attributes'], 'api_key', str)

    def test_sadpath_post_user(self): 
        # Duplicate email address
        response = self.client.post('api/v1/users', json = self.user_registration_payload, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})
        response = self.client.post('api/v1/users', json = self.user_registration_payload, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})

        self.assertEqual(400, response.status_code)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['error'], 'Key (email)=(taylor@gmail.com) already exists.')

        # Non-matching passwords
        json_payload = { 
            'email': 'taylor' + str(randint(1,10000)) + '@gmail.com',
            'password': 'password1', 
            'password_confirmation': 'password'
        }
        response = self.client.post('api/v1/users', json = json_payload, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})

        self.assertEqual(400, response.status_code)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['error'], 'Password must match password confirmation.')
