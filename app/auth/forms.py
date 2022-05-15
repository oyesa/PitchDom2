from flask_wtf import FlaskForm
from ..models import User
from wtforms.validators import DataRequired,Email,EqualTo,Length
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError



class LoginForm(FlaskForm):
    """
    This class defines the login form
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 50), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """
     This classd efines the registration form
    """
    name = StringField('Name', validators=[DataRequired(), Length(1, 50)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 50), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def check_email_exist(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. Please Login')

    def check_username_exist(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')