from flask import Blueprint, render_template, request
from culturemesh.client import Client
import flask_login

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route("/")
@flask_login.login_required
def render_post():
  fake_post = {
    "user_id": 3,
    "post_text": "Minus cumque corrupti porro natus tenetur delectus illum. Amet aut molestias eaque autem ea odio.\nAsperiores sed officia. Similique accusantium facilis sed. Eligendi tempora nisi sint tempora incidunt perferendis.",
    "network_id": 1,
    "img_link": "https://www.lorempixel.com/556/586",
    "vid_link": "https://dummyimage.com/909x765",
    "post_date": "2017-02-01 05:49:35",
    "post_class": 0,
    "id": 2,
    "post_original": "Not sure what this field is"
  }
  return render_template('post.html', post=fake_post)