#! .venv/bin/python

import os

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import blog, db
from app.models import User, Post

@blog.shell_context_processor
def make_shell_context():
    return {
        'os': os,
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Post': Post
    }
