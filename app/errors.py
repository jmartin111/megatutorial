#! .venv/bin/bash

from flask import render_template, session
from app import blog, db

@blog.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@blog.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500