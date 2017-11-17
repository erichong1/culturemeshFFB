#
# CultureMesh API Client
#

""" Gets CultureMesh User-related information """

def get_users(client, filter=None):
	raise NotImplemented

def get_user(client, user_id):
	"""
	:param user_id: The id of the user to return.

	Returns JSON of user.
	"""
	
	params = {}
	return client._request('/user/%s' % str(user_id), params)

def get_user_networks(client, user_id):
	raise NotImplemented

def get_user_posts(client, user_id):
	raise NotImplemented

def get_user_events(client, user_id):
	raise NotImplemented

# The POST, PUT requests will be added later.