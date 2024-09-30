#!.venv/bin/python3

import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__name__), 'instance'))

class BlogConfig:
    # main
    SECRET_KEY = os.environ.get('SECRET_KEY')
    G_API_KEY = os.environ.get('G_API_KEY')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    
    # mail - not really used
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ADMINS = os.environ.get('MAIL_ADMINS')
    
    # user posts
    POSTS_PER_PAGE = 3  # max amount for most dense pages

    # babel
    LANGUAGES = ['en', 'es', 'de']

class DevBlogConfig(BlogConfig):
    DEBUG_LEVEL = os.environ.get('DEBUG_LEVEL')
