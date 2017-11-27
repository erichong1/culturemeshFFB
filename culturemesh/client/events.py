#
# CultureMesh Event API
#

####################### GET methods #######################

def get_event(client, eventId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the id of the event to fetch

	Returns an event by ID.
	"""
	raise NotImplementedError

def get_event_attendance_list(client, eventId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the id of the event in question

	Returns a list of user JSONs registered to this event.
	"""
	raise NotImplementedError

####################### POST methods #######################

def create_event(client, event):
	"""
	:param client: the CultureMesh API client
	:param event: the JSON of the event to create

	Creates a new event.
	"""
	raise NotImplementedError

####################### PUT methods #######################

def update_event(client, event):
	"""
	:param client: the CultureMesh API client
	:param event: the JSON of the event to update

	Updates an event.
	"""
	raise NotImplementedError