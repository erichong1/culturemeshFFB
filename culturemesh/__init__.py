from flask import Flask, render_template
from .objects import User
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '\x18\xe5\x16E\x15;\xd6\xdb8:\x88F\xcb\x03\x9cU\x08\x01\xb8\xe5:\x8ax\xe4'
csrf = CSRFProtect(app)
import culturemesh.views
