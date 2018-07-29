#
# CultureMesh Accounts API
#

from .client import Request
####################### GET methods #######################

def get_token(client, email_or_username, password):
	"""
	:param client: the CultureMesh API Client
	:param email_or_username: The email or username of the user
	:param password: The password of the user
	"""
	url = 'account/token'
	basic_auth = (email_or_username, password)
	return client._request(url, Request.GET, basic_auth=basic_auth)
