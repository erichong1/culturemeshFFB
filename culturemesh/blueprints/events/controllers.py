from flask import Blueprint, render_template, request, redirect, url_for
from culturemesh.client import Client
from flask_login import current_user
from flask_login import login_required

from utils import enhance_event_date_info

from culturemesh.utils import user_is_attending_event
from culturemesh.utils import get_network_title
from culturemesh.utils import get_event_location

from culturemesh.blueprints.events.forms.event_forms import EventJoinForm
from culturemesh.blueprints.events.forms.event_forms import EventLeaveForm
from culturemesh.blueprints.events.forms.event_forms import EventCancelForm
from culturemesh.blueprints.events.forms.event_forms import EventCancelConfirmForm

from culturemesh.blueprints.networks.utils import gather_network_info

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

    role = None

    if event['id_host'] == current_user.id:

      # The current user is hosting this event.
      role = 'hosting'
      host['username'] = 'you'

    elif user_is_attending_event(c, current_user.id, event):

      # The current user is already signed up for this event.
      role = 'attending'
    else:

      # The current user is not signed up for this event.
      pass

    return render_template(
      'event.html',
      event=event,
      host=host,
      role=role,
      join_form=EventJoinForm(),
      leave_form=EventLeaveForm(),
      cancel_form=EventCancelForm()
    )

@events.route("/join", methods=['POST'])
@login_required
def join_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    c.join_event_as_guest(current_user, current_event_id)
    return redirect(
      url_for('events.render_events', id=current_event_id)
    )

@events.route("/leave", methods=['POST'])
@login_required
def leave_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    c.leave_event(current_user, current_event_id)
    return redirect(
      url_for('events.render_events', id=current_event_id)
    )

@events.route("/cancelconfirm", methods=['POST'])
@login_required
def cancel_event_confirm():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    event = c.get_event(current_event_id)
    network = c.get_network(event['id_network'])
    network_info = gather_network_info(network['id'], current_user.id, c)

    # The current user should only be able to cancel an event if they
    # are the host of that event.
    if not str(current_user.id) == str(event['id_host']):
      return redirect(
        url_for('user_home')
      )

    return render_template(
      'event_cancel.html',
      network_info=network_info,
      event=event,
      form=EventCancelConfirmForm()
    )

@events.route("/cancel", methods=['POST'])
@login_required
def cancel_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    event = c.get_event(current_event_id)

    # The current user should only be able to cancel an event if they
    # are the host of that event.
    if str(current_user.id) == str(event['id_host']):
      c.delete_event(current_user, current_event_id)
    return redirect(url_for('user_home.render_user_home'))
