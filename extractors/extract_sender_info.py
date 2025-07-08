
def extract_sender_info(data):
        try:
           email=data.get("extSenderInfo",{}).get("email","")
           has_email=1 if email else 0
           name=data.get("extSenderInfo",{}).get("name","")
           has_name=1 if name else 0
           return {
               "email": email,
               "has_email": has_email,
               "name": name,
               "has_name": has_name
           }
        except Exception as e:
            print("[ERROR] Sender information extraction failed:", e)
            return {
                "email": "unknown",
                #"has_email": 0,
                "name": "unknown"
                #"has_name": 0
            }
    