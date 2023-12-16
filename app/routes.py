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
from sqlalchemy import desc, asc
# from app.utils import make_response, make_data

routes = Blueprint("routes", __name__)
#Trả về danh sách giá để vẽ biểu đồ giá
@routes.route("/chart/<int:product_id>", methods=["GET"])
@cross_origin()
def get_price(product_id: int):
    productdetail = ProductDetail.query.filter_by(ProductId = product_id).all()
    mock_prices = list(map(lambda x: x.MockPrice,productdetail))[-1]
    price =   list(map(lambda x: x.Price,productdetail))[-1]
    numbers = mock_prices.split("~")
    # Convert extracted strings to float
    numbers_float = [float(num) for num in numbers]
    numbers_float.append(price)
    get_price = {
        'ProductId': product_id,
        'Price': numbers_float
    }
    return jsonify(get_price)

#Trả về list sp đang sale của một product 
@routes.route("/recommend", methods=["GET"])
@cross_origin()
def recommend():
    
    results = db.session.query(Product, ProductDetail)\
            .join(ProductDetail, Product.id == ProductDetail.ProductId)\
            .order_by(desc(Product.OriginalPrice), asc(ProductDetail.Price))\
            .limit(6)\
            .all()
    
    list_product = []
    for product, product_detail in results:
        product_id = product.id
        name = product.Name
        original_price = product.OriginalPrice
        product_detail_price = product_detail.Price
        detail_id = product_detail.id  # Giả sử detail_id là id của ProductDetail
        sale = (1 - product_detail_price/original_price)* 100

        # Truy vấn ImageLink dựa trên ProductDetailId
        list_image = ImageLink.query.filter_by(ProductDetailId=detail_id).all()
        
        list_product.append(
            {
                "product_id": product_id,
                "name": name,
                "original_price": original_price,
                "product_detail_price": product_detail_price,
                'sale': sale,
                "list_image": [image_link.Image for image_link in list_image]  # Thay thế 'some_attribute' bằng tên thuộc tính thực tế của ImageLink bạn muốn trả về
            })

    get_product = {
        'Product': list_product
    }
    return jsonify(get_product)

    
#Trả về list sp top trending: /trending
@routes.route("/trending",methods=["GET"])
@cross_origin()
def trending():
    results = db.session.query(ProductDetail)\
            .order_by(desc(ProductDetail.AvgRating), desc(ProductDetail.ReviewCount))\
            .limit(6)\
            .all()

    list_product_details = []
    for product_detail in results:
        product = Product.query.filter_by(id = product_detail.ProductId).all()
        product = product[0]
        name = product.Name
        origin_price = product.OriginalPrice
        product_id = product.id
        name = product.Name
        detailId = product_detail.id
        list_image = ImageLink.query.filter_by(ProductDetailId=detailId).all()

        list_product_details.append({
            "ProductId": product_id,
            "Price": product_detail.Price,
            "AvgRating": product_detail.AvgRating,
            "ReviewCount": product_detail.ReviewCount,
            'OriginalPrice': origin_price,
            'name': name,
            'image': [image_link.Image for image_link in list_image]
            # Thêm các thông tin khác từ product_detail mà bạn muốn lấy
        })
    get_product = {
        'Products': list_product_details
    }
    return jsonify(get_product)


# #return same products: /same-products
# @routes.route("/same-products/<product_id>", methods=["GET"])
# @cross_origin()
# def same_product(product_id):
#     pass

@routes.route("/info/<int:product_id>",methods = ["GET"])
@cross_origin()
def info(product_id:int):
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
    
    product = Product.query.filter_by(id = product_id).one()
    name = product.Name
    ori_price = product.OriginalPrice
    productdetail = ProductDetail.query.filter_by(ProductId = product_id).all()
    productdetail = productdetail[-1]
    description = productdetail.Description
    color = productdetail.Color
    avgRating = productdetail.AvgRating
    reviewCount = productdetail.ReviewCount
    mock_prices = productdetail.MockPrice
    price =   productdetail.Price
    numbers = mock_prices.split("~")
    numbers_float = [float(num) for num in numbers]
    numbers_float.append(price)
    productdetail_id = productdetail.id
    list_image = ImageLink.query.filter_by(ProductDetailId=productdetail_id).all()
    get_product = {
        "ProductId": product_id,
        'Name': name,
        'OriginalPrice': ori_price,
        'Price': numbers_float,
        'ReviewCount': reviewCount,
        'Color': color,
        'Description': description,
        'AvgRating': avgRating,
        'ReviewCount': reviewCount,
        'Image': [image_link.Image for image_link in list_image]
    }
    return jsonify(get_product)
    


@routes.route("/virtualtryon",methods = ["GET"])
@cross_origin()
def virtualtryon():
    pass

#Design sản phẩm khác: /design
@routes.route("/design",methods = ["GET"])
@cross_origin()
def design():
    pass

