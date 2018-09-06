from flask_wtf import FlaskForm
from wtforms import SubmitField

class EventJoinForm(FlaskForm):
    submit = SubmitField('Sign Up')

class EventLeaveForm(FlaskForm):
    submit = SubmitField('Leave Event')

class EventCancelForm(FlaskForm):
    submit = SubmitField('Cancel Event')

class EventCancelConfirmForm(FlaskForm):
    submit = SubmitField('Yes, Cancel Event')
