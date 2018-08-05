from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from culturemesh.client import Client
from culturemesh.utils import get_time_ago
from culturemesh.utils import get_network_title

from culturemesh.blueprints.posts.forms.post_forms import CreatePostReplyForm

import flask_login

posts = Blueprint('posts', __name__, template_folder='templates')

POST_TITLE_MAX_LEN = 10
NUM_REPLIES_TO_SHOW = 100

@posts.route("/", methods=['GET', 'POST'])
@flask_login.login_required
def render_post():

  current_post_id = request.args.get('id')
  user_id = current_user.id
  c = Client(mock=False)
  post = c.get_post(current_post_id)

  post['network_title'] = get_network_title(c.get_network(post['id_network']))
  post['username'] = c.get_user(post["id_user"])["username"]
  post['time_ago'] = get_time_ago(post['post_date'])

  # NOTE: this will not show more than the latest 100 replies
  replies = c.get_post_replies(post["id"], NUM_REPLIES_TO_SHOW)

  error_msg = None

  for reply in replies:
      reply['username'] = c.get_user(reply["id_user"])["username"]
      reply['time_ago'] = get_time_ago(reply['reply_date'])

  if request.method == 'GET':
    pass
  else:
    data = request.form
    form_submitted = CreatePostReplyForm(request.form)
    if form_submitted.validate():
      post_reply_content = data['post_reply_content']

      reply = {
        'id_parent': current_post_id,
        'id_user': user_id,
        'id_network': post['id_network'],
        'reply_text': post_reply_content
      }

      c.create_post_reply(current_post_id, reply)
      return redirect(
        url_for('posts.render_post') + "?id=%s" % str(current_post_id)
      )
    else:
      error_msg = "Oops. An error occurred. Did you forget to type a reply \
        before submitting?"


  new_form = CreatePostReplyForm()

  return render_template(
    'post.html',
    post=post,
    replies=replies,
    num_replies=len(replies),
    curr_user_id=user_id,
    form=new_form,
    error_msg=error_msg
  )

@posts.route("/ping")
@flask_login.login_required
def ping():
  c = Client(mock=False)
  return c.ping_post()
