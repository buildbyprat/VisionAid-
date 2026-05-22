from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import get_db
from app.services.hash_service import generate_hash
from app.services.stellar_service import stellar_service
from app.services.report_service import build_report_payload, serialize_for_hash
from app.models.proof_model import Proof
from app.utils.error_handler import APIError
from app.utils.logger import setup_logger
from datetime import datetime
from bson.objectid import ObjectId

blockchain_bp = Blueprint("blockchain", __name__)
logger = setup_logger("blockchain")

@blockchain_bp.route("/generate-proof", methods=["POST"])
@jwt_required()
def generate_proof():
    data = request.get_json() or {}
    doctor_id = get_jwt_identity()

    report_id = data.get("report_id")
    patient_id = data.get("patient_id")
    diagnosis = data.get("diagnosis")
    confidence = data.get("confidence")
    severity = data.get("severity")
    recommendation = data.get("recommendation")

    if not report_id or not patient_id:
        raise APIError("report_id and patient_id are required", 400)

    payload = build_report_payload(patient_id, diagnosis, confidence, severity, recommendation)
    serialized = serialize_for_hash(payload)
    hash_value = generate_hash(serialized)

    try:
        stellar_result = stellar_service.anchor_hash(hash_value)
    except Exception as e:
        logger.error("Stellar anchoring failed: %s", e)
        raise APIError("Blockchain transaction failed", 502)

    proof_doc = {
        "report_id": report_id,
        "doctor_id": doctor_id,
        "hash": hash_value,
        "tx_id": stellar_result["tx_id"],
        "memo": stellar_result["memo"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "anchored",
        "network": stellar_result["network"],
        "created_at": datetime.utcnow()
    }

    db = get_db()
    db.proofs.insert_one(proof_doc)

    db.reports.update_one(
        {"_id": ObjectId(report_id)},
        {"$set": {"hash": hash_value, "tx_id": stellar_result["tx_id"], "updated_at": datetime.utcnow()}}
    )

    logger.info("Proof generated: tx=%s report=%s", stellar_result["tx_id"], report_id)

    return jsonify({
        "success": True,
        "hash": hash_value,
        "tx_id": stellar_result["tx_id"],
        "timestamp": proof_doc["timestamp"],
        "network": stellar_result["network"]
    }), 201

@blockchain_bp.route("/verify-proof", methods=["POST"])
def verify_proof():
    data = request.get_json() or {}

    tx_id = data.get("tx_id")
    report = data.get("report")

    if not tx_id or not report:
        raise APIError("tx_id and report payload are required", 400)

    serialized = serialize_for_hash(report)
    expected_hash = generate_hash(serialized)

    try:
        memo_valid = stellar_service.verify_memo(tx_id, expected_hash)
    except Exception as e:
        logger.error("Verification fetch failed: %s", e)
        raise APIError("Unable to verify on blockchain", 502)

    status = "valid" if memo_valid else "invalid"

    logger.info("Proof verification for %s: %s", tx_id, status)

    return jsonify({
        "success": True,
        "status": status,
        "valid": memo_valid,
        "tx_id": tx_id,
        "expected_hash": expected_hash
    }), 200
