from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import model



lists = Blueprint('lists', __name__, url_prefix='/listas')


@lists.route('/', methods=['GET'])
def index():
    return render_template('signup.html')  

def configure(app):
    app.register_blueprint(lists)

