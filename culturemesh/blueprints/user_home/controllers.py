import flask_login
import utils
import datetime

from flask import Blueprint, render_template, request
from culturemesh.client import Client
from culturemesh.utils import get_network_title
from culturemesh.utils import get_user_image_url
from culturemesh.utils import get_short_network_join_date
from culturemesh.utils import get_time_ago
from culturemesh.utils import get_upcoming_events_by_user
from flask_login import current_user
from werkzeug.exceptions import HTTPException
from utils import parse_date

from culturemesh.blueprints.user_home.forms.home_forms import UserInfo

user_home = Blueprint('user_home', __name__, template_folder='templates')

@user_home.route("/")
@user_home.route("/dashboard")
@flask_login.login_required
def render_user_home():
  user_id = current_user.get_id()
 # print(dir(current_user))
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

    post['username'] = c.get_user(post['id_user'])['username']
    post['reply_count'] = c.get_post_reply_count(post['id'])['reply_count']
    post['time_ago'] = get_time_ago(post['post_date'])

    try:
      post['network'] = c.get_network(post['id_network'])
      post['network_title'] = get_network_title(post['network'])
    except HTTPException as e:
      post['network'] = None
      post['network_title'] = "Unknown"

  upcoming_events = get_upcoming_events_by_user(c, user['id'], 3)
  for event in upcoming_events:
    utils.enhance_event_date_info(event)
    event['network_title'] = get_network_title(
      c.get_network(event['id_network'])
    )

  return render_template(
    'dashboard.html',
    user=user,
    events_hosting=events_hosting,
    latest_posts=latest_posts,
    upcoming_events_in_networks=upcoming_events
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

  user_info_form=UserInfo()
  user_info_form.first_name.process_data(user['first_name'])
  user_info_form.last_name.process_data(user['last_name'])
  user_info_form.about_me.process_data(user['about_me'])
  return render_template(
    'account.html', user=user, user_info_form=user_info_form
  )

@user_home.route("/update_profile", methods=['POST'])
@flask_login.login_required
def update_profile_and_render_home():
  user_id = current_user.get_id()
  c = Client(mock=False)

  data = request.form
  form = UserInfo(request.form)
  first_name = data['first_name']
  last_name = data['last_name']
  about_me = data['about_me']

  user = {
    'id': user_id, 'first_name': first_name,
    'last_name': last_name, 'about_me': about_me
  }

  if form.validate():
    c.update_user(user)

  user = c.get_user(user_id)
  if user is None:
    return page_not_found("")
  user['img_url'] = get_user_image_url(user)

  user_info_form=UserInfo()
  user_info_form.first_name.process_data(user['first_name'])
  user_info_form.last_name.process_data(user['last_name'])
  user_info_form.about_me.process_data(user['about_me'])
  return render_template(
    'account.html', user=user, user_info_form=user_info_form
  )

@user_home.route("/events")
@flask_login.login_required
def render_user_home_events():
  user_id = current_user.get_id()
  c = Client(mock=False)
  user = c.get_user(user_id)
  user['img_url'] = get_user_image_url(user)

  if user is None:
    return page_not_found("")

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
