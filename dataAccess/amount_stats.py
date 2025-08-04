from datetime import datetime , timedelta , timezone 
from config.db import get_transactions_collection

async def get_avg_amount_last_7d(pan: str, collection=None)-> float:
    if not pan:
        return 0.0

    if collection is None:
        collection = get_transactions_collection()

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=7)

    cursor = collection.find(
        {
            "extSenderInfo.pan": pan,
            "createdAt": {"$gte": since}
        },
        {"amount": 1}
    )
        
    amounts= []

    async for doc in cursor:
        amount = doc.get("amount", 0)
        amounts.append(amount)
    
    """.explain()
    print("[DEBUG] Explain output:", cursor)
    just to test if the index is used correctly 
    """

    if not amounts:
        return 0.0

    return round(sum(amounts) / len(amounts), 2)