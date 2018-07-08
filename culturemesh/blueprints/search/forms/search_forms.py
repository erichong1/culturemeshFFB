from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    origin_or_language = StringField('origin/language', validators=[])
    residence = StringField('current_location', validators=[DataRequired()])
    submit = SubmitField('Search')
