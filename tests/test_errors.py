#! .venv/bin/python

from flask import request
from . import *
from app import blog

class ErrorsTest(unittest.TestCase):
   
    def setUp(self):
        self.app_context = setup_test_environment()
        self.client = blog.test_client()  # Create a test client

    def tearDown(self):
        teardown_test_environment(self.app_context)

    def test_404(self):
        response = self.client.get('/nothing-here.com')
        self.assertEqual(response.status_code, 404)

    def test_500(self):
        response = self.client.post()