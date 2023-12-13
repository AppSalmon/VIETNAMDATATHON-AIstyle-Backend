from AIstyle import db
from sqlalchemy import func,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(100))
    product = relationship('product',backref='brand',lazy=True)

    def __init__(self,name,description):
        self.name = name
        self.description = description
    

class product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    original_price = db.Column(db.Integer,nullable=False)
    scraped_at = db.Column(DateTime,nullable=False)
    brand_id = db.Column(db.Integer,ForeignKey(brand.id), nullable=False)
    product_detail = relationship('product_detail',backref='product',lazy=True)
    order = relationship('order',backref='product', lazy=True)
    result_box = relationship('result_box',backref='product', lazy=True)

    def __init__(self,name,original_price,scraped_at,brand_id):
        self.name = name
        self.original_price = original_price
        self.scraped_at = scraped_at
        self.brand_id = brand_id

class product_detail(db.Model):
    __tablename__ = 'product_detail'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    description = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    scraped_at = db.Column(DateTime, nullable=False)
    color = db.Column(db.String(30))
    availability = db.Column(db.String(30))
    link_image = db.Column(db.String(100), nullable=False)
    avg_rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    product_url = db.Column(db.String(100),nullable=False)
    sale = db.Column(db.String(30))
    product_id = db.Column(db.Integer,ForeignKey(product.id),nullable=False)

    def __init__(self,description,price,scraped_at,color,
                 availability,link_image,avg_rating,
                 review_count,product_url,sale,product_id): 
        self.description = description
        self.price = price
        self.scraped_at = scraped_at
        self.color = color
        self.availability = availability
        self.link_image = link_image
        self.avg_rating = avg_rating
        self.review_count = review_count
        self.product_url = product_url
        self.sale = sale
        self.product_id = product_id

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(30),nullable=False)
    role = db.Column(db.String(100))
    created_at = db.Column(DateTime,nullable=False)
    hash_password = db.Column(db.String(20),nullable=False)
    order = relationship('order',backref='user',lazy=True)

    def __init__(self,name,created,hash_password,role=None):
        self.name = name
        self.role = role
        self.created_at = created
        self.hash_password = hash_password

class order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    order_date = db.Column(DateTime,nullable=False)
    status = db.Column(db.Integer)
    delivered = db.Column(db.Integer)
    delivered_date = db.Column(DateTime)
    product_id = db.Column(db.Integer, ForeignKey(product.id),nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(user.id),nullable=False)

    def __init__(self,delivered_date,product_id,user_id,date,status=0,delivered=0):
        self.order_date = date
        self.status = status
        self.delivered = delivered
        self.delivered_date = delivered_date
        self.product_id = product_id
        self.user_id = user_id

class chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(30))
    box = relationship('chat_box',backref='chat',lazy=True)
    def __init__(self,name):
        self.name = name

class chat_box(db.Model):
    __tablename__ = 'chat_box'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    text_question = db.Column(db.String(100),nullable=False)
    link_image_question = db.Column(db.String(100),nullable=False)
    chat_id = db.Column(db.Integer,ForeignKey(chat.id),nullable=False)
    result_box = relationship('result_chat',backref='chat_box',lazy=True)

    def __init__(self,text,image,chat_id):
        self.text = text
        self.image = image
        self.chat_id = chat_id

class result_box(db.Model):
    __tablename__ = 'result_box'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    text_answer = db.Column(db.String(100), nullable=False)
    link_image_answer = db.Column(db.String(100), nullable=False)
    box_id = db.Column(db.Integer,ForeignKey(chat_box.id),nullable=False)
    product_id = db.Column(db.Integer,ForeignKey(product.id),nullable=False)

    def __init__(self,text_answer,link_image_answer,box_id,product_id):
        self.text_answer = text_answer
        self.link_image_answer = link_image_answer
        self.box_id = box_id
        self.product_id = product_id








