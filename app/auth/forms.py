#!.venv/bin/python3

from flask_babel import _,  lazy_gettext as _l

import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'), render_kw={'class': 'btn btn-outline-success'})

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
        
