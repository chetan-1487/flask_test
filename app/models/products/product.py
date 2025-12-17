from app.extension import db
import uuid


class Product(db.Model):
  __tablename__="product"
  
  id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
  name = db.Column(db.String(100))
  description = db.Column(db.String(255))
  price = db.Column(db.Integer)
  status = db.Column(db.Boolean)

  orderitem = db.relationship("OrderItem", backref="product")

  def __init__(self, name, description, price, status):
    self.name=name
    self.description=description
    self.price=price
    self.status=status

