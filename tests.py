import unittest
import os 
import json

from app import create_app
from app.api.v1.models.models import IncidenceModel

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


if __name__ == "__main__":
    unittest.main()