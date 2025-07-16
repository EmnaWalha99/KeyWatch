from config.db import get_logs_collection  
from datetime import datetime, timezone

def log_transaction(transaction: dict, features: dict, fraud_result: dict):
    logs_collection = get_logs_collection()
    log_entry = {
        "transaction": transaction,
        "features": features,
        "fraud_result": fraud_result,
        "logged_at": datetime.now(timezone.utc)
    }
    logs_collection.insert_one(log_entry)
