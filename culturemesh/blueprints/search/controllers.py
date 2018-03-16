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
    return render_template('search_results.html', networks=networks)
  else:
    return render_template('search.html', form=SearchForm())
