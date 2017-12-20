#
# Tests client/languages.py
# 

from nose.tools import assert_true
from culturemesh.client import Client

def test_language():
  """
  Basic functionality of retrieving
  a mock language. 
  """ 

  c = Client(mock=True)
  lang1 = c.get_language(2)
  print(lang1)
  assert_true(lang1 and lang1['name'] == "entish")
