from app.extension import db
from flask import Blueprint, jsonify
from app.models.orders import Order
from flask.wrappers import Response

order_bp=Blueprint("orders",__name__)

@order_bp.route("/")
def hello() -> Response:
  
  order_details = Order.query.all()

  return jsonify({"message":"product data","data":{
    "product_data":order_details
  }})