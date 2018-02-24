from flask import render_template, request
from culturemesh import app
from culturemesh.client import Client

import hashlib
import http.client as httplib
import requests
import config

from .forms import SearchForm


@app.route("/")
@app.route("/index")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

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
	if request.method == 'POST':
		c = Client(mock=True)
		data = request.form
		networks = c.get_networks(10, max_id=None) # filter_=data)
		return render_template('search_results.html', networks=networks)
	else:
		form = SearchForm()
		return render_template('search.html', form=form)

@app.route("/network")
def network():
	network_id = request.args.get('id')
	if not network_id :
		return render_template('404.html')
	c = Client(mock=True)
	try:
		network_id = int(network_id)
	except ValueError:
		return render_template('404.html')
	network = c.get_network(network_id)
	if not network:
		return render_template('404.html')

	# TODO: Get user ID and work out if user is in network.
	# Add join us button to page if they're not.

	posts = c.get_network_posts(network_id, 3)
	events = c.get_network_events(network_id, 3)

	# TODO: This assumes that the region ID and city ID are specified in the data.
	# This is not necessarily the case. This needs to be changed using the new information
	# that Ian sent us about network classes.

	network_info = {}
	network_info['network_id'] = network_id
	network_info['posts'] = posts
	network_info['events'] = events
	cur_country = c.get_country(network['location_cur']['country_id'])
	cur_region = c.get_region(network['location_cur']['region_id'])
	cur_city = c.get_city(network['location_cur']['city_id'])

	if network['network_class'] == 0:
		language = network['language_origin']['name']
		network_title = "%s speakers in %s, %s, %s" % tuple(map(lambda x: x.title(), [language, cur_city['name'], cur_region['name'], cur_country['name']]))
		network_info['network_title'] = network_title
	elif network['network_class'] == 1:
		orig_country = c.get_country(network['location_origin']['country_id'])
		orig_region = c.get_region(network['location_origin']['region_id'])
		orig_city = c.get_city(network['location_origin']['city_id'])
		network_title = 'From %s, %s, %s in %s, %s, %s' % tuple(map(lambda x: x.title(), [orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name']]))
		network_info['network_title'] = network_title

	return render_template('network.html', network_info=network_info)

@app.route("/network/events")
def network_events() :
	# TODO: A lot of this code is repeated from network(), with just minor variations.
	# This should be factored out.
	network_id = request.args.get('id')
	if not network_id :
		return render_template('404.html')
	c = Client(mock=True)
	try:
		network_id = int(network_id)
	except ValueError:
		return render_template('404.html')
	network = c.get_network(network_id)
	if not network:
		return render_template('404.html')

	# TODO: Get user ID and work out if user is in network.
	# Add join us button to page if they're not.

	events = None

	old_index = request.args.get('index')
	if not old_index:
		events = c.get_network_events(network_id, 10)
	else:
		try:
			old_index = int(old_index)
		except ValueError:
			return render_template('404.html')
		events = c.get_network_events(network_id, 10, old_index - 1)

	# TODO: Add better handling for when there's no posts left.

	if not events :
		event_index = old_index
	else :
		event_index = events[-1]['id']

	# TODO: This assumes that the region ID and city ID are specified in the data.
	# This is not necessarily the case. This needs to be changed using the new information
	# that Ian sent us about network classes.

	network_info = {}
	network_info['network_id'] = network_id
	network_info['events'] = events
	cur_country = c.get_country(network['location_cur']['country_id'])
	cur_region = c.get_region(network['location_cur']['region_id'])
	cur_city = c.get_city(network['location_cur']['city_id'])

	if network['network_class'] == 0:
		language = network['language_origin']['name']
		network_title = "%s speakers in %s, %s, %s" % tuple(map(lambda x: x.title(), [language, cur_city['name'], cur_region['name'], cur_country['name']]))
		network_info['network_title'] = network_title
	elif network['network_class'] == 1:
		orig_country = c.get_country(network['location_origin']['country_id'])
		orig_region = c.get_region(network['location_origin']['region_id'])
		orig_city = c.get_city(network['location_origin']['city_id'])
		network_title = 'From %s, %s, %s in %s, %s, %s' % tuple(map(lambda x: x.title(), [orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name']]))
		network_info['network_title'] = network_title

	return render_template('network_events.html', network_info=network_info, event_index=event_index)

@app.route("/network/posts")
def network_posts() :
	# TODO: A lot of this code is repeated from network(), with just minor variations.
	# This should be factored out.
	network_id = request.args.get('id')
	if not network_id :
		return render_template('404.html')
	c = Client(mock=True)
	try:
		network_id = int(network_id)
	except ValueError:
		return render_template('404.html')
	network = c.get_network(network_id)
	if not network:
		return render_template('404.html')

	# TODO: Get user ID and work out if user is in network.
	# Add join us button to page if they're not.

	posts = None

	old_index = request.args.get('index')
	if not old_index:
		posts = c.get_network_posts(network_id, 10)
	else:
		try:
			old_index = int(old_index)
		except ValueError:
			return render_template('404.html')
		posts = c.get_network_posts(network_id, 10, old_index - 1)

	# TODO: Add better handling for when there's no events left.

	if not posts :
		post_index = old_index
	else :
		post_index = posts[-1]['id']

	# TODO: This assumes that the region ID and city ID are specified in the data.
	# This is not necessarily the case. This needs to be changed using the new information
	# that Ian sent us about network classes.

	network_info = {}
	network_info['network_id'] = network_id
	network_info['posts'] = posts
	cur_country = c.get_country(network['location_cur']['country_id'])
	cur_region = c.get_region(network['location_cur']['region_id'])
	cur_city = c.get_city(network['location_cur']['city_id'])

	if network['network_class'] == 0:
		language = network['language_origin']['name']
		network_title = "%s speakers in %s, %s, %s" % tuple(map(lambda x: x.title(), [language, cur_city['name'], cur_region['name'], cur_country['name']]))
		network_info['network_title'] = network_title
	elif network['network_class'] == 1:
		orig_country = c.get_country(network['location_origin']['country_id'])
		orig_region = c.get_region(network['location_origin']['region_id'])
		orig_city = c.get_city(network['location_origin']['city_id'])
		network_title = 'From %s, %s, %s in %s, %s, %s' % tuple(map(lambda x: x.title(), [orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name']]))
		network_info['network_title'] = network_title

	return render_template('network_posts.html', network_info=network_info, post_index=post_index)

@app.route("/home")
@app.route("/home/dashboard")
def render_user_home():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)
	events_hosting = c.get_user_events(user_id, "hosting", 5)
	if user is None:
		return page_not_found("")

	return render_template('home_dashboard.html', user=user, events_hosting=events_hosting)

@app.route("/post")
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
def render_user_home_account():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")
	return render_template('home_account.html', user=user)

@app.route("/home/events")
def render_user_home_events():
	user_id = int(request.args.get('id'))
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
def render_user_home_networks():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	# TODO: incorporate paging into the user networks call.
	user_networks = c.get_user_networks(user_id, count=5)
	# TODO: construct network titles

	titles = []
	for network in user_networks:
		title_template = "From %s, %s, %s in %s, %s, %s, that speak %s."
		location_cur = network['location_cur']
		city = c.get_city(location_cur['city_id'])['name']
		region = c.get_region(location_cur['region_id'])['name']
		country = c.get_country(location_cur['country_id'])['name']

		location_origin = network['location_origin']
		city_orig = c.get_city(location_origin['city_id'])['name']
		region_orig = c.get_region(location_origin['region_id'])['name']
		country_orig = c.get_country(location_origin['country_id'])['name']



		language = network['language_origin']['name']
		titles.append(title_template % (city_orig.title(), region_orig.title(), country_orig.title(),
															      city.title(), region.title(), country.title(), language))

	return render_template('home_networks.html', user=user,
		user_network_titles=titles)

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
