from pymongo import MongoClient
from config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME

def get_mongo_client():
    
    try:
        client = MongoClient(MONGO_URI)
        print("[INFO] Successfully connected to MongoDB")
        return client
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        return None

def get_transactions_collection():
    try :
        collection= get_mongo_client()[DB_NAME][COLLECTION_NAME]
        print(f"[INFO] Successfully accessed collection '{COLLECTION_NAME}' in database '{DB_NAME}'")
        return collection
    except Exception as e:
        print(f"[ERROR] Failed to get transactions collection: {e}")
        return None
        