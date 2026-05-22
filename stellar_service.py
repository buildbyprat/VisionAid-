import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Payment
from stellar_sdk.exceptions import BadRequestError, ConnectionError
from app.config import Config
from app.utils.logger import setup_logger
import requests

logger = setup_logger("stellar_service")

HORIZON_URL = "https://horizon-testnet.stellar.org"
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE

class StellarService:
    def __init__(self):
        self.server = Server(horizon_url=HORIZON_URL)
        self.keypair = None
        self.public_key = Config.STELLAR_PUBLIC_KEY

        if Config.STELLAR_SECRET_KEY:
            try:
                self.keypair = Keypair.from_secret(Config.STELLAR_SECRET_KEY)
                self.public_key = self.keypair.public_key
            except Exception as e:
                logger.error("Invalid Stellar secret key: %s", e)

    def fund_account(self, public_key: str):
        try:
            resp = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
            if resp.status_code == 200:
                logger.info("Account funded via Friendbot: %s", public_key)
                return True
            else:
                logger.warning("Friendbot funding response: %s", resp.text)
                return False
        except Exception as e:
            logger.error("Friendbot funding failed: %s", e)
            return False

    def ensure_funded(self):
        if not self.public_key:
            logger.error("No public key configured")
            return False
        try:
            self.server.load_account(self.public_key)
            return True
        except Exception:
            logger.info("Account not found, attempting funding...")
            return self.fund_account(self.public_key)

    def anchor_hash(self, hash_value: str) -> dict:
        if not self.keypair:
            raise RuntimeError("Stellar keypair not configured")

        self.ensure_funded()

        try:
            source_account = self.server.load_account(self.public_key)
            memo_text = hash_value[:28] if len(hash_value) > 28 else hash_value

            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    network_passphrase=NETWORK_PASSPHRASE,
                    base_fee=self.server.fetch_base_fee()
                )
                .add_text_memo(memo_text)
                .append_payment_op(
                    destination=self.public_key,
                    amount="0.0000001",
                    asset_code="XLM"
                )
                .set_timeout(30)
                .build()
            )

            transaction.sign(self.keypair)
            response = self.server.submit_transaction(transaction)

            tx_id = response["hash"]
            logger.info("Transaction submitted: %s", tx_id)

            return {
                "tx_id": tx_id,
                "status": response.get("successful", True),
                "memo": memo_text,
                "network": "testnet"
            }
        except BadRequestError as e:
            logger.error("Stellar BadRequest: %s", e)
            raise
        except ConnectionError as e:
            logger.error("Stellar ConnectionError: %s", e)
            raise
        except Exception as e:
            logger.error("Stellar transaction failed: %s", e)
            raise

    def fetch_transaction(self, tx_id: str) -> dict:
        try:
            tx = self.server.transactions().transaction(tx_id).call()
            logger.info("Fetched transaction: %s", tx_id)
            return tx
        except Exception as e:
            logger.error("Failed to fetch transaction %s: %s", tx_id, e)
            raise

    def verify_memo(self, tx_id: str, expected_hash: str) -> bool:
        tx = self.fetch_transaction(tx_id)
        memo = tx.get("memo", "")
        is_valid = expected_hash.startswith(memo) or memo == expected_hash
        logger.info("Memo verification for %s: %s", tx_id, is_valid)
        return is_valid

stellar_service = StellarService()
