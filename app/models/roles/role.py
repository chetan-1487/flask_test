from app.extension import db
import uuid
from enum import Enum
from sqlalchemy import Enum as rolenum

class Roles(Enum):
  Admin = "Admin"
  Manager = "Manager"
  Viewer = "Viewer"

class Role(db.Model):

  __tablename__="role"

  id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
  name = db.Column(rolenum(Roles), nullable=False)
  description= db.Column(db.String(255), nullable=True)
  user_id = db.Column(db.String(100), db.ForeignKey("users.id"))

  def __init__(self, name, description):
    self.name=name
    self.description=description

