from flask_restful import reqparse, Resource

from app.api.v1.models.models import IncidenceModel

parser = reqparse.RequestParser()
parser.add_argument('type', type=str, required=True, help='Type cannot be blank!')
parser.add_argument('location', type=str, required=True, help='Location cannot be blank!')
parser.add_argument('comment', type=str, required=True, help='Comment cannot be blank!')

class RedFlagList(Resource):
    """Allows a request on a list of RedFlag items"""
    def post(self):
        data = parser.parse_args()

        red_flag = IncidenceModel(
                createdBy = 1,
                _type = data['type'],
                comment = data['comment'],
                location = data['location']
            )

        IncidenceModel.insert_an_incidence(red_flag.incidence_as_dict())

        return {
            "status": 201,
            "data": [
                {
                    "id": red_flag.get_id(),
                    "message": "Create red-flag record"
                }
            ]
        }, 201
    
    
    def get(self):
        incidences = IncidenceModel.get_all_incidences()
        if incidences == []:
            return {'message': 'no red-flag has been added yet'}, 404
        return {
            "status": 200,
            "data": incidences
        }, 200
    
class RedFlag(Resource):
    """Allows a request on a single RedFlag item"""
    def get(self, id):
        if id.isdigit():
            incidence = IncidenceModel.get_incidence_by_id(int(id))
            if incidence == {}:
                return {'message': "red flag with id {} doesn't exist".format(id)}, 404
            return {
                "status": 200,
                "data": [incidence]
            }
        else:
            return {'message': "red-flag id must be an Integer"}, 400