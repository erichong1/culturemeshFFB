#
# Tests client/posts.py
# 

from nose.tools import assert_true
from culturemesh.client import Client

def test_posts():
	c = Client(mock=True)

	post = c.get_post(4)
	print(post)
	assert_true(post['vid_link'] == "https://www.lorempixel.com/1016/295")

def test_get_post_replies():
  """
  Tests that we can get post replies as expected. 
  """
  c = Client(mock=True)
  posts1 = c.get_post_replies(1)
  posts2 = c.get_post_replies(2)
  print(posts1)

  assert_true(len(posts1) == 2)
  assert_true(len(posts2) == 0)