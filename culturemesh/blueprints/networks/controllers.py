import flask_login
import utils

from flask import Blueprint, render_template, request
from culturemesh.client import Client
from culturemesh.constants import LANGUAGE_NETWORK

networks = Blueprint('networks', __name__, template_folder='templates')

@networks.route("/")
@flask_login.login_required
def network():
  id_network = request.args.get('id')
  if not id_network:
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

  posts = c.get_network_posts(id_network, 3)
  events = c.get_network_events(id_network, 3)
  for event in events:
    utils.enhance_event_date_info(event)

  for post in posts:
    post['username'] = c.get_user(post['id_user'])['username']
    post['reply_count'] = c.get_post_reply_count(post['id'])['reply_count']

  # TODO: This assumes that the region ID and city ID are specified in the data.
  # This is not necessarily the case. This needs to be changed using the new information
  # that Ian sent us about network classes.

  network_info = {}
  network_info['id'] = id_network
  network_info['posts'] = posts
  network_info['events'] = events
  cur_country = network['country_cur']
  cur_region = network['region_cur']
  cur_city = network['city_cur']
  network_info['network_title'] = get_network_title(network)

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  return render_template('network.html', network_info=network_info)

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

  # TODO: This assumes that the region ID and city ID are specified in the data.
  # This is not necessarily the case. This needs to be changed using the new information
  # that Ian sent us about network classes.

  network_info = {}
  network_info['id'] = id_network
  network_info['events'] = events
  cur_country = network['country_cur']
  cur_region = network['region_cur']
  cur_city = network['city_cur']
  network_info['network_title'] = get_network_title(network)

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  return render_template('network_events.html', network_info=network_info, event_index=event_index)

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

  # TODO: Add better handling for when there's no events left.

  if not posts :
    post_index = old_index
  else :
    post_index = posts[-1]['id']

  # TODO: This assumes that the region ID and city ID are specified in the data.
  # This is not necessarily the case. This needs to be changed using the new information
  # that Ian sent us about network classes.

  network_info = {}
  network_info['id'] = id_network
  network_info['posts'] = posts
  cur_country = network['country_cur']
  cur_region = network['region_cur']
  cur_city = network['city_cur']

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  network_info['network_title'] = get_network_title(network)
  return render_template('network_posts.html', network_info=network_info, post_index=post_index)

@networks.route("/ping")
@flask_login.login_required
def ping():
    c = Client(mock=False)
    return c.ping_network()

def get_network_title(network):
  cur_country = network['country_cur']
  cur_region = network['region_cur']
  cur_city = network['city_cur']

  if network['network_class'] == 0:
    language = network['language_origin']
    return "%s speakers in %s, %s, %s" \
      % tuple([language, cur_city, cur_region, cur_country])
  else:
    orig_country = network['country_origin']
    orig_region = network['region_origin']
    orig_city = network['city_origin']
    return 'From %s, %s, %s in %s, %s, %s' % tuple([orig_city,
      orig_region, orig_country, cur_city, cur_region, cur_country])
