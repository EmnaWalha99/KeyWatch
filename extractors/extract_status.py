from dataAccess.count_failed_attemps import count_failed_attempts
def extract_status(data):
        try : 
            status = data.get("status", "unknown")
            status_risk = 1 if data.get("status") in ["failed_payment", "blocked",] else 0
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
            
async def extract_many_failed_attempts(data):
    try:
        number =  await count_failed_attempts(data)
        #print("number of failed attemps : ", number)
        if number is not None and number > 3 : 
            return {
                "number_of_failed_attempts" : number , 
                "many_failed_attempts" : 1
            }
        else : 
            return{
                "many_failed_attempts" : 0
            }
                    
    except Exception as e : 
        print(f"[ERROR] during extracting failed attempts: {e}") 
        return {
            "many_failed_attempts" : None
        }