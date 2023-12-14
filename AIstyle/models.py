from AIstyle import db
from sqlalchemy import func,DateTime,ForeignKey
from sqlalchemy.orm import relationship


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(200),nullable=False)
    Description = db.Column(db.String(1000))
    Product = relationship('Product',backref='Brand', lazy=True)

    def __init__(self,name,description):
        self.Name = name
        self.Description = description
    

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(200),nullable=False)
    OriginalPrice = db.Column(db.Float,nullable=False)
    ScrapedAt = db.Column(DateTime,nullable=False)
    BrandId = db.Column(db.Integer,ForeignKey(Brand.id), nullable=False)
    ProductDetail = relationship('ProductDetail', backref='Product',lazy=True)
    Order = relationship('Order',backref='Product', lazy=True)
    ResultBox = relationship('ResultBox', backref='Product', lazy=True)

    def __init__(self,name,original_price,scraped_at,brand_id):
        self.Name = name
        self.OriginalPrice = original_price
        self.ScrapedAt = scraped_at
        self.BrandId = brand_id


class ProductDetail(db.Model):
    __tablename__ = 'product_detail'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Description = db.Column(db.String(2000),nullable=False)
    Price = db.Column(db.Float, nullable=False)
    ScrapedAt = db.Column(DateTime, nullable=False)
    Color = db.Column(db.String(100))
    Availability = db.Column(db.String(100))
    LinkImage = db.Column(db.String(1000), nullable=False)
    AvgRating = db.Column(db.Float)
    ReviewCount = db.Column(db.Integer)
    ProductUrl = db.Column(db.String(1000),nullable=False)
    Sale = db.Column(db.String(100))
    ProductId = db.Column(db.Integer,ForeignKey(Product.id),nullable=False)

    def __init__(self,description,price,scraped_at,color,
                 availability,link_image,avg_rating,
                 review_count,product_url,sale,product_id): 
        self.Description = description
        self.Price = price
        self.ScrapedAt = scraped_at
        self.Color = color
        self.Availability = availability
        self.LinkImage = link_image
        self.AvgRating = avg_rating
        self.ReviewCount = review_count
        self.ProductUrl = product_url
        self.Sale = sale
        self.ProductId = product_id

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    UserName = db.Column(db.String(200),nullable=False)
    Role = db.Column(db.String(200))
    CreatedAt = db.Column(DateTime,nullable=False)
    HashPassword = db.Column(db.String(1000),nullable=False)
    Order = relationship('Order',backref='User',lazy=True)

    def __init__(self,name,created,hash_password,role=None):
        self.HashPassword = hash_password
        self.CreatedAt = created
        self.UserName = name
        self.Role = role

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    OrderDate = db.Column(DateTime,nullable=False)
    Status = db.Column(db.Integer)
    Delivered = db.Column(db.Integer)
    DeliveredDate = db.Column(DateTime)
    ProductId = db.Column(db.Integer, ForeignKey(Product.id),nullable=False)
    UserId = db.Column(db.Integer, ForeignKey(User.id),nullable=False)

    def __init__(self,delivered_date,product_id,user_id,date,status=0,delivered=0):
        self.OrderDate = date
        self.ProductId = product_id
        self.Status = status
        self.Delivered = delivered
        self.DeliveredDate = delivered_date
        self.UserId = user_id


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(200))
    Box = relationship('ChatBox',backref='Chat',lazy=True)
    def __init__(self,name):
        self.Name = name

class ChatBox(db.Model):
    __tablename__ = 'chat_box'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    TextQuestion = db.Column(db.String(3000),nullable=False)
    LinkImageQuestion = db.Column(db.String(3000),nullable=False)
    ChatId = db.Column(db.Integer,ForeignKey(Chat.id),nullable=False)
    ResultBox = relationship('ResultBox',backref='ChatBox',lazy=True)

    def __init__(self,text,image,chat_id):
        self.ChatId = chat_id
        self.TextQuestion = text
        self.LinkImageQuestion = image

class ResultBox(db.Model):
    __tablename__ = 'result_box'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    TextAnswer = db.Column(db.String(3000), nullable=False)
    LinkImageAnswer = db.Column(db.String(3000), nullable=False)
    BoxId = db.Column(db.Integer,ForeignKey(ChatBox.id),nullable=False)
    ProductId = db.Column(db.Integer,ForeignKey(Product.id),nullable=False)

    def __init__(self,text_answer,link_image_answer,box_id,product_id):
        self.TextAnswer = text_answer
        self.LinkImageAnswer = link_image_answer
        self.BoxId = box_id
        self.ProductId = product_id

