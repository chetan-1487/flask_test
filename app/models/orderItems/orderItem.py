from app.extension import db
import uuid


class OrderItem(db.Model):
  __tablename__="orderitem"

  id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
  order_id = db.Column(db.String(100), db.ForeignKey("order.id"))
  product_id = db.Column(db.String(100), db.ForeignKey("product.id"))



  def __init__(self, user_id, total_amount):
    self.user_id=user_id
    self.total_amount=total_amount
  
