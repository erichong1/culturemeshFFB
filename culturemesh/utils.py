#
# Contains utilities used by more than one blueprint
#

def get_network_title(network):
  """Returns the title of a network given a network
  JSON dictionary"""

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
    # country network (co)
    return 'From %s in %s' % (orig_location, cur_location)

  else:
    return "Unknown"

