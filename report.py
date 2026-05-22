from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import get_db
from app.models.report_model import Report
from app.utils.error_handler import APIError
from app.utils.logger import setup_logger
from bson.objectid import ObjectId

report_bp = Blueprint("report", __name__)
logger = setup_logger("report")

@report_bp.route("/reports", methods=["GET"])
@jwt_required()
def get_reports():
    doctor_id = get_jwt_identity()
    db = get_db()

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    search = request.args.get("search", "")

    query = {"doctor_id": doctor_id}
    if search:
        query["$or"] = [
            {"patient_id": {"$regex": search, "$options": "i"}},
            {"diagnosis": {"$regex": search, "$options": "i"}}
        ]

    total = db.reports.count_documents(query)
    reports = list(db.reports.find(query)
                   .skip((page - 1) * limit)
                   .limit(limit)
                   .sort("created_at", -1))

    logger.info("Fetched %d reports for doctor %s", len(reports), doctor_id)

    return jsonify({
        "success": True,
        "data": [Report.to_dict(r) for r in reports],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }), 200

@report_bp.route("/report/<id>", methods=["GET"])
@jwt_required()
def get_report(id):
    doctor_id = get_jwt_identity()
    db = get_db()

    try:
        report = db.reports.find_one({"_id": ObjectId(id), "doctor_id": doctor_id})
    except Exception:
        raise APIError("Invalid report ID", 400)

    if not report:
        raise APIError("Report not found", 404)

    return jsonify({
        "success": True,
        "data": Report.to_dict(report)
    }), 200
