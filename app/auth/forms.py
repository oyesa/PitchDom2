from flask_wtf import FlaskForm
from ..models import User
from wtforms.validators import DataRequired,Email,EqualTo,Length
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError



class SignUpForm(FlaskForm):
    email = StringField('Enter Email Address',validators=[DataRequired(),Email()])
    username = StringField('Enter Username',validators = [DataRequired(),Length(min=2,max=20)])
    password = PasswordField('Password',validators = [DataRequired()])
    password_confirm = PasswordField('Confirm Password',validators = [DataRequired(), EqualTo('password',message = 'Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('An account already exists with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('Username is taken')

class LoginForm(FlaskForm):
    email = StringField('Enter Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators =[DataRequired()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Sign In')