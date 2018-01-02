#
# Tests client/networks.py
#

from nose.tools import assert_true, assert_equal
from culturemesh.client import Client

def test_get_networks():
  """
	Tests basic network retrieval pagination. For illustrative purposes, 
  client returns mock data.
	"""
  c = Client(mock=True)
  networks = c.get_networks(10)
  assert_equal(len(networks), 2)

  networks1 = c.get_networks(1)
  assert_equal(networks1[0]['id'], 1)
  assert_equal(len(networks1), 1)

  networks2 = c.get_networks(1, max_id=0)
  assert_equal(networks2[0]['id'], 0)
  assert_equal(len(networks2), 1)
