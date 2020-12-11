from marshmallow import fields, Schema
import os
import binascii
from . import db 

class User(db.Model): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, nullable = False, unique=True)
    password = db.Column(db.String, nullable = False)
    api_key = db.Column(db.String)

    def __init__(self, data):
        self.email = data.get('email')
        self.password = data.get('password')
        self.api_key = binascii.b2a_hex(os.urandom(16))

    