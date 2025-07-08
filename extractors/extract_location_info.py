def extract_ip_info(data):
        try:
            ip_info = data.get("senderIpInformation", {})
            ip_location = data.get("senderIpLocation",{})
            #is_mobile = 1 if ip_info.get("mobile", False) else 0
            #is_proxy= 1 if ip_info.get("proxy", False) else 0
            #senderIP = data.get("senderIP")
            #is_vpn = 1 if ip_info.get("vpn", False) else 0
            return {
                "senderIP" : data.get("senderIP","unknown"),
                "ip_country" : ip_info.get("country","unknown"),
                "ip_countryCode":ip_info.get("countryCode","unknown"),
                "ip_region": ip_info.get("region","unknown"),
                "ip_regionName": ip_info.get("regionName","unknown"),
                "ip_city": ip_info.get("city","unknown"),
                "ip_zip": ip_info.get("zip","unknown"),
                "ip_lat": ip_info.get("lat","unknown"),
                "ip_lon": ip_info.get("lon","unknown"),
                "ip_timezone": ip_info.get("timezone","unknown"),
                "ip_currency": ip_info.get("currency","unknown"),
                "ip_isp": ip_info.get("isp","unknown"),
                "ip_org": ip_info.get("org","unknown"),
                "ip_as": ip_info.get("as","unknown"),
                "is_mobile": int(ip_info.get("mobile", False)),
                "is_proxy": int(ip_info.get("proxy", False)),
                "is_hosting": int(ip_info.get("hosting", False)),
                "ip_location_type": ip_location.get("type","unknown"),
                "ip_location_coordinates": ip_location.get("coordinates","unknown"),
                "ip_location_updatedAt": (
                    ip_location.get("updatedAt", {}).get("$date","unknown")
                    if isinstance(ip_location.get("updatedAt","unknown"), dict)
                    else ip_location.get("updatedAt","unknown")
                ),
                
                
            }
        except Exception as e:
            print("[ERROR] IP information extraction failed:", e)
            return {
                #"ip_address": "unknown",
                #"isp": "unknown",
                #"is_mobile": "unknown"
                
            }
            
def extract_country(data):
        try:
            ip_country =data.get("senderIpInformation", {}).get("country", "unknown")
            txn_country = data.get("extSenderInfo", {}).get("bankInfo", {}).get("bankCountryName", "unknown")
            country_mismatch = int(ip_country.lower() != txn_country.lower() and ip_country != "unknown" and txn_country != "unknown")
            bank_country_code = data.get("extSenderInfo", {}).get("bankInfo", {}).get("bankCountryCode", "unknown")
            
            return {
                "ip_country": ip_country,
                "txn_country": txn_country,
                "bank_country_code": bank_country_code,
                "country_mismatch": country_mismatch
            }
        except Exception as e:
            print("[ERROR] Country extraction failed:", e)
            return {
                "country": "unknown" ,
                "txn_country": "unknown"
            }  
            