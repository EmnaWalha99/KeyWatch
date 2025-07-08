from dataAccess.counting_transactions import get_distinct_counts , get_velocity_counts
from config.db import get_transactions_collection
from extractors.extract_sender_info import extract_sender_info
from extractors.extract_location_info import extract_ip_info , extract_country
from extractors.extract_time_info import extract_day , extract_late_hour
from extractors.extract_card_and_payment_info import extract_pan_info , extract_amount , extract_fee_rate
from extractors.extract_status import extract_status
from extractors.extract_merchant_domain import extract_merchant_domain
class FeatureExtractor:
    def __init__(self):
        pass
    
    def extract_features(self, trnx_data):
        
        features ={}
        features.update(extract_sender_info(trnx_data))
        features.update(extract_ip_info(trnx_data))   
        #amount
        features.update(extract_amount(trnx_data))
        features.update(extract_merchant_domain(trnx_data))

        features.update(extract_late_hour(trnx_data))
        features.update(extract_day(trnx_data))
        features.update(extract_status(trnx_data))
        features.update(extract_country(trnx_data))
        features.update(extract_fee_rate(trnx_data))
        features.update(extract_pan_info(trnx_data))
        
        collection = get_transactions_collection()
        features.update(get_velocity_counts(trnx_data,collection=collection))
        features.update(get_distinct_counts(trnx_data))
        return features
"""    
    def _extract_amount(self,data):
        amount = data.get('amount',0)
        
        return {
            'amount'  : amount , 
            'big_amount': 1 if amount > 1000000 else 0
        }

    def _extract_late_hour(self, data):
        try:
            utc_paid_at = data.get("paidAt", {}).get("$date", None)
            tz = data.get("senderIpInformation", {}).get("timezone", "UTC")

            print(f"[DEBUG] Raw paidAt: {utc_paid_at}")
            print(f"[DEBUG] Timezone: {tz}")

            if not utc_paid_at:
                raise ValueError("paidAt['$date'] is missing")

            dt_utc = isoparse(utc_paid_at).replace(tzinfo=timezone.utc)
            print(f"[DEBUG] UTC datetime: {dt_utc}")

            # Fallback to UTC if timezone is invalid
            try:
                dt_local = dt_utc.astimezone(ZoneInfo(tz))
            except Exception as tz_err:
                print(f"[WARN] Invalid timezone '{tz}', using UTC. Error: {tz_err}")
                dt_local = dt_utc

            print(f"[DEBUG] Local datetime: {dt_local}")

            hour = dt_local.hour
            return {
                "local_hour": hour,
                "is_late_night": 1 if 1 <= hour <= 5 else 0
            }

        except Exception as e:
            print("[ERROR] Late hour extraction failed:", e)
            return {
                "local_hour": None,
                "is_late_night": 0
            }
            
    def _extract_day(self, data):
        try:
            utc_paid_at = data.get("paidAt", {}).get("$date", None)
            if not utc_paid_at:
                raise ValueError("paidAt['$date'] is missing")
            dt_utc = isoparse(utc_paid_at).replace(tzinfo=timezone.utc)
            day_of_week = dt_utc.weekday()  # 0=lundi, 6=dimanche
            is_weekend = 1 if day_of_week >= 5 else 0  # 5=samedi, 6=dimanche
            return {
                "day_of_week": day_of_week,
                "is_weekend": is_weekend
            }
        except Exception as e:
            print("[ERROR] Day extraction failed:", e)
            return {
                "day_of_week": None,
                "is_weekend": 0
            }
            
    
    
    def _extract_country(self, data):
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
      
    def _extract_merchant_domain(self, data):
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
    
    def _extract_ip_info(self, data):
        try:
            ip_info = data.get("senderIpInformation", {})
            is_mobile = 1 if ip_info.get("mobile", False) else 0
            is_proxy= 1 if ip_info.get("proxy", False) else 0
            senderIP = data.get("senderIP")
            #is_vpn = 1 if ip_info.get("vpn", False) else 0
            return {
                "senderIP" : senderIP,
                "is_mobile": is_mobile,
                "is_proxy": is_proxy
            }
        except Exception as e:
            print("[ERROR] IP information extraction failed:", e)
            return {
                #"ip_address": "unknown",
                "isp": "unknown",
                "is_mobile": "unknown"
                
            }  
            
            
    
    def _extract_sender_info(self, data):
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
    def _extract_fee_rate(self, data):
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
            """
    


            
           
                
            