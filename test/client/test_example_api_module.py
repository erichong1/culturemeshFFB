#
# Tests example_api_module.py
# 

from nose.tools import assert_true

from culturemesh.client import Client
import requests

def test_get_dracula():
	"""
	Tests we can retrieve Dracula. 
	"""

	c = Client(mock=False)

	# Here, we want to mock the client. 
	
	dracula_ebook_num = 345

	text = c.get_gutenberg_novel(dracula_ebook_num)
	assert_true('Dracula' in text)
	assert_true('Bram Stoker' in text)

## More API call methods would go below here..