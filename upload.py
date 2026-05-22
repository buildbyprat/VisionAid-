"""
Upload / Analyze Blueprint
POST /api/analyze  – accepts an image, returns AI diagnosis JSON.
"""

from flask import Blueprint, request, jsonify
from app.services.ai_service import predict_retina

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts a multipart/form-data POST with field 'image'.
    Returns JSON: {"diagnosis": str, "confidence": float}
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided. Use field name 'image'."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    try:
        result = predict_retina(file)
        return jsonify(result), 200

    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500

    except Exception as exc:
        return jsonify({"error": "Unexpected server error.", "detail": str(exc)}), 500
