from flask import Blueprint, render_template, request
from culturemesh.client import Client
import flask_login

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route("/")
@flask_login.login_required
def render_post():
  fake_post = {
    "post_title": "This is an example post title",
    "user_id": 3,
    "post_text": "Minus cumque corrupti porro natus tenetur delectus illum. Amet aut molestias eaque autem ea odio.\nAsperiores sed officia. Similique accusantium facilis sed. Eligendi tempora nisi sint tempora incidunt perferendis.",
    "network_id": 1,
    "img_link": "https://www.lorempixel.com/556/586",
    "vid_link": "https://dummyimage.com/909x765",
    "post_date": "2017-02-01 05:49:35",
    "post_class": 0,
    "id": 2,
    "post_original": "Not sure what this field is",
    "comments": [("anotheruser", "This is a comment about the post."), ("yetanotheruser", "I agree with above."), ("randomuser", "I don't agree with what you're saying. Why do you think that this is true?")]
  }
  return render_template('post.html', post=fake_post)