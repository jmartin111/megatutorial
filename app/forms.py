#! .venv/bin/python

from flask import flash
import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app import blog, db
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
        )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError(f'Username {username.data} exists. Select something else')
        

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User.email).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(f'Email {email.data} exists. Select comething else')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, current_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_username = current_username

    def validate_username(self, username):
        if username.data != self.current_username:
            user = db.session.scalar(sa.select(User).where(
                                     User.username == username.data))
            if user is not None:
                blog.logger.info('A user tried to change their uname to an existing user')
                # flash(f"Username [{user.username}] exists. Select something else")
                raise ValueError(f"Username [{user.username}] exists. Select something else")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
