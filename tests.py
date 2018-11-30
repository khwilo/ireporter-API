import unittest
import os 
import json

from app import create_app
from app.api.v1.models.incidence import IncidenceModel

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
            "location":  "12NE"
        }
    
    def test_red_flag_creation(self):
        """Test whether the API can create a red flag"""
        res = self.client().post('/red-flags', data=self.incidences)
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(201, response_msg["status"])
        self.assertEqual("Create red-flag record", response_msg["data"][0]["message"])

    def test_fetching_all_red_flags(self):
        """Test whether the API can fetch all red flags"""
        res = self.client().post('/red-flags', data=self.incidences)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/red-flags')
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(200, response_msg["status"])
        self.assertEqual(IncidenceModel.get_all_incidences(), response_msg["data"])

    def test_fetching_one_red_flag(self):
        """Test whether the API can fetch one red flag"""
        res = self.client().post('/red-flags', data=self.incidences)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/red-flags/1')
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(200, response_msg["status"])
        self.assertEqual(IncidenceModel.get_incidence_by_id(1), response_msg["data"][0])
        res = self.client().get('/red-flags/1-')
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag id must be an Integer", response_msg["message"])
        self.assertEqual(res.status_code, 400)

    def test_delete_one_red_flag(self):
        """Test whether the API can delete a red flag"""
        res = self.client().post('/red-flags', data=self.incidences) # Create a red-flag
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/red-flags/1') # Delete the created red-flag
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag record has been deleted", response_msg["data"][0]["message"])
        res = self.client().get('/red-flags/1')
        self.assertEqual(res.status_code, 404)
        res = self.client().delete('/red-flags/2') # Test deletion of non-existent red flag record
        self.assertEqual(res.status_code, 404)
        res = self.client().delete('/red-flags/a')
        self.assertEqual(res.status_code, 400) # Test that only integer ids are allowed

    def test_edit_red_flag_location(self):
        """Test whether the API can edit a red flag location"""
        res = self.client().post('/red-flags', data=self.incidences) # Create a red-flag
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/red-flags/1/location',
            data = {
                "location": "5S10E"
            }
        )
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Updated red-flag record’s location", response_msg["data"][0]["message"])
        res = self.client().get('/red-flags/1')
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("5S10E", response_msg["data"][0]["location"])
        res = self.client().put(
            '/red-flags/1a/location',
            data = {
                "location": "5S10E"
            }
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag id must be an Integer", response_msg["message"])
        self.assertEqual(res.status_code, 400)

    def test_edit_red_flag_comment(self):
        """Test whether the API can edit a red flag location"""
        res = self.client().post('/red-flags', data=self.incidences) # Create a red-flag
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/red-flags/1/comment',
            data = {
                "comment": "RED FLAG TEST TWO"
            }
        )
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Updated red-flag record’s comment", response_msg["data"][0]["message"])
        res = self.client().get('/red-flags/1')
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("RED FLAG TEST TWO", response_msg["data"][0]["comment"])
        res = self.client().put(
            '/red-flags/x/comment',
            data = {
                "comment": "Error in comment"
            }
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("red-flag id must be an Integer", response_msg["message"])
        self.assertEqual(res.status_code, 400)

class UserTestCase(unittest.TestCase):
    """This class represents the User test case"""
    def setUp(self):
        """Define the test variables and initialize the application"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        true = True # specify value for isAdmin
        self.users = {
            "firstname": "john",
            "lastname": "doe",
            "othernames": "foo",
            "email": "joe@test.com",
            "phoneNumber": "0700000000",
            "username": "jondo",
            "isAdmin": true,
            "password": "12345"
        }
    
    def test_user_regisration(self):
        """Test whether the API can register a user"""
        res = self.client().post('/register', data=self.users)
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(201, response_msg["status"])
        self.assertEqual("Create user record", response_msg["data"][0]["message"])

if __name__ == "__main__":
    unittest.main()