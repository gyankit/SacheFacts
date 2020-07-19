from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or Bcrypt.generate_password_hash('SacheFact').decode('utf-8')

db_settings = {
    'SQLALCHEMY_TRACK_MODIFICATIONS': os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('SQLALCHEMY_DATABASE_URI')
}

file_settings = {
    'UPLOAD_FOLDER': os.environ.get('UPLOAD_FOLDER'),
    'UPLOAD_SITE': os.environ.get('UPLOAD_SITE')
}

mail_settings = {
    'MAIL_SERVER': os.environ['MAIL_SERVER'],
    'MAIL_PORT': os.environ['MAIL_PORT'],
    'MAIL_USE_TLS': os.environ['MAIL_USE_TLS'],
    'MAIL_USERNAME': os.environ['MAIL_USERNAME'],
    'MAIL_PASSWORD': os.environ['MAIL_PASSWORD'],
    'MAIL_DEFAULT_SENDER': os.environ['MAIL_DEFAULT_SENDER']
}

app.config.update(db_settings)
app.config.update(file_settings)
app.config.update(mail_settings)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'admins.login'
login_manager.login_message = f'Login required to excess this page'
login_manager.login_message_category = 'warning'

from App import models
from App import handlers

from App.users import user
from App.admins import admin

app.register_blueprint(user)
app.register_blueprint(admin)

login_manager._user_callback = models.load_user