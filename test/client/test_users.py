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
	
	dracula_ebook_num = 345

	text = c.get_gutenberg_novel(dracula_ebook_num)
	assert_true('Dracula' in text)
	assert_true('Bram Stoker' in text)