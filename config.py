import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/visionaid")

    STELLAR_SECRET_KEY = os.getenv("STELLAR_SECRET_KEY", "")
    STELLAR_PUBLIC_KEY = os.getenv("STELLAR_PUBLIC_KEY", "")
    HASH_SALT = os.getenv("HASH_SALT", "visionaid-default-salt")

    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = os.getenv("FLASK_ENV") == "development"
