#
# This file contains high-level configuration variables for CultureMeshFFB.
#
#     DO NOT INCLUDE SENSITIVE CONFIGURATION HERE.  THIS WILL BE 
#     IN VERSION CONTROL.
#

DEBUG_PORT=8080
DEBUG_ADDR='127.0.0.1'
ROOT_PATH=""

from culturemesh import app

def init():
  global ROOT_PATH
  ROOT_PATH = app.root_path


