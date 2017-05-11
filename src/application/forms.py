# forms.py
#
"""
Web forms based on Flask-WTForms
See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/
"""

from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired


class EmailForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])

