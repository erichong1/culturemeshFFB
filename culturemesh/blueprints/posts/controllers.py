
from flask import Blueprint, render_template, request
from flask_login import current_user
from culturemesh.client import Client
from culturemesh.utils import get_time_ago
from culturemesh.utils import get_network_title

import flask_login

posts = Blueprint('posts', __name__, template_folder='templates')

POST_TITLE_MAX_LEN = 10
NUM_REPLIES_TO_SHOW = 100

@posts.route("/")
@flask_login.login_required
def render_post():

  current_post_id = request.args.get('id')
  user_id = current_user.get_id()

  c = Client(mock=False)

  post = c.get_post(current_post_id)
  post_text_arr = post["post_text"].split(" ")

  post['network_title'] = get_network_title(c.get_network(post['id_network']))
  post['username'] = c.get_user(post["id_user"])["username"]
  post['time_ago'] = get_time_ago(post['post_date'])

  # NOTE: this will not show more than the latest 100 replies
  replies = c.get_post_replies(post["id"], NUM_REPLIES_TO_SHOW)

  for reply in replies:
      reply['username'] = c.get_user(reply["id_user"])["username"]
      reply['time_ago'] = get_time_ago(reply['reply_date'])

  return render_template('post.html', post=post,
    replies=replies, num_replies=len(replies))

@posts.route("/ping")
@flask_login.login_required
def ping():
  c = Client(mock=False)
  return c.ping_post()
