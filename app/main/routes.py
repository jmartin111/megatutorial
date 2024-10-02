#!.venv/bin/python3

from datetime import datetime, timezone
from langdetect import detect, LangDetectException
import sqlalchemy as sa

from flask_babel import _

from flask import current_app, render_template, flash, redirect, request, url_for, g
from flask_login import current_user, login_required

from app.main import bp
from app.models import User

from app import get_posts_per_page, build_pagination, db, get_locale
from app.main.forms import PostForm, EmptyForm
from app.models import Post 
from app.translate import Translate

from urllib.parse import urlsplit

@bp.app_template_filter('username_or_none')
def username_or_none(user):
    return user.username if user else None

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
            current_app.logger.debug('Post language not detected')
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post has been submitted'), 'alert-success')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page, per_page=get_posts_per_page(), error_out=False)
    
    # build pagination - << Page N of N >> looking thing
    pg_object = build_pagination(posts)
    
    return render_template('index.html', title='Home', posts=posts.items, form=form, pg=pg_object)


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post has been submitted'), 'alert-success')
        return redirect(url_for('user.user', username=current_user.username))
    
    return render_template('new_post.html', title='New Post', form=form)
    

@bp.route('/explore', methods=['GET'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=get_posts_per_page()+2, error_out=False)

    # build pagination - << Page N of N >> looking thing
    pg_object = build_pagination(posts)

    return render_template('explore.html', title='Explore', posts=posts.items, pg=pg_object)

@bp.route('/translate', methods=['POST'])
@login_required
def translate():
    data = request.get_json()
    return {'text': Translate(data['phrase'],
                              data['target_lang']
                              ).http_translate()}



@bp.route('user/<username>/popup')
@login_required
def user_popup(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)
