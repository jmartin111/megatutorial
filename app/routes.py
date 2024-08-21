#! .venv/bin/python

import math
from flask import render_template, flash, redirect, url_for
from app import blog
from app.forms import LoginForm

@blog.route('/')
@blog.route('/index')
def index():
    meta = {
        'username': 'jeff',
        'title': 'index'
        }
    posts = [
        {
            'author': {'username': 'jeff'},
            'title': 'one',
            'body': 'ipsum delorium, libyans have plutonium!!'
        },
        {
            'author': {'username': 'some fool'},
            'title': 'two',
            'body': 'jesus saves your everlasting soul'
        },
        {
            'author': {'username': 'jeff'},
            'title': 'three',
            'body': 'no he does not because that is just silly'
        },
    ]
    return render_template('index.html',
                           title=meta['title'],
                           user=meta['username'], 
                           posts=posts)


@blog.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login required for {form.username.data}, '
                      f'remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='SIgn In', form=form)