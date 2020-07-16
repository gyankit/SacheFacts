from flask import Blueprint

user = Blueprint('users', __name__)

from App.users import routes