from datetime import datetime, timezone, timedelta
from config.db import get_transactions_collection
from dataAccess.counting_transactions import get_distinct_counts

trnx_collection = get_transactions_collection()
now = datetime.now(timezone.utc)

# Insert mock transactions for distinct count testing
docs = [
    {
        "createdAt": now,
        "extSenderInfo": {"pan": "1111", "name": "EMNA"},
        "senderIP": "1.1.1.1"
    },
    {
        "createdAt": now,
        "extSenderInfo": {"pan": "1111", "name": "ARIJ"},
        "senderIP": "2.2.2.2"
    },
    {
        "createdAt": now,
        "extSenderInfo": {"pan": "1111", "name": "ABIR"},
        "senderIP": "3.3.3.3"
    },
    {
        "createdAt": now,
        "extSenderInfo": {"pan": "1234", "name": "HACKER"},
        "senderIP": "1.1.1.1"
    },
    {
        "createdAt": now,
        "extSenderInfo": {"pan": "5678", "name": "HACKER"},
        "senderIP": "1.1.1.1"
    },
    {
        "createdAt": now,
        "extSenderInfo": {"pan": "1234", "name": "HACKER"},
        "senderIP": "4.4.4.4"
    }
]

trnx_collection.insert_many(docs)
print("[INFO] Transactions inserted for distinct count testing.")

# Example transaction to test distinct counts for PAN
transaction = {
    "extSenderInfo": {"pan": "1111", "name": "EMNA"},
    "senderIP": "1.1.1.1"
}

result = get_distinct_counts(transaction, now=now, collection=trnx_collection)
print("[INFO] distinct counts result:", result)