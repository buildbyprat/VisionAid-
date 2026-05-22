from flask import Blueprint, request, jsonify
from app.database import get_db
from app.services.hash_service import generate_hash, verify_hash
from app.services.stellar_service import stellar_service
from app.utils.error_handler import APIError
from app.utils.logger import setup_logger

verify_bp = Blueprint("verify", __name__)
logger = setup_logger("verify")

@verify_bp.route("/verify", methods=["POST"])
def verify():
    data = request.get_json() or {}

    report_id = data.get("report_id")
    tx_id = data.get("tx_id")

    if not report_id and not tx_id:
        raise APIError("report_id or tx_id is required", 400)

    db = get_db()

    query = {}
    if report_id:
        query["report_id"] = report_id
    if tx_id:
        query["tx_id"] = tx_id

    proof = db.proofs.find_one(query)

    if not proof:
        logger.warning("Verification failed: no proof found for %s", report_id or tx_id)
        return jsonify({
            "success": True,
            "valid": False,
            "status": "invalid",
            "message": "No proof record found"
        }), 200

    report_payload = data.get("report")
    if report_payload:
        from app.services.report_service import serialize_for_hash
        serialized = serialize_for_hash(report_payload)
        expected_hash = generate_hash(serialized)

        try:
            memo_valid = stellar_service.verify_memo(proof["tx_id"], expected_hash)
            hash_valid = verify_hash(serialized, proof["hash"])
            is_valid = memo_valid and hash_valid
        except Exception as e:
            logger.error("Blockchain verification error: %s", e)
            is_valid = False

        status = "verified" if is_valid else "failed"
    else:
        is_valid = True
        status = "verified"

    logger.info("Verification result for %s: %s", report_id or tx_id, status)

    return jsonify({
        "success": True,
        "valid": is_valid,
        "status": status,
        "proof": {
            "tx_id": proof.get("tx_id"),
            "hash": proof.get("hash"),
            "timestamp": proof.get("timestamp"),
            "network": proof.get("network", "testnet")
        }
    }), 200
