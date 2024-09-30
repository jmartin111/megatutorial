#!.venv/bin/python3

from datetime import timedelta

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import os

from flask import request
from flask_moment import Moment
from flask_babel import Babel, _, lazy_gettext as _l

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import BlogConfig

# this is set to the minumum that will fit on
# the most bloated pages and is adjusted on a per-page basis
POSTS_PER_PAGE = current_app.config['POSTS_PER_PAGE']

# cosmetic only - helper function to keep render_template
# args smaller. passed into templates as a dict
def build_pagination(posts):    
     return {
        'prev_page': posts.prev_num,
        'next_page': posts.next_num,
        'has_prev': posts.has_prev ,
        'has_next': posts.has_next,
        'curr_page': posts.page,
        'num_pages': posts.pages,
    }

# get the client's preferential language
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

### register extensions ###
# db
db = SQLAlchemy()
migrate = Migrate(db)

# login
loginmgr = LoginManager()
loginmgr.login_view = 'auth.login'
loginmgr.login_message = _l('Please login to access this page')

# time and language
moment = Moment()
babel = Babel(locale_selector=get_locale)

def create_app(config_class=BlogConfig):
    # define and config the app
    blog = Flask(__name__)
    blog.config.from_object(BlogConfig)

    db.init_app(blog)
    migrate.init_app(blog)
    loginmgr.init_app(blog)
    moment.init_app(blog)
    babel.init_app(blog)

    # register blueprints
    from app.main import bp as main_bp
    blog.register_blueprint(main_bp, url_prefix='/')

    from app.auth import bp as auth_bp
    blog.register_blueprint(auth_bp, url_prefix='/auth')

    from app.user import bp as user_bp
    blog.register_blueprint(user_bp, url_prefix='/user')

    from app.errors import bp as errors_bp
    blog.register_blueprint(errors_bp)

    if not blog.debug and not blog.testing:
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
        blog.logger.info(_('Microblog Starting ...'))
        
        # dump app config
        config_dict = {key: value for key, value in blog.config.items()}
        blog.logger.info(_("App Config: %(config)s", config=config_dict))

    return blog
    
# import here to avoid circular dependencies
from app import models
