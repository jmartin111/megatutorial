#! .venv/bin/python

# sets up a temporary DB in RAM
import os
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

# 'unused' imports passed down to the various test_ files
from datetime import datetime, timezone, timedelta
import unittest
from app import blog, db
from app.models import *


# errors
from flask import request
from app.errors import not_found_error as e404
from app.errors import server_error as e500

def setup_test_environment():
    blog.config['SECRET_KEY'] = 'o8374p827c4b2ixb74o9nz!@*7p8eodu'
    app_context = blog.app_context()
    app_context.push()
    db.create_all()
    return app_context


def teardown_test_environment(app_context):
    db.session.remove()
    db.drop_all()
    app_context.pop()