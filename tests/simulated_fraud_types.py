from datetime import datetime, timedelta , timezone
import uuid
import random
from pprint import pprint
from config.db import get_transactions_collection
from extractors.feature_extractor import FeatureExtractor
from rules.rule_engine import RuleEngine
collection = get_transactions_collection()
extractor = FeatureExtractor(collection)
rule_engine=RuleEngine(rules_path="rules/rules.yaml")
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
    print("Country Mismatch:",features["ip_country_and_bank_country_mismatch"])
    
    
def simulate_timezone_switch(pan="421000**0001"):
    base_time = datetime.now(timezone.utc)
    timezones = ["Asia/Tokyo", "America/New_York", "Europe/Paris", "Africa/Tunis"]

    for i, tz in enumerate(timezones[:3]):
        transaction = {
            "_id": uuid.uuid4().hex,
            "createdAt": base_time - timedelta(days=i),
            "paidAt": base_time - timedelta(days=i),
            "amount": 600,
            "extSenderInfo": {"pan": pan},
            "senderIP": f"192.168.1.{i+10}",
            "senderIpInformation": {
                "country": "Unknown", "proxy": False, "timezone": tz
            }
        }
        collection.insert_one(transaction)

    features = extractor.extract_features(transaction)
    print("Frequent Timezone Switching:")
    pprint(features)
    
def simulate_velocity_attack(pan="411111**1111"):
    base_time = datetime.now(timezone.utc)
    for i in range(5):
        transaction = {
            "_id": uuid.uuid4().hex,
            "createdAt": base_time - timedelta(minutes=2 * i),
            "paidAt": base_time - timedelta(minutes=2 * i),
            "amount": 500,
            "extSenderInfo": {"pan": pan, "name": "BOT USER"},
            "senderIP": "41.226.5.10",
            "senderIpInformation": {"country": "Tunisia", "proxy": False}
        }
        collection.insert_one(transaction)

    features = extractor.extract_features(transaction)
    result = rule_engine.evaluate(features=features)
    print("Velocity Attack:")
    #pprint(features)
    pprint(result)

def simulate_proxy_ip():
    transaction = {
        "createdAt": datetime.now(timezone.utc),
        "paidAt": datetime.now(timezone.utc),
        "amount": 100,
        "extSenderInfo": {"pan": "400000**1234", "paymentSystem": "VISA"},
        "senderIP": "185.220.101.0",  # A known Tor node or proxy IP
        "senderIpInformation": {
            "country": "Netherlands", "proxy": True, "timezone": "Europe/Amsterdam"
        }
    }
    transaction["_id"] = uuid.uuid4().hex
    collection.insert_one(transaction)
    features = extractor.extract_features(transaction)
    print("Proxy IP Detected:")
    pprint(features)

 
if __name__=="__main__":
    #simulate_country_mismatch()
    #simulate_timezone_switch()
    simulate_velocity_attack()
    #simulate_proxy_ip()
    
    
    
    