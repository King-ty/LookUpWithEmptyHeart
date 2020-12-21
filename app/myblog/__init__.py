from flask import Blueprint

myblog_bp = Blueprint('myblog', __name__, template_folder='templates')

from .views import *
