#
# Contains classes for several userful CultureMesh Objects
#

from datetime import date

class User(object):
	"""
	A CultureMesh user.
	"""

	def __init__(self, user_id=None, username=None, 
				 firstName=None, lastName=None, email=None, 
				 registerDate=str(date.today()), role=None, gender=None, 
				 confirmed=False, act_code="IDK", 
		         img_link=None, fp_code="IDK", password=None,
		         about_me="", last_login=""):

		"""
 		 TODO: describe parameters.
		"""
		self.user_id = user_id
		self.username = username
		self.password = password
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.registerDate = registerDate
		self.role = role
		self.gender = gender
		self.confirmed = confirmed
		self.act_code = act_code
		self.img_link = img_link
		self.fp_code = fp_code
		self.about_me = about_me
		self.last_login = last_login