from flask import Flask 
from flask_restful import Resource, Api
from config import config
from dotenv import load_dotenv
load_dotenv()

def create_app(env = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    api = Api(app)

    from api.resources.forecast import ForecastResource

    api.add_resource(ForecastResource, '/api/v1/forecast')
    return app 