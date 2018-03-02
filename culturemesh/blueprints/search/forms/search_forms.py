from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    origin = StringField('From', validators=[])
    language = StringField('Or speaking', validators=[])
    residence = StringField('And living in', validators=[DataRequired()])
    submit = SubmitField('Search Networks')