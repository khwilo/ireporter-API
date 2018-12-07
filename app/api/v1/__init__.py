from flask import Blueprint
from flask_restful import Api
from app.api.v1.views import *

api_blueprint = Blueprint("api", __name__, url_prefix='/api/v1')
auth_blueprint = Blueprint("auth", __name__, url_prefix='/auth')

api = Api(api_blueprint)
auth_api = Api(auth_blueprint)

api.add_resource(RedFlagList, '/red-flags')
api.add_resource(RedFlag, '/red-flags/<id>')
api.add_resource(RedFlagLocation, '/red-flags/<id>/location')
api.add_resource(RedFlagComment, '/red-flags/<id>/comment')
api.add_resource(RedFlagStatus, '/red-flags/<id>/status')

auth_api.add_resource(UserRegistration, '/register')
auth_api.add_resource(UserLogin, '/login')