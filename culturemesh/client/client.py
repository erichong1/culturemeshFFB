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
from config import _API_BASE_URL_

MOCK_API = True

# Might change.

class Client(object):
	""" Talks directly to CultureMesh """

	def __init__(self, key=None, client_id=None, client_secret=None,
                 timeout=None, connect_timeout=None, read_timeout=None,
                 retry_timeout=60, requests_kwargs=None,
                 queries_per_second=10, channel=None):
		# TODO: insert client initialization here. 
		pass 

	def _request(self, url, params):
		"""
		Carries out HTTP GET/POST.  Returns body as JSON.
    	"""
		if MOCK_API:
			return self._mock_request(url, params)
		return None

	def _mock_request(self, url, params):
		"""
		Used in development.  Uses local data to return API responses.
		"""
		return None



""" Register the client with the API functions. """
from .example_api_module import get_gutenberg_novel
from .users import get_user
 ## Add more API call imports here

Client.get_gutenberg_novel = get_gutenberg_novel
Client.get_user = get_user
 ## Every single method imported above must be registered
 ## with the client here.
