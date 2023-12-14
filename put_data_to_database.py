from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# from AIstyle import *
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
from AIstyle import db, create_app


load_dotenv(dotenv_path = "./AIstyle/.env")

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
user_postgreSQL = os.environ.get("user_postgreSQL")
password_postgreSQL = os.environ.get("password_postgreSQL")



app = create_app(remove = True)


import pandas as pd
df_btc = pd.read_csv("Process_data/data_btc.csv")
print(df_btc)


''' Add data brand to database '''
brand_nike = Brand(name = "nike", description = "Nike, Inc. is a globally renowned American multinational corporation that is engaged in the design, development, manufacturing, and marketing of footwear, apparel, equipment, accessories, and services. The company is one of the world's largest and most recognizable athletic and sportswear brands, and it has established itself as a symbol of innovation, performance, and style.")
brand_adidas = Brand(name = "adidas", description = "Adidas is a multinational corporation that is widely recognized for its presence in the sportswear and athletic footwear industry. The company was founded on August 18, 1949, by Adolf Dassler in Herzogenaurach, Germany. The name Adidas is a combination of the founder's nickname, Adi, and the first three letters of his last name.")

with app.app_context():
    db.session.add(brand_nike)
    db.session.add(brand_adidas)
    db.session.commit()

''' Add data Product to database '''







if __name__ == '__main__':
    app.run(debug=True)