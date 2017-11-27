#
# CultureMesh API Client
#
# Inspired by: https://github.com/googlemaps/google-maps-services-python
# TODO: add license information. 
#

"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

import requests
import os
import json
from urllib.parse import urlparse

class Client(object):
	""" Talks directly to CultureMesh """

	_api_base_url_ = "www.culturemesh.com/api/v1/"

	def __init__(self, key=None, client_id=None, client_secret=None,
                 timeout=None, connect_timeout=None, read_timeout=None,
                 retry_timeout=60, requests_kwargs=None,
                 queries_per_second=10, channel=None, mock=True):
		# TODO: insert client initialization here. 
		self.mock = mock
		pass 

	def _request(self, url, params):
		"""
		Carries out HTTP GET/POST.  Returns body as JSON.
    	"""
		if self.mock:
			return self._mock_request(url, params)
		raise NotImplementedError("Coming soon.")

	def _mock_request(self, url, params):
		"""
		Used in development.  Uses local data to return API responses.
		"""
		url_ = urlparse(url)
		path = os.path.normpath(url_.path).split(os.sep)
		print(path)
		if len(path) == 3:
			if path[1] == "user":
				user_id = int(path[2])
				return self._mock_get_user(user_id)

		return 


	def _mock_get_user(self, user_id):
		with open('../data/db_mock_users.json') as users:    
			users = json.load(users)
			for u in users:
				if u['user_id'] == user_id:
					return u
		return None



""" Register the client with the API functions. """

from .example_api_module import get_gutenberg_novel
from .events import get_event
from .events import get_event_attendance_list
from .events import create_event
from .events import update_event
from .posts import get_post
from .posts import get_post_replies
from .posts import create_post
from .posts import create_post_reply
from .users import get_users
from .users import get_user
from .users import get_user_networks
from .users import get_user_posts
from .users import get_user_events
from .users import create_user
from .users import add_user_to_event
from .users import add_user_to_network
from .users import update_user

# We may consider adding a wrapper around these assignments
# below to introduce more specific features for the client.

Client.get_gutenberg_novel = get_gutenberg_novel
Client.get_event = get_event
Client.get_event_attendance_list = get_event_attendance_list
Client.create_event = create_event
Client.update_event = update_event
Client.get_post = get_post
Client.get_post_replies = get_post_replies
Client.create_post = create_post
Client.create_post_reply = create_post_reply
Client.get_users = get_users
Client.get_user = get_user
Client.get_user_networks = get_user_networks
Client.get_user_posts = get_user_posts
Client.get_user_events = get_user_events
Client.create_user = create_user
Client.add_user_to_event = add_user_to_event
Client.add_user_to_network = add_user_to_network
Client.update_user = update_user
