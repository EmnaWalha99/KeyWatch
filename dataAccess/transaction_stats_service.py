from datetime import datetime, timedelta , timezone

class TransactionStatsService:
    def __init__(self, db):
        self.collection = db.get_transactions_collection()
    
    def find_last_transaction_with_pan(self , transaction):
        pan = transaction.get("extSenderInfor",{}).get("pan")
        
        if not pan : 
            return None
        
        last_trx = self.collection.find_one(
            {
            "extSenderInfo.pan":pan 
            },
            sort=[("createdAt",-1)]
                                    )
        return last_trx
    def get_avg_amount_last_7d(self ,pan):
        if not pan: 
            return 0
        now = datetime.now(timezone.utc)
        since = now -timedelta(days=7)
        cursor = self.collection.find(
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





