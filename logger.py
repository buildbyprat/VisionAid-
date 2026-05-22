import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name="visionaid"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        log_dir = os.path.join(os.path.dirname(__file__), "../../blockchain/proof_logs")
        os.makedirs(log_dir, exist_ok=True)
        fh = RotatingFileHandler(
            os.path.join(log_dir, "app.log"),
            maxBytes=5*1024*1024,
            backupCount=3
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
