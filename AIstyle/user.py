from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from AIstyle.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from AIstyle import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta

user = Blueprint("user", __name__)

def clean_print(lst_print):
    print("======================================")
    print(lst_print)
    print("======================================")

@user.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        clean_print([email, password])

    return render_template("login.html", user = current_user)

@user.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        password = generate_password_hash(password, method = "sha256")
        clean_print(request.form)
    return render_template("signup.html", user = current_user)

@user.route("/logout")
def logout():
    return {
            "status": "success"
    }