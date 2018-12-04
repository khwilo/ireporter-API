from flask import Flask
from flask_jwt_extended import JWTManager

from app.api.v1 import api_blueprint, auth_blueprint

from instance.config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
    