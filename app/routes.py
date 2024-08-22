#! .venv/bin/python

import sqlalchemy as sa

from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import blog, db
from app.forms import LoginForm
from app.models import User

from urllib.parse import urlsplit

@blog.route('/')
@blog.route('/index')
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # get user data from db
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
            )
        if user is None or not user.check_password(form.password.data):
            # falied login
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # user checks out
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='SIgn In', form=form)


@blog.route('/logout')
def logout():
    logout_user()
    return(redirect(url_for('index')))
