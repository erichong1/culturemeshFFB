"""
Contains the views and templates for the top-level site. This includes:
  - The home page
  - The about page
  - The registration page
  - The login page
"""
import http.client as httplib
import requests
import config
import flask_login
import werkzeug

from flask_wtf.csrf import CSRFError
from flask import render_template, request, redirect, session
from culturemesh import app, login_manager
from culturemesh.client import Client
from flask_login import current_user
from culturemesh.forms import LoginForm, RegisterForm
from culturemesh.models import User
from culturemesh.constants import LOGIN_MSG, LOGIN_FAILED_MSG, LOGIN_ERROR
from culturemesh.constants import REGISTER_MSG, \
  REGISTER_PASSWORDS_DONT_MATCH_MSG, REGISTER_ERROR_MSG, \
  REGISTER_USERNAME_TAKEN_MSG, REGISTER_EMAIL_TAKEN_MSG, PRIVACY_MSG

from culturemesh.utils import email_registered, username_taken

@app.route("/")
@app.route("/index")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user and current_user.is_authenticated:
    return page_not_found("")

  if request.method == 'POST':
    form = RegisterForm(request.form)

    firstname = request.form['firstname'].strip()
    lastname = request.form['lastname'].strip()
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()
    confirm_password = request.form["confirm_password"].strip()

    data = {
      'firstname': firstname,
      'lastname': lastname,
      'username': username,
      'email': email,
      'password': '',
      'confirm_password': ''
    }

    if not form.validate():
      return render_template(
        'register.html',
        msg=REGISTER_ERROR_MSG,
        privacy_msg=PRIVACY_MSG,
        form=RegisterForm(data=data)
      )

    c = Client(mock=False)

    if password != confirm_password:
      return render_template(
        'register.html',
        msg=REGISTER_PASSWORDS_DONT_MATCH_MSG,
        privacy_msg=PRIVACY_MSG,
        form=RegisterForm(data=data)
      )

    if username_taken(c, username):
      return render_template(
        'register.html',
        msg=REGISTER_USERNAME_TAKEN_MSG,
        privacy_msg=PRIVACY_MSG,
        form=RegisterForm(data=data)
      )

    if email_registered(c, email):
      return render_template(
        'register.html',
        msg=REGISTER_EMAIL_TAKEN_MSG,
        privacy_msg=PRIVACY_MSG,
        form=RegisterForm(data=data)
      )

    # TODO:
    user_string = "Name: " + username + " Email: " \
      + email + " Password: " + password + " Confirm Password: " + confirm_password \
      + "firstname: " + firstname + " lastname: " + lastname
    return "<html>%s</html>" % user_string
  else:
    return render_template(
      'register.html',
      msg=REGISTER_MSG,
      privacy_msg=PRIVACY_MSG,
      form=RegisterForm()
    )

@app.route("/login", methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'POST':
      if not LoginForm(request.form).validate():
        return render_template(
          'login.html', msg=LOGIN_ERROR, form=LoginForm()
        )

      email_or_username = request.form['email_or_username']
      password = request.form['password']
      c = Client(mock=False)
      try:
        token = c.get_token(email_or_username, password)
      except werkzeug.exceptions.Unauthorized as ex:
        # Unathorized.
        return render_template(
          'login.html', msg=LOGIN_FAILED_MSG, form=LoginForm()
        )

      user_id = c.get_user(token['id'])
      user = User(
        user_dict,
        api_token=token['token'],
        api_token_expiration_epoch=token['token_expiration_epoch']
      )
      flask_login.login_user(user)
      return redirect('/home')
    else:
        return render_template('login.html', msg=LOGIN_MSG, form=LoginForm())

@app.errorhandler(httplib.UNAUTHORIZED)
@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/index')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


##################### Other functions #########################

@login_manager.user_loader
def load_user(user_id):
	c = Client(mock=False)
	user = c.get_user(user_id)
	if user is None:
		return None
	return User(user)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(CSRFError)
@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
@app.errorhandler(httplib.METHOD_NOT_ALLOWED)
def internal_server_error(e):
    return render_template('error.html')

