import re
from datetime import datetime

def is_valid_email(email):
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email) is not None

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def sanitize_patient_id(pid):
    return re.sub(r"[^a-zA-Z0-9\-]", "", pid)
