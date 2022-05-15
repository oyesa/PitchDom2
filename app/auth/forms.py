from flask_wtf import FlaskForm
from ..models import User
from wtforms.validators import DataRequired,Email,EqualTo,Length
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError

