from datetime import datetime, timedelta , timezone
import uuid
import random
from pprint import pprint
from config.db import get_transactions_collection
from extractors.feature_extractor import FeatureExtractor

collection = get_transactions_collection()
extractor = FeatureExtractor(collection)

# simulate country mismatch 
def simulate_country_mismatch():
    transaction = {
       "createdAt": datetime.now(timezone.utc),
        "paidAt": datetime.now(timezone.utc),
        "amount": 1500,
        "extSenderInfo": {
            "pan": "400000**0000",
            "paymentSystem": "VISA",
            "bankInfo": {"bankCountryName": "France"},
        },
        "senderIP": "41.226.5.10",
        "senderIpInformation": {
            "country": "Tunisia",
            "timezone": "Africa/Tunis",
            "proxy": False
        } 
    }
    transaction["_id"]=uuid.uuid4().hex
    collection.insert_one(transaction)
    features = extractor.extract_features(transaction)
    print("Country Mismatch:")
    pprint(features)
    
    
if __name__=="__main__":
    simulate_country_mismatch()
    