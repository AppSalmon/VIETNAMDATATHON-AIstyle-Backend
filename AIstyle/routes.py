from flask import Blueprint, render_template, flash, request, jsonify, session
from flask_login import current_user, login_required
import json
from AIstyle.models import *
from AIstyle import db
from flask import jsonify
from flask_cors import cross_origin
from datetime import datetime
import threading


routes = Blueprint("routes", __name__)
#Trả về danh sách giá để vẽ biểu đồ giá
@routes.route("/chart/<int:product_id>", methods=["GET"])
@cross_origin()
def get_price(product_id: int):
    list_sale_price =  list(map(lambda x: x.Price ,ProductDetail.query.filter_by(ProductId = product_id).all()))
    product =  Product.query.filter_by(id = product_id).first()
    name = product.Name
    original_price = product.OriginalPrice
    get_price = {"ProductId": product_id,
                 'Name': name,
                 'OriginalPrice': original_price,
                 'Price': list_sale_price
        }
    return jsonify(get_price)
#Trả về list sp đang sale của một product 
@routes.route("/recommend",methods=["GET"])
@cross_origin()
def recommend():
    product = Product.query.all()
    name = list(map(lambda x: x.Name, product))
    original_price = list(map(lambda x: x.OriginalPrice, product))
    productId = list(map(lambda x: x.id, product))
    list_product = []
    for i in range(len(productId)):
        detail = ProductDetail.query.filter_by(ProductId = productId[i]).all()
        
        list_sale_price = list(map(lambda x: x.Price,detail))
        at = list(map(lambda x: x.ScrapedAt,detail))
        index = min(range(len(at)), key=lambda i: abs(datetime.now() - at[i]))
        price = list_sale_price[index]
        list_product.append({'id':i,
                             'name':name[i],
                             'original_price':original_price[i],
                             "price":price,
                             'sale': (1 - price/original_price[i])* 100})
    get_trending = {'Product': list_product}
    list_product_sort = sorted(get_trending['Product'], key=lambda x: x['sale'], reverse=True)
    for i in range(len(list_product_sort)):
        list_product_sort[i]['key'] = i
    get_trending = {'Product': list_product_sort}
    return jsonify(get_trending)

    
#Trả về list sp top trending: /trending
@routes.route("/trending",methods=["GET"])
@cross_origin()
def trending():
    product = Product.query.all()
    product_id =  list(map(lambda x: x.id, product))
    name = list(map(lambda x: x.Name, product))
    list_product = []
    for i in range(len(product_id)):
        detail = ProductDetail.query.filter_by(ProductId = product_id[i]).all()
        rating = list(map(lambda x: x.AvgRating,detail))
        at = list(map(lambda x: x.ScrapedAt,detail))
        index = min(range(len(at)), key=lambda i: abs(datetime.now() - at[i]))
        rating = rating[index]
        list_product.append({'id': i,
                             'name': name[i],
                             'rating': rating})
    
    get_trending = {'Product': list_product}
    list_product_sort = sorted(get_trending['Product'], key=lambda x: x['rating'], reverse=True)
    for i in range(len(list_product_sort)):
        list_product_sort[i]['key'] = i
    get_trending = {'Product': list_product_sort}
    return jsonify(get_trending)


#return same products: /same-products
@routes.route("/same-products/<product_id>", methods=["GET"])
@cross_origin()
def same_product(product_id):
    pass

@routes.route("/info/<product_id>",methods = ["GET"])
@cross_origin()
def info(product_id):
    try:
        t1 = threading.Thread(target=get_price(product_id))
        t2 = threading.Thread(target=recommend)
        t3 = threading.Thread(target=trending)

        t1.start()
        t2.start()
        t1.start()

        t1.join()  # Chờ t1 hoàn thành
        t2.join()  # Chờ t2 hoàn thành
        t3.join() 

        return "GOOD"
    except:
        return "FAIL"


#click mannequin (ma nơ canh) hiện giỏ chứa hàng để design/virtual try on: /cart
@routes.route("/cart/<int:userId>",methods = ["GET"])
@cross_origin()
def cart(userId : int):
    product_id = list(map(lambda x: x.ProductID , Cart.query.filter_by(UserId=userId).all()))
    list_product = []
    for i in range(len(product_id)):
        product = Product.query.filter_by(id = product_id[i]).all()
        name = list(map(lambda x: x.Name,product))
        detail = ProductDetail.query.filter_by(ProductId = product_id[i]).all()
        price = list(map(lambda x: x.Price,detail))
        color = list(map(lambda x: x.color, detail))
        at = list(map(lambda x: x.ScrapedAt,detail))
        index = min(range(len(at)), key=lambda i: abs(datetime.now() - at[i]))
        price = price[index]
        list_product.append({'id': product_id[i],
                             'name': name,
                             "price": price,
                             'color': color})
    get_cart = {'user': userId, 'Products':list_product}    
    return jsonify(get_cart)

@routes.route("/virtualtryon",methods = ["GET"])
@cross_origin()
def virtualtryon():
    pass

#Design sản phẩm khác: /design
@routes.route("/design",methods = ["GET"])
@cross_origin()
def design():
    pass

