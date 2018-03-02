from flask import Blueprint, render_template, request
from culturemesh.client import Client
import flask_login

events = Blueprint('events', __name__, template_folder='templates')