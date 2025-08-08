import json
import requests
import time 
from config.db import get_transactions_collection

def clean(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if isinstance(v, dict) and "$oid" in v:
                new_obj[k] = v["$oid"]
            else:
                new_obj[k] = clean(v)
        return new_obj
    elif isinstance(obj, list):
        return [clean(item) for item in obj]
    else:
        return obj


with open('fourth_batch.json', 'r') as f:
    raw_data=json.load(f)

processed_transactions = clean(raw_data)

url ='http://localhost:8000/apply-rules'
headers= {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
suspicious =[]
transaction_collection=get_transactions_collection()
with open("suspicious_log.txt","a") as log_file :
    for k, transaction in enumerate(processed_transactions):
        print(f"sending transaction {k+1}")
        response = requests.post(url, headers=headers , json=transaction)
        if response.status_code == 200 :
            response_data = response.json()
            fraud_result = response_data.get("fraud_result", {})
            fraud_risk = fraud_result.get("fraud_risk", "low")
            transaction_cleaned = transaction.copy()
            transaction_cleaned.pop('_id', None)  # Remove existing _id if any
            transaction_collection.insert_one(transaction_cleaned)

            if fraud_risk != "low":
                    print(f" Suspicious transaction {k+1}")
                    risk = fraud_result.get("fraud_risk", "unknown")
                    reasons = fraud_result.get("reasons", [])
                    log_file.write(f"Transaction {k+1} {transaction}: fraud_risk={risk}, reason={reasons}\n")
                    log_file.flush()
        else:
            print(f"failed{response.status_code}")
        
        time.sleep(0.2)
    
"""with open("suspicious_log.txt",'w') as f :
    for idx, item in enumerate(suspicious):
        tx = item["transaction"]
        result = item["fraud_result"]
        risk = result.get("fraud_risk", "unknown")
        reasons = result.get("reasons", [])
        f.write(f"Transaction {idx+1}: fraud_risk={risk}, reason={reasons}\n")

    print("Summary written to suspicious_log.txt")    
"""