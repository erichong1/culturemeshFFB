#
# Contains utilities used by more than one blueprint
#

from culturemesh.constants import BLANK_PROFILE_IMG_URL
from culturemesh.constants import USER_IMG_URL_FMT
from culturemesh.client import Client

from utils import parse_date
from utils import get_month_abbr

def get_network_title(network):
  """Returns the title of a network given a network
  JSON as a dict"""

  cur_country = network['country_cur']
  cur_region = network['region_cur']
  cur_city = network['city_cur']

  orig_country = network['country_origin']
  orig_region = network['region_origin']
  orig_city = network['city_origin']

  cur_location = ', '.join([l for l \
    in [cur_city, cur_region, cur_country] if l is not None])

  orig_location = ', '.join([l for l \
    in [orig_city, orig_region, orig_country] if l is not None])

  if network['network_class'] == '_l':

    # Language network
    language = network['language_origin']
    return "%s speakers in %s" % (language, cur_location)

  elif network['network_class'] == 'cc' \
    or network['network_class'] == 'rc' \
    or network['network_class'] == 'co':
    # City network (cc), region network (rc), or
    # country network (co).
    # Title-wise, we treat them all the same.

    return 'From %s in %s' % (orig_location, cur_location)

  else:
    return "Unknown"

def get_user_image_url(user):
  """Returns the URL of a user's profile image
  given a user JSON as a dict
  """

  if user['img_link'] is None:
    return BLANK_PROFILE_IMG
  else:
    return USER_IMG_URL_FMT % user['img_link']

def get_short_network_join_date(network):
  """Returns a short version of the user's Join
  date to a network:

  Mon day, Year
  """

  if 'join_date' not in network:
    return "unknown"
  else:
    date = parse_date(network['join_date'])
    short_month = get_month_abbr(date)
    year = date.year
    day = date.day
    return "%s %s, %s" % (str(short_month), str(day), str(year))


