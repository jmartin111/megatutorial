#! .venv/bin/python

from flask import render_template
from app import blog

@blog.route('/')
@blog.route('/index')
def index():
    meta = {
        "username": "jeff",
        "title": "index"
        }
    posts = [
        {
            "author": {"username": "jeff"},
            "title": "one",
            "body": "ipsum delorium, libyans have plutonium!!"
        },
        {
            "author": {"username": "some fool"},
            "title": "two",
            "body": "jesus saves your everlasting soul"
        },
        {
            "author": {"username": "jeff"},
            "title": "three",
            "body": "no he does not because that is just silly"
        },
    ]
    return render_template("index.html",
                           title=meta["title"],
                           user=meta["username"], 
                           posts=posts)
