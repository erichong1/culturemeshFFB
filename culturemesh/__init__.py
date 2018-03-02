from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__,
            template_folder="templates")

# Install Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Install CSRF Protection
app.secret_key = '\x18\xe5\x16E\x15;\xd6\xdb8:\x88F\xcb\x03\x9cU\x08\x01\xb8\xe5:\x8ax\xe4'
csrf = CSRFProtect(app)

import culturemesh.views

# Register Blueprints

from culturemesh.user_home.controllers import user_home
from culturemesh.search.controllers import search
app.register_blueprint(user_home, url_prefix='/home')
app.register_blueprint(search, url_prefix='/search')
