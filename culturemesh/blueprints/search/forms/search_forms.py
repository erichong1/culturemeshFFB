from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_type = SelectField(
        'Search Type',
        choices=[('language', 'speak'), ('location', 'are from')]
    )
    origin_or_language = StringField(
        'origin/language', validators=[DataRequired()]
    )
    residence = StringField(
        'current_location', validators=[DataRequired()]
    )
    submit = SubmitField('Search')
