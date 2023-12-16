from flask import Blueprint, render_template, flash, request, jsonify, session
from flask_login import current_user, login_required
import json
from app.models import *
from app import db
from flask import jsonify
from flask_cors import cross_origin
from datetime import datetime
import threading
import re
from sqlalchemy.orm import joinedload
# from app.utils import make_response, make_data

routes = Blueprint("routes", __name__)
#Trả về danh sách giá để vẽ biểu đồ giá
@routes.route("/chart/<int:product_id>", methods=["GET"])
@cross_origin()
def get_price(product_id: int):
    list_sale_price =  list(map(lambda x: x.Price ,ProductDetail.query.filter_by(ProductId = product_id).all()))
    list_sale_price = list_sale_price[0].split("~")
    list_sale_price = [float(num) for num in list_sale_price]
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
@routes.route("/recommend", methods=["GET"])
@cross_origin()
def recommend():
    product = Product.query.all()
    name = list(map(lambda x: x.Name, product))
    original_price = list(map(lambda x: x.OriginalPrice, product))
    productId = list(map(lambda x: x.id, product))
    list_product = []
    for i in range(len(productId)):
        detail = ProductDetail.query.filter_by(ProductId = productId[i]).all()
        detail_id = list(map(lambda x: x.id, detail))
        list_sale_price = list(map(lambda x: x.Price,detail))
        at = list(map(lambda x: x.ScrapedAt,detail))
        index = min(range(len(at)), key=lambda i: abs(datetime.now() - at[i]))
        list_sale_price = list_sale_price[index]
        numbers = list_sale_price.split("~")
        # Convert extracted strings to float
        numbers_float = [float(num) for num in numbers]
        price = numbers_float[-1]
        list_image = []
        for j in range(len(detail_id)):
            images = list(map(lambda x: x.Image, ImageLink.query.filter_by(ProductDetailId=detail_id[j])))
            list_image.append(images)
        list_product.append({'id':i,
                                'name':name[i],
                                'original_price':original_price[i],
                                "price":price,
                                'sale': (1 - price/original_price[i])* 100,
                                'list_image': list_image})
    get_trending = {'Product': list_product}
    list_product_sort = sorted(get_trending['Product'], key=lambda x: x['sale'], reverse=True)[:50]
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
        detail_id = list(map(lambda x: x.id, detail))
        rating = list(map(lambda x: x.AvgRating,detail))
        reviewCount = list(map(lambda x: x.ReviewCount,detail))
        list_sale_price = list(map(lambda x: x.Price,detail))
        at = list(map(lambda x: x.ScrapedAt,detail))
        index = min(range(len(at)), key=lambda i: abs(datetime.now() - at[i]))
        rating = rating[index]
        reviewCount = reviewCount[index]
        list_sale_price = list_sale_price[index]
        numbers = list_sale_price.split("~")
        # Convert extracted strings to float
        numbers_float = [float(num) for num in numbers]
        price = numbers_float[-1]
        list_image = []
        for j in range(len(detail_id)):
            images = list(map(lambda x: x.Image, ImageLink.query.filter_by(ProductDetailId=detail_id[j])))
            list_image.append(images)
        list_product.append({'id': i,
                             'name': name[i],
                             'rating': rating,
                             'review_count': reviewCount,
                             'price': price,
                             'list_image': list_image})
    
    get_trending = {'Product': list_product}
    list_product_sort = sorted(get_trending['Product'], key=lambda x: (x['rating'], x['review_count']), reverse=True)
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
# @routes.route("/cart/<int:userId>",methods = ["GET"])
# @cross_origin()
# def cart(userId : int):
#     product_id = list(map(lambda x: x.ProductID , Cart.query.filter_by(UserId=userId).all()))
#     list_product = []
#     for i in range(len(product_id)):
#         product = Product.query.filter_by(id = product_id[i]).all()
#         name = list(map(lambda x: x.Name,product))
#         detail = ProductDetail.query.filter_by(ProductId = product_id[i]).all()
#         price = list(map(lambda x: x.Price,detail))
#         color = list(map(lambda x: x.color, detail))
#         at = list(map(lambda x: x.ScrapedAt,detail))
#         index = min(range(len(at)), key=lambda i: abs(datetime.now() - at[i]))
#         price = price[index]
#         list_product.append({'id': product_id[i],
#                              'name': name,
#                              "price": price,
#                              'color': color})
#     get_cart = {'user': userId, 'Products':list_product}    
#     return jsonify(get_cart)

@routes.route('/product/<int:product_id>', methods = ['GET'])
@cross_origin()
def getproduct(product_id: int):
    try:
        product = Product.query.filter_by(id = product_id).all()
        product = product[-1]
        name = product.Name
        ori_price = product.OriginalPrice
        detail = ProductDetail.query.filter_by(ProductId = product_id).all()
        description = list(map(lambda x: x.Description,detail))
        color = list(map(lambda x: x.Color,detail))
        avgRating = list(map(lambda x: x.AvgRating,detail))
        reviewCount = list(map(lambda x: x.ReviewCount,detail))
        price = list(map(lambda x: x.Price,detail))
        numbers = price[-1].split("~")
        numbers_float = [float(num) for num in numbers]
        detail_id = list(map(lambda x: x.id, detail))
        list_image = []
        for j in range(len(detail_id)):
            images = list(map(lambda x: x.Image, ImageLink.query.filter_by(ProductDetailId=detail_id[j])))
            list_image.append(images)
        get_product = {
            "ProductId": product_id,
            'Name': name,
            'OriginalPrice': ori_price,
            'Price': numbers_float,
            'reviewCount': reviewCount,
            'color': color,
            'description': description,
            'avgRating': avgRating,
            'reviewCount': reviewCount,
            'image': list_image
        }
        return jsonify(get_product)
    except:
        return 'Fail'


@routes.route("/virtualtryon",methods = ["GET"])
@cross_origin()
def virtualtryon():
    pass

#Design sản phẩm khác: /design
@routes.route("/design",methods = ["GET"])
@cross_origin()
def design():
    pass

