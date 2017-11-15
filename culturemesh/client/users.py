#
# CultureMesh API Client
#

""" Gets CultureMesh User-related information """

def get_user(client, user_id):
	"""
	:param user_id: The id of the user to return.
	"""
	
	params = {}
	return client._request('/user/%s' % str(user_id), params)