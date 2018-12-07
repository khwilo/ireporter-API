import unittest
import os 
import json

from app import create_app
from app.api.v1.models.incidence import IncidenceModel, INCIDENCES
from app.api.v1.models.user import UserModel, USERS

class IncidenceTestCase(unittest.TestCase):
    """This class represents the Incidence test case"""
    def setUp(self):
        """Define the test variables and initialize the application"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.incidences = {
            "createdBy": 1,
            "type": "RED-FLAG",
            "comment":  "comment",
            "location":  "12N3E"
        }

        self.regular_user = {
            "firstname": "john",
            "lastname": "doe",
            "othernames": "foo",
            "email": "joe@test.com",
            "phoneNumber": "0700000000",
            "username": "jondo",
            "isAdmin": False,
            "password": "12345"
        }

        self.regular_user_login = {
            "username": "jondo",
            "password": "12345"
        }

        self.admin_user = {
            "firstname": "jane",
            "lastname": "doe",
            "othernames": "bar",
            "email": "jane@test.com",
            "phoneNumber": "0711111111",
            "username": "bando",
            "isAdmin": True,
            "password": "56789"
        }

        self.admin_user_login = {
            "username": "bando",
            "password": "56789"
        }

    def get_accept_content_type_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_authentication_headers(self, access_token):
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = "Bearer {}".format(access_token)
        return authentication_headers
    
    def test_unauthorized_red_flag_creation(self):
        """
        Test that an unauthorized red flag creation results in a 401 error.
        Context: Provide no authorization header
        """
        r_user = self.client().post('/auth/register', headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        l_user = self.client().post('/auth/login', headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        res = self.client().post('/api/v1/red-flags', headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.incidences), content_type="application/json")
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 401)
        self.assertEqual("Missing Authorization Header", response_msg["msg"])

    
    def test_admin_cannot_create_red_flag(self):
        """
        Test that administrators are not allowed to create red flags.
        """
        res = self.client().post('/auth/register', headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.admin_user_login))
        self.assertEqual(res.status_code, 200)
        
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences))
        self.assertEqual(res.status_code, 401)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Only regular users can create a red-flag", response_msg["message"])

    
    def test_authorized_regular_user_can_create_red_flag(self):
        """
        Test whether the API can create a red flag
        Allow only registered regular user.
        Raise an error if user is an administrator.
        """
        res = self.client().post('/auth/register', headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        res = self.client().post('/auth/login', headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences))
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(201, response_msg["status"])
        self.assertEqual("Create red-flag record", response_msg["data"][0]["message"])

    def test_unauthorized_cannot_fetch_all_red_flags(self):
        """
        Test whether the API cannot allow a user to fetch all red flags 
        without an access token
        """
        res = self.client().get('/api/v1/red-flags')
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 401)
        self.assertEqual("Missing Authorization Header", response_msg["msg"])

    
    def test_fetching_all_red_flags(self):
        """Test whether the API can fetch all red flags"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user)) # Register a new user
        self.assertEqual(res.status_code, 201) # Confirm if the new user has been created
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login)) # Log in a registered user
        self.assertEqual(res.status_code, 200) # Confirm if the registered user has been logged in
        response_msg = json.loads(res.data.decode("UTF-8")) # Fetch the response message from loggin in
        access_token = response_msg['access_token'] # Fetch the access token from loggin in
        res = self.client().post('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences)) # Create a new post
        self.assertEqual(res.status_code, 201) # Confirm if the new post has been created
        res = self.client().get('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token)) # Fetch all posts that have been created
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(200, response_msg["status"])
        self.assertEqual(IncidenceModel.get_all_incidences(), response_msg["data"])
    
    def test_unauthorized_user_cannot_fetch_one_red_flag(self):
        """
        Test that the API cannot allow one to fetch a specific red flag 
        by its ID without providing an access token
        """
        res = self.client().get('/api/v1/red-flags/1')
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 401)

    
    def test_fetching_one_red_flag(self):
        """Test whether the API can fetch one red flag"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences))
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/red-flags/1', headers=self.get_authentication_headers(access_token))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(200, response_msg["status"])
        self.assertEqual(IncidenceModel.get_incidence_by_id(1), response_msg["data"][0])
   
    def test_unauthorized_user_cannot_delete_a_red_flag(self):
        """Test the API cannot deletion of a red flag without authorization"""
        res = self.client().delete('/api/v1/red-flags/1')
        self.assertEqual(res.status_code, 401)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Missing Authorization Header", response_msg['msg'])

    def test_delete_one_red_flag(self):
        """Test whether the API can delete a red flag"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences)) # Create a red-flag
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/red-flags/1', 
            headers=self.get_authentication_headers(access_token)) # Delete the created red-flag
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag record has been deleted", response_msg["data"][0]["message"])
        res = self.client().get('/api/v1/red-flags/1', 
            headers=self.get_authentication_headers(access_token)) # Try accessing the deleted red flag
        self.assertEqual(res.status_code, 404)

    def test_unauthorized_edit_of_a_red_flag_location(self):
        """Test the API cannot edit a red flag location without authorization"""
        res = self.client().put(
            'api/v1/red-flags/1/location', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(
                {
                    "location": "5S10E"
                }
            )
        )
        self.assertEqual(res.status_code, 401)

    
    def test_edit_red_flag_location(self):
        """Test whether the API can edit a red flag location"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences)) # Create a red-flag
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/red-flags/1/location', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "location": "5S10E"
                }
            )
        )
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Updated red-flag record’s location", response_msg["data"][0]["message"])
        res = self.client().get('/api/v1/red-flags/1', 
            headers=self.get_authentication_headers(access_token))
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("5S10E", response_msg["data"][0]["location"])

    def test_unauthorized_edit_of_a_red_flag_comment(self):
        """
        Test the API doesn't allowed unauthorized 
        editing of a red flag comment
        """
        res = self.client().put(
            '/api/v1/red-flags/1/comment',
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(
                {
                    "comment": "RED FLAG COMMENT UPDATE"
                }
            )
        )
        self.assertEqual(res.status_code, 401)

    
    def test_edit_red_flag_comment(self):
        """Test whether the API can edit a red flag comment"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences)) # Create a red-flag
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/red-flags/1/comment', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                     "comment": "RED FLAG COMMENT UPDATE"
                }
            )
        )
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Updated red-flag record’s comment", response_msg["data"][0]["message"])
        res = self.client().get('/api/v1/red-flags/1', headers=self.get_authentication_headers(access_token))
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("RED FLAG COMMENT UPDATE", response_msg["data"][0]["comment"])

    def test_unauthorized_edit_of_a_red_flag_status(self):
        """Test the API doesn't allow an unauthorized edit of a red flag"""
        res = self.client().put(
            '/api/v1/red-flags/1/status', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(
                {
                    "status": "UNRESOLVED"
                }
            )
        )
        self.assertEqual(res.status_code, 401)

    def test_edit_red_flag_status(self):
        """Test the API can edit a red flag status"""
        # Regular user registration
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user)
        )
        self.assertEqual(res.status_code, 201)

        # Regular user login
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login)
        )
        self.assertEqual(res.status_code, 200)

        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token'] # Get access token for the regular user to create a red flag

        # Regular user creates a post 
        res = self.client().post("/api/v1/red-flags", 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences))
        self.assertEqual(res.status_code, 201)

        # Administrator registration
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user)
        )
        self.assertEqual(res.status_code, 201)

         # Administrator login
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user_login)
        )
        self.assertEqual(res.status_code, 200)

        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token'] # Adminstrator's access token

        # Adminstrator changes the red flag status
        res = self.client().put(
            "/api/v1/red-flags/1/status", 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "status": "RESOLVED"
                }
            )
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Updated red-flag record's status", response_msg["data"][0]["message"])
        res = self.client().get('/api/v1/red-flags/1', headers=self.get_authentication_headers(access_token))
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("RESOLVED", response_msg["data"][0]["status"])
    
    def test_non_integer_id_not_allowed(self):
        """Test the API doesn't allow non integer values"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().post('/api/v1/red-flags', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(self.incidences))
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/red-flags/i', 
            headers=self.get_authentication_headers(access_token)) # Try fetching a red flag with wrong ID type
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag id must be an Integer", response_msg["message"])
        self.assertEqual(res.status_code, 400)
        res = self.client().delete('/api/v1/red-flags/a', 
            headers=self.get_authentication_headers(access_token)) # Try deleting a red flag with wrong ID type
        self.assertEqual(res.status_code, 400)
        res = self.client().put(
            '/api/v1/red-flags/1a/location', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "location": "5S10E"
                }
            )
        ) # Try updating a red flag location with wrong ID type
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag id must be an Integer", response_msg["message"])
        self.assertEqual(res.status_code, 400)
        res = self.client().put(
            '/api/v1/red-flags/x/comment', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "comment": "Error in comment"
                }
            )
        ) # Try updating a red flag comment with wrong ID type
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag id must be an Integer", response_msg["message"])
        self.assertEqual(res.status_code, 400)

        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().put(
            'api/v1/red-flags/e/status',
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "status": "REJECTED"
                }
            )
        )
        self.assertEqual(res.status_code, 400) 

    def test_an_empty_list_cannot_be_modified(self):
        """Test that the API cannot allow empty lists to be modified"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().get('/api/v1/red-flags/1', 
            headers=self.get_authentication_headers(access_token)) # Fetch a non-existent red flag record
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red flag with id 1 doesn't exist", response_msg["message"])
        self.assertEqual(res.status_code, 404)
        res = self.client().delete('/api/v1/red-flags/2', 
            headers=self.get_authentication_headers(access_token)) # Delete a non-existent red flag record
        self.assertEqual(res.status_code, 404)
        res = self.client().put(
            'api/v1/red-flags/3/location', 
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "location": "5S10E"
                }
            )
        ) # Edit the location of a non-existent red flag record
        self.assertEqual(res.status_code, 404)   
        res = self.client().put(
            'api/v1/red-flags/4/comment',
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "comment": "RED FLAG COMMENT UPDATE"
                }
            )
        )
        self.assertEqual(res.status_code, 404)

        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.admin_user_login))
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg['access_token']
        res = self.client().put(
            'api/v1/red-flags/5/status',
            headers=self.get_authentication_headers(access_token), 
            data=json.dumps(
                {
                    "status": "UNDER INVESTIGATION"
                }
            )
        )
        self.assertEqual(res.status_code, 404) 

    def tearDown(self):
        del INCIDENCES[:]
        del USERS[:]

class UserTestCase(unittest.TestCase):
    """This class represents the User test case"""
    def setUp(self):
        """Define the test variables and initialize the application"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
       
        self.regular_user = {
            "firstname": "john",
            "lastname": "doe",
            "othernames": "foo",
            "email": "joe@test.com",
            "phoneNumber": "0700000000",
            "username": "jondo",
            "isAdmin": False,
            "password": "12345"
        }

        self.regular_user_login = {
            "username": "jondo",
            "password": "12345"
        }

        # Provide a user with a wrong password
        self.wrong_user_password = {
            "username": "jondo",
            "password": "wrong_password"
        }
    
    def get_accept_content_type_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_user_regisration(self):
        """Test whether the API can register a user"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(201, response_msg["status"])
        self.assertEqual("Create user record", response_msg["data"][0]["message"])

    
    def test_user_cannot_login_before_registration(self):
        """Test the API cannot login a user before signing up"""
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("User with username 'jondo' doesn't exist!", response_msg["message"])

    def test_user_can_login_after_registration(self):
        """Test the API can login a user after signing up"""
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user_login))
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Logged in as jondo", response_msg["message"])
    
    def test_user_cannot_login_with_wrong_password(self):
        res = self.client().post('/auth/register', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.regular_user))
        res = self.client().post('/auth/login', 
            headers=self.get_accept_content_type_headers(), 
            data=json.dumps(self.wrong_user_password))
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Wrong credentials", response_msg["message"])
    
    def tearDown(self):
        del USERS[:]

if __name__ == "__main__":
    unittest.main()