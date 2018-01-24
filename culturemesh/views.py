from flask import render_template, request
from culturemesh import app
from culturemesh.client import Client

import hashlib
import http.client as httplib
import requests
import config

from .forms import SearchForm


@app.route("/")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/base")
def base():
	return render_template('base.html')

@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html')

@app.route("/register")
def render_register_page():
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

@app.route("/login", methods=['GET', 'POST'])
def login():
	email = request.form["email"]
	password = request.form["password"]
	return "Email: " + email + " Password: " + password

@app.route("/search", methods=['GET', 'POST'])
def render_search_page():
	form = SearchForm()
	return render_template('search.html', form=form)

@app.route("/home")
def render_user_home():
	return render_template('user_home.html')

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
