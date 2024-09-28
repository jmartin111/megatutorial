#! .venv/bin/python

from flask_babel import _,  lazy_gettext as _l

import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app import db
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password_confirm = PasswordField(
        _l('Confirm Password'), validators=[DataRequired(),
                                        EqualTo('password', message='Password fields must match')])
    submit = SubmitField(_l('Register'), render_kw={'class': 'btn btn-outline-success'})

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError(
                _('Username %(username)s exists. Select something else', username=username.data))
        

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User.email).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(
                _('Email %(email)s exists. Select comething else', email=email.data))

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'), render_kw={'class': 'btn btn-outline-success'})

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'), render_kw={'class': 'btn btn-outline-success'})

class FollowForm(FlaskForm):
    submit = SubmitField(_l('Follow'), render_kw={'class': 'btn btn-outline-success'})

class PostForm(FlaskForm):
    post = TextAreaField('', validators=[DataRequired(), Length(min=1, max=140)],
                         render_kw={
                             'style': 'background-color: rgb(63 83 180);'
                             'border-radius: 10px;'
                             'padding: 7px;'
                             'resize: none;',
                             'placeholder': 'Make your mark ...'
                        })
    submit = SubmitField(_l('Post'), render_kw={'class': 'btn btn-outline-success'})
