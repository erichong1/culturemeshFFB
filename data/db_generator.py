#
# For dev use only!
#

import sys
import json
import random
from faker import Faker

if hasattr(sys, 'real_prefix'):
	print("This should not be run from inside a virtualenv")
	exit()

""" Creates a randomly generated mock database """

def make_users(faker, num_users):
	"""
	Makes NUM_USERS fake users and dumps them to a json file.
	"""

	user_id_ctr = 1
	users = []
	for _ in range(num_users):
		user = {}
		user['user_id'] = user_id_ctr
		user['username'] = faker.user_name()
		user['firstName'] = faker.first_name()
		user['lastName'] = faker.last_name()
		user['email'] = faker.email()
		user['registerDate'] = str(faker.past_datetime(start_date="-1000d", tzinfo=None))
		user['role'] = 1 # Not sure
		user['last_login'] = str(faker.past_datetime(start_date="-7d", tzinfo=None))
		user['gender'] = random.choice(['male', 'female'])
		user['about_me'] = faker.text(max_nb_chars=200, ext_word_list=None)
		user['confirmed'] = random.choice([True, False])
		user['act_code'] = "IDK"
		user['img_link'] = faker.image_url(width=None, height=None)
		user['fp_code'] = "IDK"

		user_id_ctr += 1
		users.append(user)

	with open('db_mock_users.json', 'w+') as outfile:
		json.dump(users, outfile)

def create_culturemesh_db(num_users=5, num_networks=2, num_events=4, num_posts=5):
	"""
	Makes a fake culture mesh database in the form of json files. 
	"""

	faker = Faker()
	faker.seed(1)
	
	make_users(faker, num_users)

	# Create some Networks
		# TODO

	# Create some Events
		# TODO

	# Create some Posts
		# TODO

if __name__ == "__main__":
	create_culturemesh_db()