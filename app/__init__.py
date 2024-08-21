#! .venv/bin/python3

from flask import Flask
from config import BlogConfig

blog = Flask(__name__)
blog.config.from_object(BlogConfig)

from app import routes
