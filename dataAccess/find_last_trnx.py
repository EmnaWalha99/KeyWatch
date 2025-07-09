from config.db import get_transactions_collection

def find_last_transaction_with_pan(transaction , collection):
    if collection is None : 
        collection = get_transactions_collection()
    pan = transaction.get("extSenderInfor",{}).get("pan")
    
    last_trx = collection.find_one(
        {
        "extSenderInfo.pan":pan 
        },
        sort=[("createdAt",-1)]
                                   )
    if not last_trx :
        return {"first_trnx" : 1}
    
    return last_trx
