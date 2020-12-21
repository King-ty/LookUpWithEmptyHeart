from flask import Blueprint

todolist_bp = Blueprint('todolist', __name__, template_folder = 'templates')

from .views import *