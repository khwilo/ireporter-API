'''This module represents a User entity'''
from datetime import datetime

USERS = []

class UserModel:
    '''Entity representation for a user'''
    def __init__(self, firstname, lastname, othernames, email, phoneNumber, username, isAdmin, password):
        self.id = len(USERS) + 1
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.registered = str(datetime.utcnow())
        self.isAdmin = isAdmin
        self.password = password

    def get_user_id(self):
        '''Returns the id of the user'''
        return self.id

    @staticmethod
    def add_a_user(user):
        '''Add a new user'''
        USERS.append(user)

    @staticmethod
    def get_user_by_id(id):
        '''Return a user with the given in'''
        user = {}
        for u in range(len(USERS)):
            if USERS[u].get('id') == id:
                user = USERS[u]
        return user

    @staticmethod
    def get_user_by_username(username):
        '''Return a user with the given username'''
        user = {}
        for u in range(len(USERS)):
            if USERS[u].get('username') == username:
                user = USERS[u]
        return user

    @staticmethod
    def get_all_users():
        '''Return all users as a list'''
        return USERS

    @staticmethod
    def delete_a_user_by_id():
        '''Delete a given user by id'''
        global USERS
        USERS = list(filter(lambda u: u['id'] != id, USERS))

    def user_as_dict(self):
        '''Convert user object to a dictionary'''
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othernames': self.othernames,
            'email': self.email,    
            'phoneNumber': self.phoneNumber,
            'username': self.username,
            'registered': self.registered,
            'isAdmin': self.isAdmin,
            'password': self.password
        }
        