from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    origin_or_language = StringField('origin/language', validators=[])
    residence = StringField('and live in', validators=[DataRequired()])
    submit = SubmitField('Search Networks')
