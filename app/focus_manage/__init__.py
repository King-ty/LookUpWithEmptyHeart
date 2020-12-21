from flask import Blueprint

focus_bp = Blueprint('focus_bp', __name__, template_folder='templates')

from .views import *
