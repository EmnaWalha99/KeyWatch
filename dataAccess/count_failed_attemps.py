from datetime import datetime,timedelta,timezone
import re
from config.db import get_transactions_collection
from utils.cache_utils import cache_or_fetch

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

async def count_failed_attemps_cache(transaction, collection=None, time_windows_minutes=1):
    pan = transaction.get("extSenderInfo", {}).get("pan")
    if not pan:
        return 0
    key = f"failed_attemps:{pan}:{time_windows_minutes}m"
    return await cache_or_fetch(key, count_failed_attempts, 120 , transaction, collection, time_windows_minutes)