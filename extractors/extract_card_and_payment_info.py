def extract_pan_info(data):
        try:
            pan = data.get("extSenderInfo", {}).get("pan", "")
            bin_code = pan[:6] if len(pan) >= 6 else None
            return {
                "bin": bin_code
            }
        except Exception as e:
            print("[ERROR] PAN extraction failed:", e)
            return {
                "bin": None
            }
def extract_amount(data):
        amount = data.get('amount',0)
        
        return {
            'amount'  : amount , 
            'big_amount': 1 if amount > 1000000 else 0
        }


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