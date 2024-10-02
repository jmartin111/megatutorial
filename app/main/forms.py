#!.venv/bin/python3

from flask_babel import _,  lazy_gettext as _l

import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

from app import db
from app.models import User

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

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
