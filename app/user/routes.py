#!.venv/bin/python3

from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required
from flask_babel import _

import sqlalchemy as sa

from app import db, build_pagination, POSTS_PER_PAGE
from app.user import bp
from app.user.forms import EditProfileForm, FollowForm

from app.models import User, Post 

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = db.paginate(sa.select(Post).where(Post.author == user).order_by(Post.timestamp.desc()),
                        page=1, per_page=POSTS_PER_PAGE, error_out=False)
    
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).where(Post.author == user).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=POSTS_PER_PAGE, error_out=False)

    form = FollowForm()

    pg_object = build_pagination(posts)

    return render_template('user/user.html', title='Profile', 
                           user=user, posts=posts, form=form, pg=pg_object)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'), 'alert-success')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        
    return render_template('user/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>/', methods=['POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit:
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(_('User %(user)s not found!', user=username), 'alert-warning')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself, you halibut'), 'alert-warning')
            return redirect(url_for('user.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(user)s', user=username), 'alert-success')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('main.index'))
    

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit:
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(_('User %(user)s not found!', user=username), 'alert-warning')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!'), 'alert-warning')
            return redirect(url_for('user.user', username==username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are no longer following %(user)s.', user=username), 'alert-success')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('main.index'))