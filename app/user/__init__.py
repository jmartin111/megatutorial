#!.venv/bin/python3

from flask import Blueprint

bp = Blueprint('user', template_folder='templates')

from app.user import routes
