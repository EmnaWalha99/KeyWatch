
def extract_merchant_domain(data):
        try:
            merchant_domain = data.get("requestOrigin", "")
            return {
                "merchant_domain": merchant_domain.split("//")[-1].split("/")[0]
            }
        except Exception as e:
            print("[ERROR] Merchant domain extraction failed:", e)
            return {
                "merchant_domain": "unknown"
            }