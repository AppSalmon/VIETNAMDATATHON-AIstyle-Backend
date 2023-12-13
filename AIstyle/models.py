from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime  # Add this import
from enum import unique
from datetime import timezone, datetime
from AIstyle import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='Category', lazy=True)

    def __str__(self):
        return self.name

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, default=0)
    image = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    create_date = db.Column(DateTime, default=datetime.now())  # Fix the data type
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name

