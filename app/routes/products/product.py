from app.extension import db
from flask import Blueprint, jsonify
from app.models.products import Product

product_bp=Blueprint("products",__name__)

@product_bp.route("/")
def hello():

  products_details = Product.query.all()

  return jsonify({"message":"product data","data":{
    "product_data":products_details
  }})