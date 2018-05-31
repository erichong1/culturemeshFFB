from flask import Blueprint, render_template, request
from culturemesh.client import Client
import flask_login
from flask_login import current_user

events = Blueprint('events', __name__, template_folder='templates')

@events.route("/")
@flask_login.login_required
def render_events():
    current_event_id = request.args.get('id')
    c = Client(mock=True)
    fake_event = c.get_event(current_event_id)
    return render_template('event.html', event=fake_event)
