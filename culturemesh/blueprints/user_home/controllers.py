import flask_login
import utils
import sys

from flask import Blueprint, render_template
from culturemesh.client import Client
from culturemesh.utils import get_network_title
from culturemesh.utils import get_user_image_url
from culturemesh.utils import get_short_network_join_date
from culturemesh.utils import get_time_ago
from flask_login import current_user
from werkzeug.exceptions import HTTPException

user_home = Blueprint('user_home', __name__, template_folder='templates')

@user_home.route("/")
@user_home.route("/dashboard")
@flask_login.login_required
def render_user_home():
  user_id = current_user.get_id()
  c = Client(mock=False)
  user = c.get_user(user_id)
  user['img_url'] = get_user_image_url(user)
  events_hosting = c.get_user_events(user_id, "hosting", 5)
  if user is None:
    return page_not_found("")

  for event in events_hosting:
    utils.enhance_event_date_info(event)

  latest_posts = c.get_user_posts(user_id, 3)

  for post in latest_posts:
    print(post)
    post['username'] = c.get_user(post['id_user'])['username']
    post['reply_count'] = c.get_post_reply_count(post['id'])['reply_count']
    post['time_ago'] = get_time_ago(post['post_date'])

    try:
      post['network'] = c.get_network(post['id_network'])
      post['network_title'] = get_network_title(post['network'])
    except HTTPException as e:
      post['network'] = None
      post['network_title'] = "Unknown"

  return render_template(
    'dashboard.html',
    user=user,
    events_hosting=events_hosting,
    latest_posts=latest_posts
  )

@user_home.route("/account")
@flask_login.login_required
def render_user_home_account():
  user_id = current_user.get_id()
  c = Client(mock=False)
  user = c.get_user(user_id)
  user['img_url'] = get_user_image_url(user)

  if user is None:
    return page_not_found("")
  return render_template('account.html', user=user)

@user_home.route("/events")
@flask_login.login_required
def render_user_home_events():
  user_id = current_user.get_id()
  c = Client(mock=False)
  user = c.get_user(user_id)
  user['img_url'] = get_user_image_url(user)

  if user is None:
    return page_not_found("")

  # TODO: incorporate paging into the events hosting API call
  events_hosting = c.get_user_events(user_id, "hosting", 5)
  if events_hosting is None:
    return page_not_found("")

  for event in events_hosting:
    utils.enhance_event_date_info(event)

  return render_template('events.html', user=user,
    events_hosting=events_hosting)

@user_home.route("/networks")
@flask_login.login_required
def render_user_home_networks():
  user_id = current_user.get_id()
  c = Client(mock=False)
  user = c.get_user(user_id)
  user['img_url'] = get_user_image_url(user)

  if user is None:
    return page_not_found("")

  # TODO: incorporate paging into the user networks call.
  user_networks = c.get_user_networks(user_id, count=50)

  networks = []
  for network in user_networks:
    network_ = {'id': network['id']}
    network_['title'] = get_network_title(network)
    network_['join_date'] = get_short_network_join_date(network)
    num_users = c.get_network_user_count(network['id'])['user_count']
    network_['user_count'] = num_users
    networks.append(network_)

  return render_template('networks.html', user=user, networks=networks)

@user_home.route("/ping")
@flask_login.login_required
def ping():
  c = Client(mock=False)
  return c.ping_user()
