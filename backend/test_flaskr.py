import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        test_config = {
            'SQLALCHEMY_DATABASE_URI': self.database_path,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
            }
        self.app = create_app(test_config)
        self.client = self.app.test_client
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_test(self):
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()