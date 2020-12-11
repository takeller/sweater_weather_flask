from flask import Flask 
from flask_restful import Resource, Api
from config import config
from dotenv import load_dotenv
from .models import db
load_dotenv(override=True)

def create_app(env = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    api = Api(app)
    db.init_app(app)

    from api.resources.forecast import ForecastResource
    from api.resources.user import UserResource

    api.add_resource(ForecastResource, '/api/v1/forecast')
    api.add_resource(UserResource, '/api/v1/users')
    return app 