from datetime import datetime

class Report:
    collection = "reports"

    @staticmethod
    def to_dict(doc):
        if not doc:
            return None
        return {
            "id": str(doc.get("_id")),
            "patient_id": doc.get("patient_id"),
            "doctor_id": doc.get("doctor_id"),
            "diagnosis": doc.get("diagnosis"),
            "confidence": doc.get("confidence"),
            "severity": doc.get("severity"),
            "recommendation": doc.get("recommendation"),
            "heatmap_url": doc.get("heatmap_url"),
            "original_url": doc.get("original_url"),
            "hash": doc.get("hash"),
            "tx_id": doc.get("tx_id"),
            "timestamp": doc.get("timestamp"),
            "created_at": doc.get("created_at"),
            "status": doc.get("status", "completed")
        }
