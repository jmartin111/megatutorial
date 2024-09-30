#!.venv/bin/python3

import os

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app, db
from app.models import User, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'os': os,
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Post': Post
    }
