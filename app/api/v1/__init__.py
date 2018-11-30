from flask import Blueprint
from flask_restful import Api
from app.api.v1.views import *

api_blueprint = Blueprint("api", __name__)

api = Api(api_blueprint)

api.add_resource(RedFlagList, '/red-flags')
api.add_resource(RedFlag, '/red-flags/<id>')
api.add_resource(RedFlagLocation, '/red-flags/<id>/location')
api.add_resource(RedFlagComment, '/red-flags/<id>/comment')