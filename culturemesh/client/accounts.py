#
# CultureMesh Accounts API
#

from .client import Request
####################### GET methods #######################

	# TODO

####################### POST methods #######################

def verify_account(client, email_or_username, password):
	"""
	:param client: the CultureMesh API client
	:param email_or_usename: The email or username entered at login
	:param password: The password entered at login

	Returns: if email/username and password match an existing user's
	 data return the id of the corresponding user otherwise return None
	"""
	url = '/verify_account/%s/%s' % (str(email_or_username), str(password))
	return client._request(url, Request.GET)
