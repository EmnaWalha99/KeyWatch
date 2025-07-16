from dataAccess.amount_stats import get_avg_amount_last_7d
from config.db import get_transactions_collection
def extract_pan_info(data):
        try:
            pan = data.get("extSenderInfo", {}).get("pan", "")
            bin_code = pan[:6] if len(pan) >= 6 else None
            return {
                "pan" : pan,
                "bin": bin_code
            }
        except Exception as e:
            print("[ERROR] PAN extraction failed:", e)
            return {
                "pan": None , 
                "bin": None
            }
def extract_amount(data):
        amount = data.get('amount',0)
        
        return {
            'amount'  : amount , 
        }

def extract_avg_amount_last_7d(data, collection=None):
    try:
        if collection is None : 
            collection = get_transactions_collection()
        pan=data.get("extSenderInfo",{}).get("pan")
        if not pan : 
            return {"avg_amount_last_7d": None}
        avg_amount = get_avg_amount_last_7d(pan, collection=collection)
        return {"avg_amount_last_7d":avg_amount}
    except Exception as e : 
        print("[ERROR] Avg amount extraction failed:", e)
        return {"avg_amount_last_7d": None}

def extract_fee_rate(data):
        try:
            fee_rate = data.get("feeRate", None)
            return {
                "fee_rate": fee_rate
            }
        except Exception as e:
            print("[ERROR] Fee rate extraction failed:", e)
            return {
                "fee_rate": None
            }
