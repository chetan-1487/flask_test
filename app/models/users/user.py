from app.extension import db
import uuid
from datetime import datetime


class User(db.Model):
  __tablename__="users"

  id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  status = db.Column(db.String(50), default="active")
  profile_image_url = db.Column(db.String(100), nullable=True)

  createdAt = db.Column(db.DateTime(), default = datetime.now())
  updatedAt = db.Column(db.DateTime(), default = datetime.now(), onupdate=datetime.now())

  order = db.relationship("Order", backref="user", lazy=True)
  role = db.relationship("Role", backref="user", lazy=True)


  def __init__(self, first_name, last_name, username, email, password, status, profile_image_url):
    self.first_name=first_name
    self.last_name=last_name
    self.username=username
    self.email=email
    self.password=password
    self.status=status
    self.profile_image_url=profile_image_url

  def __repr__(self):
    return f"username --> {self.username}"
