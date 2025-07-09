from dataAccess.find_last_trnx import find_last_transaction_with_pan
from config.db import get_transactions_collection
import math
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
            
def haversine(coord1 , coord2): # calculating distance between two coordinates 
    lon1 , lat1 = coord1
    lon2 , lat2 = coord2
    R = 6371 # le rayonn de la terre en KM
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2-lat1)
    dlambda = math.radians(lon2 -lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def extract_country_mismatch(data):
    try: 
        ip_country = data.get("senderIpInformation",{}).get("country","unknown")
        bank_country_name = data.get("extSenderInfo",{}).get("bankInfo" ,{}).get("bankCountryName","unknown")
        country_mismatch = int(ip_country.lower() != bank_country_name.lower()and ip_country !="unknown" and bank_country_name!="unknown")
        return {
            "ip_country_and_bank_country_mismatch": country_mismatch
        }
    except Exception as e: 
        print("[ERROR] Country extraction failed:", e)
        return {
            "ip_country_and_bank_country_mismatch" : "unknown"
        }
       
def extract_impossible_travel(data):
    try:
        current_location = data.get("senderIpLocation", {}).get("coordinates")
        current_time = data.get("createdAt")
        collection = get_transactions_collection()
        last_trx = find_last_transaction_with_pan(data,collection)
        if not last_trx:
            return {"impossible_travel": 0}

        last_location = last_trx.get("senderIpLocation", {}).get("coordinates")
        last_time = last_trx.get("createdAt")  # Fixed typo: should be "createdAt"

        if not (last_location and last_time and current_location and current_time):
            return {"impossible_travel": 0}

        distance = haversine(current_location, last_location)
        # Ensure both times are datetime objects
        if hasattr(current_time, "timestamp") and hasattr(last_time, "timestamp"):
            time_difference_hours = (current_time - last_time).total_seconds() / 3600.0
        else:
            return {"impossible_travel": 0}

        if time_difference_hours == 0:
            return {"impossible_travel": 0}

        speed = distance / time_difference_hours
        impossible = int(speed > 1000)  # Threshold: 1000 km/h

        return {
            "impossible_travel": impossible,
            "time_difference_with_last_trnx_h": time_difference_hours,
            "travel_distance_km": distance,
            "travel_speed_kmh": speed
        }
    except Exception as e:
        print("[ERROR] error occurred during extracting impossible travel feature:", e)
        return {
            "impossible_travel": "unknown"
        }
        
    
    
def extract_frequent_timezone_switch(data , collection=None , n=3 , threshold=2) : 
    if collection is None :
        from config.db import get_transactions_collection
        collection = get_transactions_collection()
    pan = data.get("extSenderInfo", {}).get("pan")
    if not pan : 
        return {"frequent_timezone_switch": 0 , "unique_timezones":0}
    cursor = collection.find(
        {"extSenderInfo.pan": pan, "senderIpInformation.timezone": {"$exists": True}},
        sort=[("createdAt", -1)],
        limit=n
    )
    timezones = set()
    for trnx in cursor:
        tz = trnx .get("senderIPInformation", {}).get("timezone")
        if tz:
            timezones.add(tz)
    return {
        "frequent_timezone_switch": int(len(timezones)>= threshold),
        "unique_timezones" : len(timezones)
    }
        