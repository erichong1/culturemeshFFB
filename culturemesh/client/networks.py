#
# CultureMesh Networks API
#

####################### GET methods #######################

from .client import Request

def get_networks(client, filter_=None):
	"""
	:param client: the CultureMesh API client
	:param filter: A json with which to filter a site-wide user query.

	Returns a list of users filtered by FILTER.
	"""
	params = {'filter': filter_}
	url = '/networks'
	return client._request(url, Request.GET, body_params=params)
