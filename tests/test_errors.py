#!.venv/bin/python3

from flask import request
import requests
from . import *
from app import blog

from requests_mock import Mocker

class ErrorsTest(unittest.TestCase):
   
    def setUp(self):
        self.app_context = setup_test_environment()
        self.client = blog.test_client()  # Create a test client

    def tearDown(self):
        teardown_test_environment(self.app_context)

    def test_404(self):
        response = self.client.get('/nothing-here.com')
        self.assertEqual(response.status_code, 404)

    def test_405(self):
        response = self.client.post()
        self.assertEqual(response.status_code, 405)

    def test_500(self):
        with Mocker() as mocker:
            mocker.get('https://example.com/api', status_code=500)
            response = requests.get('https://example.com/api')
            self.assertEqual(response.status_code, 500)
                                