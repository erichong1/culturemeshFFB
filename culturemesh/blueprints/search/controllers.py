from flask import Blueprint, render_template, request
from culturemesh.client import Client
from culturemesh.blueprints.search.forms.search_forms import SearchForm

search = Blueprint('search', __name__, template_folder='templates')

@search.route("/", methods=['GET', 'POST'])
def render_search_page():
  if request.method == 'POST':
    c = Client(mock=True)
    data = request.form
    search_type = str(data.get('search_type'))
    filter_ ={"search_type": search_type}
    if search_type == "location":
        filter_["from"] = data['origin_or_language']
    elif search_type == "language":
        filter_["language"] = data['origin_or_language']
    else:
        raise Exception("Invalid Search Type %s" % search_type)
    filter_["near"] = data['residence']
    networks = c.get_networks(10, max_id=None, filter_=filter_)
    for network in networks:
        for location in ['location_origin', 'location_cur']:
            network[location]['city_name'] = c.get_city(network[location]['city_id'])['name']
            network[location]['country_name'] = c.get_country(network[location]['country_id'])['name']
            network[location]['region_name'] = c.get_region(network[location]['region_id'])['name']

    if search_type == "location":
        return render_template('location_search_results.html', networks=networks)
    elif search_type == "language":
        return render_template('language_search_results.html', networks=networks)
    else:
        raise Exception("Invalid Search Type %s" % search_type)
  else:
    return render_template('search.html', form=SearchForm())
