#
# CultureMesh Locations API 
#

####################### GET methods #######################

def get_city(client, cityId):
	"""
	:param client: the CultureMesh API client
	:param cityId: the id of the city to fetch.

	Returns a city JSON.
	"""
	raise NotImplementedError

def get_region(client, regionId):
	"""
	:param client: the CultureMesh API client
	:param regionId: the id of the region to fetch

	Returns a region JSON.
	"""
	raise NotImplementedError

def get_country(client, countryId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the if of the country to fetch

	Returns a country JSON.
	"""
	raise NotImplementedError

def location_autocomplete(client, input_text):
	"""
	:param client: the CultureMesh API client
	:param input_text: partial input text to a query field

	Returns a list of location JSONs
	in order of relevance.
	"""
	raise NotImplementedError