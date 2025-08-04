from datetime import datetime,timedelta,timezone
import re
from config.db import get_transactions_collection

async def count_failed_attempts(transaction , collection=None,time_window_minutes=1):
    status = transaction.get("status","")
    if status == "failed_payment" or re.search(r"\bfailed\b",status , re.IGNORECASE) :
        if collection is None :
            collection = get_transactions_collection()
        pan = transaction.get("extSenderInfo", {}).get("pan")
        if not pan :
            return 0
        now = datetime.now(timezone.utc)
    
        time_threshold = now - timedelta(minutes= time_window_minutes)
        
        
        number_of_failed_attempts = await collection.count_documents({
            "extSenderInfo.pan":pan , 
            "status" : "failed_payment",
            "createdAt":{"$gte": time_threshold}  
        })
        
        return number_of_failed_attempts
    return 0 