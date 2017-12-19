#
# Tests client/events.py
# 

from nose.tools import assert_true
from culturemesh.client import Client

def test_get_event():
  """
  Tests we can get a single event.
  """
  c = Client(mock=True)

  event1 = c.get_event(2)
  event2 = c.get_event(0)

  print(event1)

  assert_true(event1 is not None and \
     event1['title'] == "Reverse-engineered 6thgeneration neural-net")
  assert_true(event2 == None)