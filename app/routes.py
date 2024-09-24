#! .venv/bin/python

from crypt import methods
from datetime import datetime, timezone

import sqlalchemy as sa

from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import blog, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, FollowForm
from app.models import User

from .mock_posts import get_posts

from urllib.parse import urlsplit

@blog.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@blog.route('/')
@blog.route('/index')
@login_required
def index():
    # get the current logged in user avatar as a placeholder
    user = db.session.scalar(sa.select(User).where(User.username == current_user.username))
    posts = get_posts(user)

    return render_template('index.html', posts=posts)


@blog.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return(redirect(url_for('index')))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} successfully registered', 'alert-success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


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
            flash('Invalid username or password', 'alert-danger')
            return redirect(url_for('login'))
        # user checks out
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@blog.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = get_posts(user)

    form = FollowForm()
    return render_template('user/user.html', title='Profile', user=user, posts=posts, form=form)


@blog.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'alert-success')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        
    return render_template('user/edit_profile.html', title='Edit Profile', form=form)


@blog.route('/new_post', methods=['GET', 'POST'])
def new_post():
    return(render_template('user/new_post.html'))

@blog.route('/follow/<username>/', methods=['POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit:
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found!' 'alert-warning')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself, you halibut', 'alert-warning')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}', 'alert-success')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    

@blog.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit:
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found' 'alert-warning')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!' 'alert-warning')
            return redirect(url_for('user', username==username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.', 'alert-success')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@blog.route('/logout')
def logout():
    logout_user()
    return(redirect(url_for('index')))
