#! .venv/bin/python

import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__name__), 'instance'))

class BlogConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                            f"sqlite:///{os.path.join(basedir, 'blog.db')}"