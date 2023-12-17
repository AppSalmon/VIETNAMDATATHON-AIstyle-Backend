from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re


# from AIstyle import *
from app.models import (
    Brand,
    Product,
    ProductDetail,
    User,
    Order,
    Chat,
    ChatBox,
    ResultBox,
    ImageLink
)
from app import db, create_app


load_dotenv(dotenv_path = "./app/.env")

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
user_postgreSQL = os.environ.get("user_postgreSQL")
password_postgreSQL = os.environ.get("password_postgreSQL")

app = create_app(remove=True)

''' Import data '''
import pandas as pd
df_crawl = pd.read_csv("VIETNAMDATATHON-AIstyle-Backend\Process_data\data.csv")
# df_btc = pd.read_csv("VIETNAMDATATHON-AIstyle-Backend\Process_data\data_btc.csv")
df = pd.read_csv("VIETNAMDATATHON-AIstyle-Backend\Process_data\data_2.csv")


''' Add data brand to database '''
brand_nike = Brand(name = "Nike", description = "Nike, Inc. is a globally renowned American multinational corporation that is engaged in the design, development, manufacturing, and marketing of footwear, apparel, equipment, accessories, and services. The company is one of the world's largest and most recognizable athletic and sportswear brands, and it has established itself as a symbol of innovation, performance, and style.")
brand_adidas = Brand(name = "Adidas", description = "Adidas is a multinational corporation that is widely recognized for its presence in the sportswear and athletic footwear industry. The company was founded on August 18, 1949, by Adolf Dassler in Herzogenaurach, Germany. The name Adidas is a combination of the founder's nickname, Adi, and the first three letters of his last name.")

with app.app_context():
    db.session.add(brand_nike)
    db.session.add(brand_adidas)
    db.session.commit()

'''Add data PRoduct to database'''

productId = 0
for index, row in df.iterrows():
    productId = index + 1
    if row['brand'] != 'adidas':
        new_product = Product(
            name= row['name'],
            original_price= row['original_price'],
            scraped_at= datetime.strptime(row['scraped_at'], '%Y-%m-%d %H:%M:%S'),
            key_image = row['key_image'],
            brand_id= 1
        )
        with app.app_context():
            db.session.add(new_product)
            db.session.commit()

        product_detail = ProductDetail(
            description= row['description'],
            avg_rating= row['avg_rating'],
            price= row['price'],
            mock_prices= row['mock_prices'],
            scraped_at= row['scraped_at'],
            color= row['color'],
            availability= row['availability'],
            review_count= row['review_count'],
            product_url= row['url'],
            sale= 0,
            product_id= productId 
        )
        with app.app_context():
            db.session.add(product_detail)
            db.session.commit()
        link = row['images'][2:-2]
        image = ImageLink(
            image= link,
            product_detail_id= productId 
        )
        with app.app_context():
            db.session.add(image)
            db.session.commit()
    else:
        new_product = Product(
            name= row['name'],
            original_price= row['original_price'],
            scraped_at= row['scraped_at'],
            key_image = row['key_image'],
            brand_id= 2
        )
        with app.app_context():
            db.session.add(new_product)
            db.session.commit()

        product_detail = ProductDetail(
            description= row['description'],
            avg_rating= row['avg_rating'],
            price= row['price'],
            mock_prices= row['mock_prices'],
            scraped_at= row['scraped_at'],
            color= row['color'],
            availability= row['availability'],
            review_count= row['review_count'],
            product_url= row['url'],
            sale= 0,
            product_id= productId 
        )
        with app.app_context():
            db.session.add(product_detail)
            db.session.commit()

        links = re.findall(r'https://\S+\.jpg', row['images'])
        for link in links:
            image = ImageLink(
                image= link,
                product_detail_id= productId 
            )
            with app.app_context():
                db.session.add(image)
                db.session.commit()
productId2 = 0
for index, row in df_crawl.iterrows():
    try:
        productId2 = productId + index + 1
        if row['brand'] != 'adidas':
            new_product = Product(
                name= row['name'],
                original_price= row['original_price'],
                scraped_at= row['scraped_at'],
                key_image = None,
                brand_id= 1
            )
            with app.app_context():
                db.session.add(new_product)
                db.session.commit()
            product_detail = ProductDetail(
                description= row['description'],
                avg_rating= row['avg_rating'],
                price= row['price'],
                mock_prices= row['mock_prices'],
                scraped_at= row['scraped_at'],
                color= row['color'],
                availability= row['availability'],
                review_count= row['review_count'],
                product_url= row['url'],
                sale= 0,
                product_id= productId2
            )
            with app.app_context():
                db.session.add(product_detail)
                db.session.commit()
            link = row['images'][2:-2]
            image = ImageLink(
                image= link,
                product_detail_id= productId 
            )
            with app.app_context():
                db.session.add(image)
                db.session.commit()
        else:
            new_product = Product(
                name= row['name'],
                original_price= row['original_price'],
                scraped_at= row['scraped_at'],
                key_image = None,
                brand_id= 2
            )
            with app.app_context():
                db.session.add(new_product)
                db.session.commit()

            product_detail = ProductDetail(
                description= row['description'],
                avg_rating= row['avg_rating'],
                price= row['price'],
                mock_prices= row['mock_prices'],
                scraped_at= row['scraped_at'],
                color= row['color'],
                availability= row['availability'],
                review_count= row['review_count'],
                product_url= row['url'],
                sale= 0,
                product_id= productId2 
            )
            with app.app_context():
                db.session.add(product_detail)
                db.session.commit()

            links = re.findall(r'https://\S+\.jpg', row['images'])
            for link in links:
                image = ImageLink(
                    image= link,
                    product_detail_id= productId 
                )
                with app.app_context():
                    db.session.add(image)
                    db.session.commit()
    except:
        pass

