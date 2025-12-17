from app.extension import db
from flask import Blueprint, jsonify
from app.models.orderItems import OrderItem

orderitems_bp=Blueprint("orderitem",__name__)

@orderitems_bp.route("/all")
def all():
  order_item = OrderItem.query.all()
  return jsonify({"message":"hello in orderItems","data":{
    "data":order_item
  }})