from flask_wtf import FlaskForm 
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import DataRequired


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Something about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    title = StringField("Pitch Title", validators = [DataRequired()])
    category = SelectField("Choice of category to submit to?", choices=[("Fashion", "Fashion Pitches"), ( "Elevator", "Elevator Pitches"), ("Architecture", "Architecturial Pitches"), ("Investor", "Investor Pitches")],validators=[DataRequired()])
    pitch_content = TextAreaField('The Pitch (Impress us)',validators = [DataRequired()] )
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Add a comment',validators = [DataRequired()] )
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    category_name = TextAreaField('Add a category', validators=[DataRequired()])
    submit = SubmitField('Submit')