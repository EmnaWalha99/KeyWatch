from datetime import datetime , timedelta , timezone 
from config.db import get_transactions_collection

def get_avg_amount_last_7d(pan , collection=None):
    if not pan: 
        return 0
    if collection is None : 
        collection = get_transactions_collection()
    now = datetime.now(timezone.utc)
    since = now -timedelta(days=7)
    cursor = collection.find(
        {
            "extSenderInfo.pan" : pan , 
            "createdAt" : {"$gte" : since}
        },
        {"amount" : 1}
    )
    amounts = [doc.get("amount" , 0) for doc in cursor if doc.get("amount") is not None]
    if not amounts : 
        return 0 
    return sum(amounts)/len(amounts)

