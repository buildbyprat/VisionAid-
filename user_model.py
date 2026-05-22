from datetime import datetime
from bson import ObjectId

class User:
    collection = "users"

    @staticmethod
    def schema():
        return {
            "email": str,
            "password_hash": str,
            "name": str,
            "clinic_name": str,
            "role": str,
            "created_at": datetime,
            "updated_at": datetime
        }

    @staticmethod
    def to_dict(doc):
        if not doc:
            return None
        return {
            "id": str(doc.get("_id")),
            "email": doc.get("email"),
            "name": doc.get("name"),
            "clinic_name": doc.get("clinic_name"),
            "role": doc.get("role", "doctor"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at")
        }
