"""
Contains the CultureMesh user class.

Add any other CultureMesh objects here as needed.
"""

import config
import datetime

from flask_login import UserMixin

class User(UserMixin):
	"""
	A CultureMesh user. This object is available to views
	via the 'current_user' variable for the current logged-in session.
	"""

	def __init__(self, user_dict):
		self.user_id = int(user_dict['id'])
		self.username = user_dict['username']
		self.firstName = user_dict['firstName']
		self.lastName = user_dict['lastName']
		self.email = user_dict['email']
		self.registerDate = datetime.datetime.strptime(
			user_dict['registerDate'], config.DATETIME_FMT_STR
		)
		self.role = int(user_dict['role'])
		self.gender = user_dict['gender']
		self.confirmed = user_dict['confirmed']
		self.act_code = user_dict['act_code']
		self.img_link = user_dict['img_link']
		self.fp_code = user_dict['fp_code']
		self.about_me = user_dict['about_me']
		self.last_login = datetime.datetime.strptime(
			user_dict['last_login'], config.DATETIME_FMT_STR
		)

	def get_id(self):
		return str(self.user_id)

	@property
	def api_token(self):
		"""
		Return this user's CultureMesh API token.
		"""
		return "todo"
