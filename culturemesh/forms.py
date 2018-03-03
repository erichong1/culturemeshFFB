from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class LoginForm(FlaskForm):
    user_id = StringField('User ID', validators=[])
    submit = SubmitField('Login')