from flask import Blueprint, render_template, request
from culturemesh.client import Client
import flask_login
from flask_login import current_user

posts = Blueprint('posts', __name__, template_folder='templates')

POST_TITLE_MAX_LEN = 10

@posts.route("/")
@flask_login.login_required
def render_post():

  current_post_id = request.args.get('id')
  user_id = current_user.get_id()

  c = Client(mock=False)

  post = c.get_post(current_post_id)
  post_text_arr = post["post_text"].split(" ")

  # Currently, the title of a post is simply the first few words
  title = ' '.join(post_text_arr[:min(len(post_text_arr), POST_TITLE_MAX_LEN)])

  if len(post_text_arr) > POST_TITLE_MAX_LEN:
    title += "..."

  # NOTE: this only fetches a single post reply
  num_replies = 1
  replies = c.get_post_replies(post["id"], num_replies)

  usernames = []
  for reply in replies:
      username = c.get_user(reply["id_user"])["username"]
      usernames.append(username)

  return render_template('post.html', title=title,
    post=post, replies=replies,
    reply_usernames=usernames, num_replies=len(replies))

@posts.route("/ping")
@flask_login.login_required
def ping():
  c = Client(mock=False)
  return c.ping_post()
