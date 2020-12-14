import os 
from dotenv import load_dotenv
load_dotenv()

class Development(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Testing(object): 
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

config = { 
    'development': Development, 
    'testing': Testing
}