from flask import Blueprint, render_template, request
from culturemesh.client import Client
from flask_login import current_user
from flask_login import login_required
from culturemesh.utils import get_network_title
from culturemesh.utils import get_event_location
from utils import enhance_event_date_info

events = Blueprint('events', __name__, template_folder='templates')

@events.route("/ping")
@login_required
def ping():
  c = Client(mock=False)
  return c.ping_event()

@events.route("/")
@login_required
def render_events():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    event = c.get_event(current_event_id)
    date_info = {}
    enhance_event_date_info(event)

    network = c.get_network(event['id_network'])
    event['network_title'] = get_network_title(network)
    event['location'] = get_event_location(event)
    host = c.get_user(event['id_host'])
    return render_template(
      'event.html', event=event, host=host
    )
