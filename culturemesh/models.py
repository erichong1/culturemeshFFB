"""
Contains the CultureMesh user class.

Add any other CultureMesh objects here as needed.
"""

from flask_login import UserMixin
from utils import parse_date

class User(UserMixin):
	"""
	A CultureMesh user. This object is available to views
	via the 'current_user' variable for the current logged-in session.
	"""

	def __init__(self,
				 user_dict,
				 api_token=None,
				 api_token_expiration_epoch=None):
		self.user_id = int(user_dict['id'])
		self.username = user_dict['username']
		self.firstName = user_dict['first_name']
		self.lastName = user_dict['last_name']
		self.email = user_dict['email']
		self.registerDate = parse_date(user_dict['register_date'])
		self.role = int(user_dict['role'])
		self.gender = user_dict['gender']
		self.confirmed = user_dict['confirmed']
		self.act_code = user_dict['act_code']
		self.img_link = user_dict['img_link']
		self.fp_code = user_dict['fp_code']
		self.about_me = user_dict['about_me']
		self.last_login = parse_date(user_dict['last_login'])
		self._token = api_token

		# TODO: set this from upstream logic.
		self._token_expiration_epoch = 0

	def get_id(self):
		return str(self.user_id)

	@property
	def api_token(self):
		"""
		Return this user's CultureMesh API token.
		"""
		return self._token

	def secs_til_token_expiration(self):
		"""
		How many seconds before this user's
		CultureMesh API token expires.
		"""
		return self._token_expiration_epoch - int(time.time())

	def api_token_is_fresh(self):
		"""
		True if the user's API token is valid.
		"""
		return self.secs_til_token_expiration() > 0
