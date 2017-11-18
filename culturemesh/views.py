from flask import render_template, request
from culturemesh import app
from .database import mysql
from culturemesh.client import Client

import hashlib
import http.client as httplib
import requests

@app.route("/example_api_call")
def example_api_call():
	"""
	For illustrative purposes only.
	"""

	c = Client()
	dracula_ebook_num = 345
	dracula_text = c.get_gutenberg_novel(dracula_ebook_num)
	return render_template('example.html', example=dracula_text)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
	searchFrom = request.form["from"]
	searchIn = request.form["in"]
	return "Looking for users from " + searchFrom + " in " + searchIn + "."

@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html')

@app.route("/register")
def register():
	return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	email = request.form["email"]
	password = request.form["password"]
	return "Email: " + email + " Password: " + password

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
