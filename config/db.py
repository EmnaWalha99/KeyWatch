#from pymongo import MongoClient
#from config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME  , LOGS_COLLECTION

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI= "mongodb://localhost:27017"
MONGO_DB_NAME= "fraud-detection"

client = AsyncIOMotorClient(MONGO_URI)
db= client[MONGO_DB_NAME]

def get_transactions_collection():
    try:
        return db["transactions"]
    except Exception as e:
        print(f"[ERROR] Failed to get transactions collection: {e}")
        return None

def get_logs_collection():
    try:
        return db["logs"]
    except Exception as e:
        return db["logs"]


"""
_client = None
def get_mongo_client():
    global _client
    if _client is None:
        try:
            _client = MongoClient(MONGO_URI)
            print("[INFO] Successfully connected to MongoDB")
        except Exception as e:
            print(f"[ERROR] Failed to connect to MongoDB: {e}")
    return _client

def get_transactions_collection():
    try :
        return get_mongo_client()[DB_NAME][COLLECTION_NAME]
    except Exception as e:
        print(f"[ERROR] Failed to get transactions collection: {e}")
        return None
        
def get_logs_collection():
    try : 
        return get_mongo_client()[DB_NAME][LOGS_COLLECTION]
    except Exception as e : 
        print(f"[ERROR] Failed to get logs collection: {e}")
        return None
    
"""