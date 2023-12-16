from flask import Blueprint, render_template, flash, request, jsonify, session
from flask_login import current_user, login_required
import json

home = Blueprint("home", __name__)

@home.route("/")
def home_page():
    return "This is home page"