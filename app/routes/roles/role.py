from flask import Blueprint, jsonify
from app.models.roles import Role
import os
from dotenv import load_dotenv
from app.extension import db
from flask.wrappers import Response
from uuid import UUID

load_dotenv()

role_bp = Blueprint("roles", __name__)


@role_bp.route("/all")
def all() -> Response:

  pagiation = int(os.getenv("pagination"), 10)

  query= Role.query
  query=query.offset(pagiation)

  result = query.all()

  order = [
    {
      "name":e.name,
      "decription":e.description
    }
    for e in result
  ]

  return jsonify({"message":"all order details","data":{
    "order":order
  }}), 200


@role_bp.route("/roles/<id>", methods=["DELETE"])
def delete_role(id: str) -> Response:
  role = Role.query.filter_by(id==id).first()

  if role.user_id:
    return jsonify({"message":"user already assigned"})
  
  db.session.delete(role)
  db.session.commit()

  return jsonify({"message":"role deleted successfully."})