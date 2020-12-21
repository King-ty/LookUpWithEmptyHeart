from flask import Blueprint

bbs_bp = Blueprint('bbs',
                   __name__,
                   url_prefix='/bbs',
                   template_folder='templates')

from .views import *
