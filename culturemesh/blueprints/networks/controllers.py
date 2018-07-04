import flask_login
import utils

from flask import Blueprint, render_template, request
from flask_login import current_user
from culturemesh.client import Client
from culturemesh.utils import get_network_title

from culturemesh.blueprints.networks.forms.network_forms import NetworkJoinForm
from culturemesh.blueprints.networks.utils import gather_network_info

networks = Blueprint('networks', __name__, template_folder='templates')

@networks.route("/")
@flask_login.login_required
def network():
  id_network = request.args.get('id')
  c = Client(mock=False)
  id_user = current_user.get_id()
  network_info = gather_network_info(id_network, id_user, c)
  return render_template(
    'network.html', network_info=network_info, form=NetworkJoinForm()
  )

@networks.route("/join", methods=['POST'])
@flask_login.login_required
def join_network():
  id_network = request.args.get('id')
  id_user = current_user.get_id()
  form = NetworkJoinForm(request.form)
  c = Client(mock=False)
  if form.validate():
    c.add_user_to_network(id_user, id_network)

  network_info = gather_network_info(id_network, id_user, c, "join")
  return render_template(
    'network.html', network_info=network_info, form=NetworkJoinForm()
  )

@networks.route("/leave", methods=['POST'])
@flask_login.login_required
def leave_network():
  id_network = request.args.get('id')
  c = Client(mock=False)
  id_user = current_user.get_id()
  network_info = gather_network_info(id_network, id_user, c, "leave")
  return render_template(
    'network.html', network_info=network_info, form=NetworkJoinForm()
  )

@networks.route("/events")
@flask_login.login_required
def network_events() :
  # TODO: A lot of this code is repeated from network(), with just minor variations.
  # This should be factored out.
  id_network = request.args.get('id')
  if not id_network :
    return render_template('404.html')
  c = Client(mock=False)
  try:
    id_network = int(id_network)
  except ValueError:
    return render_template('404.html')
  network = c.get_network(id_network)
  if not network:
    return render_template('404.html')

  # TODO: Get user ID and work out if user is in network.
  # Add join us button to page if they're not.

  events = None

  old_index = request.args.get('index')
  if not old_index:
    events = c.get_network_events(id_network, 10)
  else:
    try:
      old_index = int(old_index)
    except ValueError:
      return render_template('404.html')
    events = c.get_network_events(id_network, 10, old_index - 1)

  # TODO: Add better handling for when there's no posts left.

  if not events :
    event_index = old_index
  else :
    event_index = events[-1]['id']

  for event in events:
    utils.enhance_event_date_info(event)

  id_user = current_user.get_id()
  user_networks = c.get_user_networks(id_user, count=100)
  user_is_member = False
  for network_ in user_networks:
    if int(id_network) == int(network_['id']):
      user_is_member = True
      break

  network_info = {}
  network_info['id'] = id_network
  network_info['events'] = events
  network_info['network_title'] = get_network_title(network)
  network_info['user_is_member'] = user_is_member

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  referrer = request.headers.get("Referer")

  return render_template(
    'network_events.html', network_info=network_info,
    event_index=event_index, referer_url=referrer
  )

@networks.route("/posts")
@flask_login.login_required
def network_posts() :
  # TODO: A lot of this code is repeated from network(), with just minor variations.
  # This should be factored out.
  id_network = request.args.get('id')
  if not id_network :
    return render_template('404.html')
  c = Client(mock=False)
  try:
    id_network = int(id_network)
  except ValueError:
    return render_template('404.html')

  network = c.get_network(id_network)
  if not network:
    return render_template('404.html')

  # TODO: Get user ID and work out if user is in network.
  # Add join us button to page if they're not.

  posts = None

  old_index = request.args.get('index')
  if not old_index:
    posts = c.get_network_posts(id_network, 10)
  else:
    try:
      old_index = int(old_index)
    except ValueError:
      return render_template('404.html')
    posts = c.get_network_posts(id_network, 10, old_index - 1)

  for post in posts:
    post['username'] = c.get_user(post['id_user'])['username']
    post['reply_count'] = c.get_post_reply_count(post['id'])['reply_count']
    post['time_ago'] = get_time_ago(post['post_date'])

  # TODO: Add better handling for when there's no events left.

  if not posts :
    post_index = old_index
  else :
    post_index = posts[-1]['id']

  id_user = current_user.get_id()
  user_networks = c.get_user_networks(id_user, count=100)
  user_is_member = False
  for network_ in user_networks:
    if int(id_network) == int(network_['id']):
      user_is_member = True
      break

  network_info = {}
  network_info['id'] = id_network
  network_info['posts'] = posts
  network_info['user_is_member'] = user_is_member

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  network_info['network_title'] = get_network_title(network)
  return render_template('network_posts.html', network_info=network_info, post_index=post_index)

@networks.route("/posts/new")
@flask_login.login_required
def create_new_post():
    c = Client(mock=False)
    id_network = request.args.get('id')
    user_id = current_user.get_id()
    create_post_url = c.get_create_post_url()

    network = c.get_network(id_network)
    network_title = get_network_title(network)

    return render_template(
      'network_create_post.html',
      curr_user_id=user_id,
      id_network=id_network,
      network_title=network_title,
      create_post_url=create_post_url
    )

@networks.route("/events/new")
@flask_login.login_required
def create_new_event():
    c = Client(mock=False)
    id_network = request.args.get('id')
    user_id = current_user.get_id()
    create_event_url = c.get_create_event_url()
    network = c.get_network(id_network)
    network_title = get_network_title(network)

    return render_template(
      'network_create_event.html',
      curr_user_id=user_id,
      id_network=id_network,
      network_title=network_title,
      create_event_url=create_event_url
    )

@networks.route("/ping")
@flask_login.login_required
def ping():
    c = Client(mock=False)
    return c.ping_network()

