#
# Tests client/users.py
# 

from nose.tools import assert_true
from culturemesh.client import Client

def test_get_user():
	"""
	Tests we can retrieve a user.  For illustrative purposes, the client is not mocked!
	"""

	c = Client()

	# Here, we want to mock the client. 
	
	user = c.get_user(3)
	assert(user is not None)