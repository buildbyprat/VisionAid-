from datetime import datetime
from app.utils.logger import setup_logger
import json

logger = setup_logger("report_service")

def build_report_payload(patient_id: str, diagnosis: str, confidence: float, 
                         severity: str, recommendation: str, timestamp: str = None) -> dict:
    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + "Z"

    payload = {
        "patient_id": patient_id,
        "diagnosis": diagnosis,
        "confidence": confidence,
        "severity": severity,
        "recommendation": recommendation,
        "timestamp": timestamp,
        "version": "1.0"
    }

    logger.info("Report payload built for patient: %s", patient_id)
    return payload

def serialize_for_hash(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
