import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
  SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
  SQLALCHEMY_TRACK_MODIFICATION=os.getenv("SQLALCHEMY_TRACK_MODIFICATION")
  SECRET_KEY = os.getenv("SECRET_KEY")
  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
  JWT_ALGO = os.getenv("JWT_ALGO")
  JWT_LOCATION = os.getenv("JWT_LOCATION")
  JWT_ACCESS_TOKEN_EXPIRE = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE", 15)))