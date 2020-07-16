from App.users import user
from flask import render_template, redirect, url_for


@user.route('/')
def home():
    return render_template('user/home.html')