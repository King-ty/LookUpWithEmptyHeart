from flask import Blueprint

chatroom_bp = Blueprint('chatroom_bp', __name__, template_folder='templates')

from .views import *