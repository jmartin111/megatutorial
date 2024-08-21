#! .venv/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import BlogConfig

# define and config the app
blog = Flask(__name__)
blog.config.from_object(BlogConfig)

# register extensions
db = SQLAlchemy(blog)
migrate = Migrate(blog, db)
login = LoginManager(blog)

# import here to avoid circular dependencies
from app import routes, models
