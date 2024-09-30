#!.venv/bin/python3

# sets up a temporary DB in RAM
import os
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

# 'unused' imports passed down to the various test_ files
from datetime import datetime, timezone, timedelta
import unittest
from app import create_app, db
from app.models import *


# errors
from app.errors.handlers import not_found_error as e404
from app.errors.handlers import server_error as e500


from config import BlogConfig

class TestConfig(BlogConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

def setup_test_environment(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    return self.app_context


def teardown_test_environment(app_context):
    db.session.remove()
    db.drop_all()
    app_context.pop()