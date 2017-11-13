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

    	# TODO
		return requests.get(url)



""" Register the client with the API functions. """
from .example_api_module import get_gutenberg_novel
 ## Add more API call imports here

Client.get_gutenberg_novel = get_gutenberg_novel
 ## Every single method imported above must be registered
 ## with the client here.
