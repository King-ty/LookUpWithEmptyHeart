from flask import Blueprint

mycenter_app = Blueprint('mycenter_app', __name__, template_folder='templates')

from .views import *
