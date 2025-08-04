from datetime import datetime, timedelta, timezone
from config.db import get_transactions_collection
import os 
import yaml


def load_config(path="config/velocity_config.yaml"):
    with open(path,"r") as f :
        return yaml.safe_load(f)
    

config= load_config()


async def get_velocity_counts(transaction, now=None, collection=None):
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

    for key, windows in config["velocity_check"].items():
        value = key_values.get(key)
        if not value:
            continue

        for window_minutes in windows:
            since = now - timedelta(minutes=window_minutes)
            query_field=config["field_mapping"][key]
        
            

            query = {
                query_field: value,
                "createdAt": {"$gte": since}
            }

            count = await collection.count_documents(query)

            
            label_map=config["label_map"]
            key_label = f"{label_map[key]}_in_last_{window_minutes}m"
            flat_results[key_label] = count

    return flat_results


    
async def get_distinct_counts(transaction, now=None, collection=None):
    if now is None:
        now = datetime.now(timezone.utc)
    if collection is None:
        collection = get_transactions_collection()

    flat_results = {}

    for main_field, distinct_fields in config["distinct_check"].items():
        main_value = get_nested_value(transaction, config["field_mapping"][main_field])
        if not main_value:
            continue

        window = config["default_window_minutes"].get(main_field, 60)
        since = now - timedelta(minutes=window)

        for distinct_field in distinct_fields:
            query = {
                config["field_mapping"][main_field]: main_value,
                "createdAt": {"$gte": since}
            }

            distinct_values = await collection.distinct(distinct_field, query)
            count = len(distinct_values)

            readable_key = f"{main_field}__{distinct_field}"
            label = config["readable_map"].get(
                readable_key,
                f"{field_name(main_field)}_to_{field_name(distinct_field)}"
            )

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
