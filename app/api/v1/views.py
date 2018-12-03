from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from app.api.v1.models.incidence import IncidenceModel
from app.api.v1.models.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('type', type=str, required=True, help='Type cannot be blank!')
parser.add_argument('location', type=str, required=True, help='Location cannot be blank!')
parser.add_argument('comment', type=str, required=True, help='Comment cannot be blank!')

class RedFlagList(Resource):
    """Allows a request on a list of RedFlag items"""
    @jwt_required
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

    def delete(self, id):
        if id.isdigit():
            incidence = IncidenceModel.get_incidence_by_id(int(id))
            if incidence == {}:
                return {'message': "red flag with id {} doesn't exit".format(id)}, 404
            else:
                IncidenceModel.delete_by_id(int(id))
                return {
                    "status": 200,
                    "data": [{
                        "id": int(id),
                        "message": "red-flag record has been deleted"
                    }]
                }, 200
        else:
            return {'message': "incidence id must be an Integer"}, 400

class RedFlagLocation(Resource):
    """Allows a request on a single RedFlag Location"""
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str, required=True, help='Location cannot be blank!')
        data = parser.parse_args()

    
        if id.isdigit():
            incidence = IncidenceModel.get_incidence_by_id(int(id))
            if incidence == {}:
                return {'message': "red flag with id {} doesn't exit".format(id)}, 404
            else:
                incidence.update(data)
                return {
                    "status": 200,
                    "data": [{
                        "id": id,
                        "message": "Updated red-flag record’s location"
                    }]
                }
        return {'message': "red-flag id must be an Integer"}, 400
        
class RedFlagComment(Resource):
    """Allows a request on a single RedFlag comment"""
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('comment', type=str, required=True, help='Comment cannot be blank!')
        data = parser.parse_args()

        if id.isdigit():
            incidence = IncidenceModel.get_incidence_by_id(int(id))
            if incidence == {}:
                return {'message': "red flag with id {} doesn't exit".format(id)}, 404
            else:
                incidence.update(data)
                return {
                    "status": 200,
                    "data": [{
                        "id": id,
                        "message": "Updated red-flag record’s comment"
                    }]
                }
        else:
            return {'message': "red-flag id must be an Integer"}, 400

# USER MODEL #
class UserRegistration(Resource):
    """Registers a new user"""
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, required=True, help='Firstname cannot be blank!')
        parser.add_argument('lastname', type=str, required=True, help='Lastname cannot be blank!')
        parser.add_argument('othernames', type=str, required=True, help='Othernames cannot be blank!')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank!')
        parser.add_argument('phoneNumber', type=str, required=True, help='PhoneNumber cannot be blank!')
        parser.add_argument('username', type=str, required=True, help='Username cannot be blank!')
        parser.add_argument('isAdmin', type=bool, required=True, help='IsAdmin cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')
        data = parser.parse_args()

        # Create an instance of the user
        user = UserModel(
            firstname = data['firstname'],
            lastname = data['lastname'],
            othernames = data['othernames'],
            email = data['email'],
            phoneNumber = data['phoneNumber'],
            username = data['username'],
            isAdmin = data['isAdmin'],
            password = UserModel.generate_password_hash(data['password'])
        )

        username = data['username']
        password = data['password']

        # Validate the username
        if username.isdigit():
            return {'message': 'username cannot consist of digits only'}, 400
        if not username or not username.split():
            return {'message': 'username cannot be empty'}

        if not password or not password.split():
            return {'message': 'password cannot be empty'}
        
        users = UserModel.get_all_users() # Get all list of users 

        if next(filter(lambda u: u['username'] == username, users), None):
            return {
                'message': "A user with the username '{}' already exists!".format(username)
            }
        
        UserModel.add_a_user(user.user_as_dict())
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])

        return {
            "status": 201,
            "data": [
                {
                    "id": user.get_user_id(),
                    "message": "Create user record",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            ]
        }, 201

class UserLogin(Resource):
    '''Allow a registered user to login'''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')
        data = parser.parse_args()

        current_user = UserModel.get_user_by_username(data['username'])

        if not current_user:
            return {'message': "User with username '{}' doesn't exist!".format(data['username'])}, 400

        if UserModel.verify_password_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 401
