from flask import render_template, request
from culturemesh import app
from culturemesh import login_manager
from culturemesh.client import Client

import http.client as httplib
import requests
import config
import flask_login
from flask_login import current_user
import flask

from .forms import SearchForm, LoginForm
from .models import User


@app.route("/")
@app.route("/index")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/register")
def render_register_page():
	if current_user and current_user.is_authenticated:
		return page_not_found("")
	else:
		return render_template('register.html')

#TODO: make this work?
@app.route("/register", methods=['POST'])
def register():
	name = request.form["name"]
	email = request.form["email"]
	password = request.form["password"]
	confirm_password = request.form["confirm-password"]
	user_string = "Name: " + name + " Email: " + email + " Password: " + " Confirm Password: " + confirm_password
	return render_template('dashboard.html', user=user_string)

@app.route("/login")
def render_login_page():
	return render_template('login.html')

@app.route('/login_dummy', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == 'POST':
      user_id = request.form['user_id']

      if not user_id.isdigit():
        form = LoginForm()
        return render_template('login_dummy_fail.html', form=form)

      c = Client(mock=True)
      user_dict = c.get_user(int(user_id))
      if user_dict is not None:
        user = User(user_dict)
        flask_login.login_user(user)
        return flask.redirect('/home')
      else:
        form = LoginForm()
        return render_template('login_dummy_fail.html', form=form)
    else:
        form = LoginForm()
        return render_template('login_dummy.html', form=form)

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect('/index')

@app.route("/search", methods=['GET', 'POST'])
def render_search_page():
	if request.method == 'POST':
		c = Client(mock=True)
		data = request.form
		networks = c.get_networks(10, max_id=None) # filter_=data)
		return render_template('search_results.html', networks=networks)
	else:
		form = SearchForm()
		return render_template('search.html', form=form)

@app.route("/home")
@app.route("/home/dashboard")
@flask_login.login_required
def render_user_home():
	user_id = current_user.get_id()
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	return render_template('home_dashboard.html', user=user)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return flask.redirect('/login_dummy')

@app.route("/post")
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

@app.route("/home/account")
@flask_login.login_required
def render_user_home_account():
	user_id = current_user.get_id()
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")
	return render_template('home_account.html', user=user)

@app.route("/home/events")
@flask_login.login_required
def render_user_home_events():
	user_id = current_user.get_id()
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	# TODO: incorporate paging into the events hosting API call
	events_hosting = c.get_user_events(user_id, "hosting", 5)
	if events_hosting is None:
		return page_not_found("")

	return render_template('home_events.html', user=user,
		events_hosting=events_hosting)

@app.route("/home/networks")
@flask_login.login_required
def render_user_home_networks():
	user_id = current_user.get_id()
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	# TODO: incorporate paging into the user networks call.
	user_networks = c.get_user_networks(user_id, count=5)
	# TODO: construct network titles
	return render_template('home_networks.html', user=user,
		user_networks=user_networks)

##################### Other Callbacks #########################

@login_manager.user_loader
def load_user(user_id):
	c = Client(mock=True)
	user = c.get_user(user_id)
	if user is None:
		return None
	return User(user)

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
