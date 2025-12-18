from app.extension import db
from flask import Blueprint, jsonify
from app.models.orderItems import OrderItem
from flask.wrappers import Response

orderitems_bp=Blueprint("orderitem",__name__)

@orderitems_bp.route("/all")
def all() -> Response:
  order_item = OrderItem.query.all()
  return jsonify({"message":"hello in orderItems","data":{
    "data":order_item
  }})