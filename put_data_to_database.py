from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from AIstyle import *
from AIstyle.models import (
    Brand,
    Product,
    ProductDetail,
    User,
    Order,
    Chat,
    ChatBox,
    ResultBox
)
from AIstyle import db


load_dotenv(dotenv_path = "./AIstyle/.env")

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
user_postgreSQL = os.environ.get("user_postgreSQL")
password_postgreSQL = os.environ.get("password_postgreSQL")



app = create_app(remove = True)

import pandas as pd
df_btc = pd.read_csv("Process_data/data_btc.csv")
print(df_btc)

# print("===>", Product)
brand1 = Brand(name = "Nike2", description = "haha")
with app.app_context():
    db.session.add(brand1)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)