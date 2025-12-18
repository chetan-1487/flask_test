from flask import Flask
from app.routes.users import user_bp
from app.routes.roles import role_bp
from app.routes.orders import order_bp
from app.routes.products import product_bp
from app.routes.orderItems import orderitems_bp
from app.extension import db, migrate, jwtmanager
from app.config import Config
from dotenv import load_dotenv
import os

load_dotenv()


def createApp(testing=False) -> Flask:
  app = Flask(__name__)

  app.config.from_object(Config)

  if testing:
    app.config["SQLALCHEMY_DATABASE_URI"]= os.getenv("TESTING_DATABASE_URI")

  db.init_app(app)
  migrate.init_app(app,db)
  jwtmanager.init_app(app)

  app.register_blueprint(user_bp, url_prefix="/users")
  app.register_blueprint(role_bp, url_prefix="/roles")
  app.register_blueprint(order_bp, url_prefix="/orders")
  app.register_blueprint(product_bp, url_prefix="/products")
  app.register_blueprint(orderitems_bp, url_prefix="/orderitems")

  return app


if __name__=="__main__":
  app = createApp()
  app.run(debug=True)