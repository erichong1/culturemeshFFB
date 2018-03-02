from flask import Blueprint, render_template, request
from culturemesh.client import Client
from culturemesh.search.forms.search_forms import SearchForm

search = Blueprint('search', __name__, template_folder='templates')

@search.route("/", methods=['GET', 'POST'])
def render_search_page():
  if request.method == 'POST':
    c = Client(mock=True)
    data = request.form
    networks = c.get_networks(10, max_id=None) # filter_=data)
    return render_template('search_results.html', networks=networks)
  else:
    return render_template('search.html', form=SearchForm())