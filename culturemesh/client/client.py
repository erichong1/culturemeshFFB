#
# Inspired by: https://github.com/googlemaps/google-maps-services-python
#
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
		raise NotImplementedError

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
from .users import get_user
 ## Add more API call imports here

Client.get_gutenberg_novel = get_gutenberg_novel
Client.get_user = get_user
 ## Every single method imported above must be registered
 ## with the client here.
