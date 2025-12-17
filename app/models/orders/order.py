from app.extension import db
import uuid


class Order(db.Model):
  __tablename__="order"

  id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
  user_id = db.Column(db.String(100), db.ForeignKey("users.id"))
  total_amount = db.Column(db.Integer)

  order_items = db.relationship("OrderItem", backref="order", lazy=True)

  def __init__(self, user_id, total_amount):
    self.user_id=user_id
    self.total_amount=total_amount
  
