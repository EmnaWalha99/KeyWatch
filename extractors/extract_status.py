def extract_status(data):
        try : 
            status = data.get("status", "unknown")
            status_risk = 1 if data.get("status") in ["failed_payment", "rejected"] else 0
            failure_contains_low_balance=int("low balance" in str(data.get("details","")).lower() or "insufficient" in str(data.get("details","")).lower())
            return {
                "status": status,
                "status_failure_risk": status_risk,
                "failure_contains_low_balance": failure_contains_low_balance
            }
       
        except Exception as e :
            print("[ERROR] Status extraction failed:", e)
            return {
                "status": "unknown"
            }