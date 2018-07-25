import http.client as httplib
import requests
import config
import flask_login

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
  REGISTER_USERNAME_TAKEN_MSG, REGISTER_EMAIL_TAKEN_MSG


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
    if not RegisterForm(request.form).validate():
      return render_template(
        'register.html', msg=REGISTER_ERROR_MSG, form=RegisterForm()
      )

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
      return render_template(
        'register.html',
        msg=REGISTER_PASSWORDS_DONT_MATCH_MSG,
        form=RegisterForm()
      )

    user_string = "Name: " + username + " Email: " + email + " Password: " + password + " Confirm Password: " + confirm_password
    return "<html>%s</html>" % user_string
  else:
    return render_template(
      'register.html', msg=REGISTER_MSG, form=RegisterForm()
    )

@app.route("/login", methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'POST':
      if not LoginForm(request.form).validate():
        return render_template('login.html', msg=LOGIN_ERROR, form=LoginForm())

      email_or_username = request.form['email_or_username']
      password = request.form['password']
      c = Client(mock=True)
      user_id = c.verify_account(email_or_username, password)

      # TODO: need to actually log the user in.
      if user_id == -1:
        return render_template('login.html', msg=LOGIN_FAILED_MSG, form=LoginForm())
      user_dict = c.get_user(int(user_id))
      if user_dict is not None:
        user = User(user_dict)
        flask_login.login_user(user)
        return redirect('/home')
      else:
        return render_template('login.html', msg=LOGIN_FAILED_MSG, form=LoginForm())
    else:
        return render_template('login.html', msg=LOGIN_MSG, form=LoginForm())

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
	c = Client(mock=True)
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
