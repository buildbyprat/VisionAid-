from datetime import datetime

class Proof:
    collection = "proofs"

    @staticmethod
    def to_dict(doc):
        if not doc:
            return None
        return {
            "id": str(doc.get("_id")),
            "report_id": doc.get("report_id"),
            "hash": doc.get("hash"),
            "tx_id": doc.get("tx_id"),
            "memo": doc.get("memo"),
            "timestamp": doc.get("timestamp"),
            "status": doc.get("status"),
            "network": doc.get("network", "testnet"),
            "created_at": doc.get("created_at")
        }
