#! .venv/bin/python3

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import json
import os

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import BlogConfig, DevBlogConfig

# define and config the app
blog = Flask(__name__)
blog.config.from_object(BlogConfig)

# register extensions
db = SQLAlchemy(blog)
migrate = Migrate(blog, db)
loginmgr = LoginManager(blog)
loginmgr.login_view = 'login'

if not blog.debug:
    # mail server config
    if blog.config['MAIL_SERVER']:
        auth = None
        if blog.config['MAIL_USERNAME'] or blog.config['MAIL_PASSWORD']:
            auth = (['MAIL_USERNAME'], blog.config['MAIL_PASSWORD'])
        secure = None
        if blog.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(blog.config['MAIL_SERVER'], blog.config['MAIL_PORT']),
            fromaddr=f'no-reply@ {blog.config['MAIL_SERVER']}',
            toaddrs=blog.config['MAIL_ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        blog.logger.addHandler(mail_handler)

    # log file config
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', 'w',
                                       maxBytes=1024*1024, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    blog.logger.addHandler(file_handler)

    blog.logger.setLevel(logging.INFO)
    blog.logger.info('Microblog Starting ...')
    
    # dump app config
    config_dict = {key: value for key, value in blog.config.items()}
    blog.logger.info(f"App Config: {config_dict}")

# import here to avoid circular dependencies
from app import routes, models, errors
