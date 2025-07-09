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
def get_velocity_counts(transaction, now=None, collection=None):
    if now is None:
        now = datetime.now(timezone.utc)
    if collection is None:
        collection = get_transactions_collection()

    pan = transaction.get("extSenderInfo", {}).get("pan")
    senderIP = transaction.get("senderIP")
    email = transaction.get("extSenderInfo", {}).get("email")
    name = transaction.get("extSenderInfo", {}).get("name")

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

            query_field = {
                "pan": "extSenderInfo.pan",
                "senderIP": "senderIP",
                "email": "extSenderInfo.email",
                "name": "extSenderInfo.name"
            }[key]

            query = {
                query_field: value,
                "createdAt": {"$gte": since}
            }

            count = collection.count_documents(query)

            # 🌟 Nom plus explicite
            label_map = {
                "pan": "same_card_used",
                "senderIP": "same_ip_used",
                "email": "same_email_used",
                "name": "same_name_used"
            }
            key_label = f"{label_map[key]}_in_last_{window_minutes}m"
            flat_results[key_label] = count

    return flat_results


    
def get_distinct_counts(transaction, now=None, collection=None):
    if now is None:
        now = datetime.now(timezone.utc)
    if collection is None:
        collection = get_transactions_collection()

    field_mapping = {
        "pan": "extSenderInfo.pan",
        "senderIP": "senderIP",
        "extSenderInfo.name": "extSenderInfo.name"
    }

    flat_results = {}

    for main_field, distinct_fields in distinct_check.items():
        main_value = get_nested_value(transaction, field_mapping[main_field])
        if not main_value:
            continue

        window = default_window_minutes.get(main_field, 60)
        since = now - timedelta(minutes=window)

        for distinct_field in distinct_fields:
            query = {
                field_mapping[main_field]: main_value,
                "createdAt": {"$gte": since}
            }

            distinct_values = collection.distinct(distinct_field, query)
            count = len(distinct_values)

            readable_map = {
                ("pan", "extSenderInfo.name"): "same_card_used_by_multiple_names",
                ("pan", "senderIP"): "same_card_used_from_multiple_ips",
                ("senderIP", "extSenderInfo.pan"): "same_ip_used_by_multiple_cards",
                ("extSenderInfo.name", "extSenderInfo.pan"): "same_name_used_with_multiple_cards"
            }

            label = readable_map.get((main_field, distinct_field),
                                     f"{field_name(main_field)}_to_{field_name(distinct_field)}")

            flat_results[f"{label}_last_{window}m"] = count

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
