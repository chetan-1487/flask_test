from flask import Blueprint, jsonify, request, make_response
from app.utils import is_password_valid, is_username_valid
from app.image_func import save_image
from app.models.users import User
from app.models.roles import Role
from app.extension import db, bcrypt
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps
from flask.wrappers import Response
from uuid import UUID

user_bp = Blueprint("users", __name__)


def user_role(*roles):
  def wrapper(func):
    @wraps(func)
    def decorator(*args, **kwargs):
      try:
        verify_jwt_in_request()
      except Exception:
        return jsonify({"error": "Token missing or invalid"}), 401

      claim = get_jwt()
      role = claim.get("roles")
      if not any(r in role for r in roles):
        resp = make_response(jsonify({"error":"Access denied. only admin and manager can take action"}))
        return resp

      return func(*args, **kwargs)
    return decorator
  return wrapper
    



@user_bp.route("/create", methods=["POST"])
def create() -> Response:

  first_name = request.form.get("first_name")
  last_name = request.form.get("last_name")
  username = request.form.get("username")
  email = request.form.get("email")
  password = request.form.get("password")
  status = request.form.get("status")
  role = request.form.get("role")
  profile_image = request.files.get("profile_image_url")

  
  if User.query.filter_by(email=email).first():
    return jsonify({"error": "Email already exists"}), 409


  if not is_username_valid(username):
    return jsonify({"error":"username must be alphanumeric."})
  
  if not is_password_valid(password):
    return jsonify({"error":"password must have one uppercase, one lowercase, one digit, special character and length at least 8."})
  
  pass_hash = bcrypt.generate_password_hash(password).decode("utf-8")
  
  image_url = save_image(profile_image) if profile_image else None

  user_details = User(first_name, last_name, username, email, pass_hash, status, image_url)
  role_details = Role(role, "default role")

  user_details.role.append(role_details)


  db.session.add(user_details)
  db.session.commit()

  return jsonify({"message":"user registration successfully", "users":{
    "name" : f"{first_name} {last_name}",
    "username": username,
    "email":email,
    "status":status,
    "profile_image_url":image_url
  }}), 201


@user_bp.route("/login", methods=["POST"])
def login() -> Response:
  email = request.form.get("email")
  password = request.form.get("password")

  user = User.query.filter_by(email=email).first()

  if not user:
    return jsonify({"error":"user doesnot exist."}), 404

  role = Role.query.filter_by(user_id=user.id).first()
  
  if not bcrypt.check_password_hash(user.password, password):
    return jsonify({"message":"invaild email and password"}), 401
  
  token = create_access_token(identity=user.id, additional_claims={"username":user.username,"email":user.email,"roles":role.name.value})

  return jsonify({"message":"user login successfully.", "tokens":{
    "access_token":token
  }})

@user_bp.route("/change-password", methods=["PUT"])
def change_password() -> Response:
  email = request.form.get("email")
  current_password = request.form.get("current_password")
  new_password = request.form.get("new_password")
  confirm_password = request.form.get("confirm_password")

  user = User.query.filter_by(email=email).first()

  if not user:
    return jsonify({"error":"user doesnot exist."}), 404
  
  if not bcrypt.check_password_hash(user.password, current_password):
    return jsonify({"message":"invaild email and password"}), 401
  
  if new_password!=confirm_password:
    return jsonify({"error":"both new and confirm password different"})
  
  pass_hash = bcrypt.generate_password_hash(confirm_password).decode("utf-8")

  user.password = pass_hash
  db.session.commit()

  return jsonify({"message":"passoword change successfully."}), 200


@user_bp.route("/all", methods=["GET"])
def all() -> Response:
    roles = request.args.getlist("roles")   
    status = request.args.get("status")    
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 10))

    query = User.query

    if status:
        query = query.filter(User.status == status)

    if roles:
        query = query.join(User.roles).filter(Role.name.in_(roles))

    users = query.offset(page * limit).limit(limit).all()

    user_list = [
        {
            "username": u.username,
            "email": u.email,
        }
        for u in users
    ]

    return jsonify({
        "message": "all users",
        "page": page,
        "limit": limit,
        "count": len(user_list),
        "users": user_list
    }), 200


@user_bp.route("/users/<uuid:id>", methods=["GET"])
@user_role("admin", "manager")
def users(id: UUID) -> Response:
  user_detail = User.query.filter_by(id=id).first()

  if not user_detail:
    return jsonify({"message":"user doesnot exist"}), 404

  return jsonify({"message":"user details", "data":{
    "username":user_detail.username,
    "email":user_detail.email,
    "roles": [r.name for r in user_detail.roles],
    "profile_image_url":user_detail.profile_image_url
  }}), 200
  

@user_bp.route("/update/users/<uuid:id>", methods=["PUT"])
@user_role("admin", "manager")
def update_users(id: UUID) -> Response:

  first_name = request.form.get("first_name")
  last_name = request.form.get("last_name")
  status = request.form.get("status")
  profile_image_url = request.files["profile_image_url"]

  user_detail = User.query.filter_by(id=id).first()

  if not user_detail:
    return jsonify({"message":"user doesnot exist"}), 404

  image_url = save_image(profile_image_url)

  obj = {
    "first_name" : first_name,
    "last_name" : last_name,
    "status" : status,
    "profile_image_url" :image_url
  }

  for key,value in obj.items():
    if hasattr(user_detail,key):
      setattr(user_detail,key,value)

  db.session.commit()

  return jsonify({"message":"successfully updated details", "data":{
    "username":user_detail.username,
    "email":user_detail.email,
    "roles":user_detail.roles,
    "profile_image_url":user_detail.profile_image_url
  }}), 200
  

@user_bp.route("/users/<uuid:id>/archive", methods=["PUT"])
@user_role("admin", "manager")

def user_archive(id: UUID) -> Response:
  user_detail = User.query.filter_by(id=id).first()

  if not user_detail:
    return jsonify({"message":"user doesnot exist"}), 404
  
  if user_detail.status=="archived":
    return jsonify({"message":"user already archived."})
  
  user_detail.status = "archived"
  db.session.commit()

  return jsonify({"message":"set status successfully"})


@user_bp.route("/users/<uuid:id>/restore", methods=["PUT"])
@user_role("admin", "manager")

def user_restore(id : UUID) -> Response:
  user_detail = User.query.filter_by(id=id).first()

  if not user_detail:
    return jsonify({"message":"user doesnot exist"}), 404
  
  if user_detail.status=="active":
    return jsonify({"message":"user already active."})
  
  user_detail.status = "active"
  db.session.commit()

  return jsonify({"message":"status set successfully"})