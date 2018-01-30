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

@app.route("/network")
def network():
	network_id = request.args.get('id')
	c = Client(mock=True)
	try:
		network_id = int(network_id)
	except ValueError:
		return render_template('404.html')
	network = c.get_network(network_id)
	if not network:
		return render_template('404.html')

	# TODO: This assumes that the region ID and city ID are specified in the data.
	# This is not necessarily the case. This will need to be changed when we know
	# what unspecified region IDs will look like in  API calls.

	network_info = {}
	cur_country = c.get_country(network['location_cur']['country_id'])
	cur_region = c.get_region(network['location_cur']['region_id'])
	cur_city = c.get_city(network['location_cur']['city_id'])

	if network['network_class'] == 0:
		language = network['language_origin']['name']
		title = "%s speakers in %s, %s, %s" % (language, cur_city['name'], cur_region['name'], cur_country['name'])
		network_info['title'] = title
	elif network['network_class'] == 1:
		orig_country = c.get_country(network['location_origin']['country_id'])
		orig_region = c.get_region(network['location_origin']['region_id'])
		orig_city = c.get_city(network['location_origin']['city_id'])
		title = 'From %s, %s, %s in %s, %s, %s' % (orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name'])
		network_info['title'] = title

	return render_template('network.html', network_info=network_info)

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
