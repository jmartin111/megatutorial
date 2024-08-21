#! .venv/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import BlogConfig

blog = Flask(__name__)
blog.config.from_object(BlogConfig)

db= SQLAlchemy(blog)
migrate = Migrate(blog, db)

blog.logger.debug(f"DATABASE: {blog.config['SQLALCHEMY_DATABASE_URI']}")

from app import routes, models
