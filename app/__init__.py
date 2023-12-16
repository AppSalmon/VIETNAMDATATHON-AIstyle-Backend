from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
user_postgreSQL = os.environ.get("user_postgreSQL")
password_postgreSQL = os.environ.get("password_postgreSQL")

# print(SECRET_KEY, DB_NAME, user_postgreSQL, password_postgreSQL)

def create_database(app,remove):
    '''
    Chưa comment
    '''
    with app.app_context():
        if remove == True:
            db.drop_all()
        db.create_all()
    print("=> Created BD!")

def create_app(remove = False):
    '''
    Chưa comment
    '''
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    # app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql+psycopg2://{user_postgreSQL}:{password_postgreSQL}@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:211551@localhost/productdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    create_database(app,remove)

    from app.user import user
    from app.home import home
    from app.routes import routes


    app.register_blueprint(user)
    app.register_blueprint(home)
    app.register_blueprint(routes)


    return app

from app.models import *
from app.home import *
from app.user import *
from app.routes import *