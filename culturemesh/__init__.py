from flask import Flask, render_template
from .objects import User

app = Flask(__name__)
import culturemesh.views
