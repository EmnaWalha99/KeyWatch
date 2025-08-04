def extract_sender_info(data):
    try:
        ext_info = data.get("extSenderInfo", {})
        email = ext_info.get("email", "")
        name = ext_info.get("name", "")
        return {
            "email": email,
            "has_email": int(bool(email)),
            "name": name,
            "has_name": int(bool(name))
        }
    except Exception as e:
        print("[ERROR] Sender information extraction failed:", e)
        return {
            "email": "unknown",
            "has_email": 0,
            "name": "unknown",
            "has_name": 0
        }
