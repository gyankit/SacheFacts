from flask import Blueprint

admin = Blueprint('admins', __name__)

from App.admins import routes