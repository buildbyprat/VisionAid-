import hashlib
import hmac
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger("hash_service")

def generate_hash(payload: str) -> str:
    salt = Config.HASH_SALT.encode("utf-8")
    payload_bytes = payload.encode("utf-8")
    hash_value = hmac.new(salt, payload_bytes, hashlib.sha256).hexdigest()
    logger.info("Hash generated for payload length %d", len(payload))
    return hash_value

def verify_hash(payload: str, expected_hash: str) -> bool:
    regenerated = generate_hash(payload)
    is_valid = hmac.compare_digest(regenerated, expected_hash)
    logger.info("Hash verification result: %s", is_valid)
    return is_valid
