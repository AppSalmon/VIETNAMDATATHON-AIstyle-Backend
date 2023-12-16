from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from AIstyle import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta

user = Blueprint("user", __name__)

@user.route("/login")
def login():
    return "This page is Login"

@user.route("/signup")
def signup():
    return "This page is signup"

@user.route("/logout")
def logout():
    return "This page is logout"
