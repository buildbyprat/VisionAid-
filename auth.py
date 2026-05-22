from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from app.database import get_db
from app.models.user_model import User
from app.utils.helpers import is_valid_email
from app.utils.error_handler import APIError
from app.utils.logger import setup_logger
from datetime import datetime

auth_bp = Blueprint("auth", __name__)
logger = setup_logger("auth")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    name = data.get("name", "").strip()
    clinic_name = data.get("clinic_name", "").strip()

    if not email or not password or not name:
        raise APIError("Email, password and name are required", 400)

    if not is_valid_email(email):
        raise APIError("Invalid email format", 400)

    if len(password) < 6:
        raise APIError("Password must be at least 6 characters", 400)

    db = get_db()
    if db.users.find_one({"email": email}):
        raise APIError("Email already registered", 409)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user_doc = {
        "email": email,
        "password_hash": password_hash,
        "name": name,
        "clinic_name": clinic_name,
        "role": "doctor",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    logger.info("New user registered: %s", email)

    access_token = create_access_token(identity=str(result.inserted_id))

    return jsonify({
        "success": True,
        "token": access_token,
        "user": User.to_dict(user_doc)
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        raise APIError("Email and password are required", 400)

    db = get_db()
    user = db.users.find_one({"email": email})

    if not user:
        raise APIError("Invalid credentials", 401)

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        raise APIError("Invalid credentials", 401)

    access_token = create_access_token(identity=str(user["_id"]))

    logger.info("User logged in: %s", email)

    return jsonify({
        "success": True,
        "token": access_token,
        "user": User.to_dict(user)
    }), 200
