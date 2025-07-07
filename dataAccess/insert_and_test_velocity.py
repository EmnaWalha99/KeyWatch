from datetime import datetime , timezone , timedelta
from config.db import get_transactions_collection
from dataAccess.counting_transactions import get_velocity_counts
trnx_collection = get_transactions_collection()

now = datetime.now(timezone.utc)

doc= []

for i in range(5): 
    doc.append({
        "createdAt": now - timedelta(minutes=i),  # à 1 minute d'intervalle
        "extSenderInfo": {
            "pan": "521265**8218",
            "email": "",
            "name": "EMNA"
            },
        "senderIP": "192.168.10.11"
        })
     
    
trnx_collection.insert_many(doc)
print("[INFO] 5 transactions inserted for velocity check testing ")

transaction = {
        "extSenderInfo": {
            "pan": "521265**8218",
            "email": "",
            "name": "EMNA"
        },
        "senderIP": "192.168.10.11"
    }

result = get_velocity_counts(transaction , now=now , collection = trnx_collection)
print("[INFO] velocity counts result : " , result)

