from config.db import get_transactions_collection

async def find_last_transaction_with_pan(transaction: dict , collection=None)-> dict | None:
    if collection is None : 
        collection = get_transactions_collection()
    pan = transaction.get("extSenderInfo",{}).get("pan")
    
    if not pan: 
        return None 
    return await collection.find_one(
        {"extSenderInfo.pan": pan},
        sort= [("createdAt", -1)],
        projection={"_id": 0} #to exclude the id
        
    )
