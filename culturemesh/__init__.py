from flask import Flask, render_template
from .database import mysql
from .network import network
from .dbdiagnostics import dbdiagnostics
from .objects import User

app = Flask(__name__)
import culturemesh.views
