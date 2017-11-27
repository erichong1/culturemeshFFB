#
# CultureMesh Users API
#

####################### GET methods #######################

def get_users(client, filter_=None):
	"""
	:param client: the CultureMesh API client
	:param filter: A json with which to filter a site-wide user query.

	Returns a list of users filtered by FILTER.
	"""
	params = {'filter': filter_}
	return client._request('/users', params)

def get_user(client, userId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return.

	Returns JSON of user.
	"""
	params = {}
	return client._request('/user/%s' % str(user_id), params)

def get_user_networks(client, userId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return a list of networks for.

	Returns list of network JSONs to which USER_ID belongs.
	"""
	params = {}
	return client._request('/user/%s/networks' % str(user_id), params)

def get_user_posts(client, userId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return posts for.

	Returns list of post JSONs authered by USER_ID.
	"""
	params = {}
	return client._request('/user/%s/posts' % str(user_id), params)

def get_user_events(client, userId, role):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return events for.
	:param role: can be "hosting" or "attending"

	Returns list of events related to USER_ID, according to ROLE.
	"""
	params = {}
	return client._request('/user/%s/events' % str(user_id), params)


####################### POST methods #######################

def create_user(client, user):
	"""
	:param client: the CultureMesh API client
	:param user: the user JSON to create.

	Creates a new user.
	"""
	params = {"user": user}
	return client._request('/user', params) 

def add_user_to_event(client, userId, eventId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to to add
	:param eventId: The id of the event to register this user to

	Registers a user to a attend an event.
	"""
	params = {}
	return client._request('/user/%s/addToEvent/%s' % (str(userId), str(eventId)), params) 

def add_user_to_network(client, userId, networkId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to add
	:param networkId: The id of the network to add user to

	Adds a user to a network.
	"""
	params = {}
	return client._request('/user/%s/addToNetwork/%s' % (str(userId), str(networkId)), params) 

####################### PUT methods #######################

def update_user(client, user):
	"""
	:param client: the CultureMesh API client
	:param user: A user JSON to update an existing user with.

	Updates the information of a user.
	"""
	params = {'user': user}

	raise NotImplementedError

	#TODO: how to differentiate this as a POST here?

	return client._request('/user', params) 