from datetime import datetime, timedelta, timezone
from config.db import get_transactions_collection


#transactions_collection=get_transactions_collection()

velocity_check = { 
    "pan" : [15 , 60],
    "senderIP" : [60] , 
    "email" : [300] , 
    "name" : [300]
}
distinct_check = {
    "pan": ["extSenderInfo.name", "senderIP"],
    "senderIP": ["extSenderInfo.pan"],
    "extSenderInfo.name": ["extSenderInfo.pan"]
}
default_window_minutes = {
    "pan": 15,
    "senderIP": 60,
    "extSenderInfo.name": 300
}
def get_velocity_counts(transaction , now=None, collection=None):
    if now is None:
        now = datetime.now(timezone.utc)
    if collection is None :
        collection = get_transactions_collection()
    pan = transaction.get("extSenderInfo", {}).get("pan", None)
    senderIP = transaction.get("senderIP", None)
    email = transaction.get("extSenderInfo", {}).get("email", None)
    name = transaction.get("extSenderInfo", {}).get("name", None)
    
    
    velocity_check = {  # i need to delte this later ! 
    "pan" : [15 , 60],
    "senderIP" : [60] , 
    "email" : [300] , 
    "name" : [300]
}
    key_values = {
        "pan": pan,
        "senderIP": senderIP,
        "email": email,
        "name": name
    }
    flat_results = {}
    
    for key, windows in velocity_check.items():
        value = key_values.get(key)
        if not value:
            continue

        for window_minutes in windows:
            since = now - timedelta(minutes=window_minutes)
        
            if key == "pan":
                query = {
                    "extSenderInfo.pan": value,
                    "createdAt": {"$gte": since}
                }
            elif key == "senderIP":
                query = {
                    "senderIP": value,
                    "createdAt": {"$gte": since}
                }
            elif key == "email":
                query = {
                    "extSenderInfo.email": value,
                    "createdAt": {"$gte": since}
                }
            elif key == "name":
                query = {
                    "extSenderInfo.name": value,
                    "createdAt": {"$gte": since}
                }
            else:
                continue

            #print(f"[DEBUG] Query for {key} ({window_minutes}m): {query}")
            count = collection.count_documents(query)
            flat_results[f"{key}_{window_minutes}m_velocity"]=count
            #print(f"[DEBUG] Count : {count}")
            #results[key][f"{window_minutes}m"] = count
    
    return flat_results

    
def get_distinct_counts(transaction , now=None , collection=None):
    distinct_check = {
    "pan": ["extSenderInfo.name", "senderIP"],
    "senderIP": ["extSenderInfo.pan"],
    "extSenderInfo.name": ["extSenderInfo.pan"]
}
    default_window_minutes = {
    "pan": 15,
    "senderIP": 60,
    "extSenderInfo.name": 300
}
    if now is None :
        now = datetime.now(timezone.utc)
    if collection is None:
        collection = get_transactions_collection()
  
    field_mapping = {
        "pan" : "extSenderInfo.pan",
        "senderIP":"senderIP",
        "extSenderInfo.name":"extSenderInfo.name"
    }
    flat_results={}
    
    for main_field, distinct_fields in distinct_check.items() : 
        mapped_field = field_mapping.get(main_field,main_field)
        main_value = get_nested_value(transaction , mapped_field)
        if not main_value:
            continue
        
        window = default_window_minutes.get(main_field, 60)
        since = now - timedelta(minutes=window)

        for distinct_field in distinct_fields:
            query = {
                mapped_field: main_value,
                "createdAt": {"$gte": since}
            }
            count = len(collection.distinct(distinct_field, query))
            key = f"{field_name(main_field)}_distinct_{field_name(distinct_field)}_{window}m"
            flat_results[key] = count

    return flat_results
        
def get_nested_value(dct , dotted_key):
    keys = dotted_key.split('.')
    for key in keys:
        if isinstance(dct, dict) and key in dct:
            dct = dct[key]
        else:
            return None
    return dct

def field_name(dotted_key):
    return dotted_key.replace(".","_")
