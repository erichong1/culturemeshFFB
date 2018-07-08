from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

class NetworkJoinForm(FlaskForm):
    submit = SubmitField('Join Network')

class CreatePostForm(FlaskForm):
    post_content = StringField(
      'post_content', validators=[
        InputRequired(message="Post cannot be empty."),
      ],
      widget=TextArea(),
      render_kw={'autofocus': True}
    )
    submit = SubmitField('Create Post')

class CreateEventForm(FlaskForm):
    submit = SubmitField('Join Network')

