from flask import request, jsonify
from app.utils.error_handler import APIError
from app.utils.logger import setup_logger

logger = setup_logger("upload_controller")

def handle_upload():
    if "file" not in request.files:
        raise APIError("No file provided", 400)

    file = request.files["file"]
    if file.filename == "":
        raise APIError("Empty filename", 400)

    logger.info("Upload received: %s", file.filename)

    return jsonify({
        "success": True,
        "message": "Upload received. AI processing handled separately.",
        "filename": file.filename,
        "status": "pending_ai"
    }), 200
