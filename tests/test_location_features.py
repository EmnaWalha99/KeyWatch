import pytest
from datetime import datetime, timedelta
from extractors.extract_location_info import extract_frequent_timezone_switch
from extractors.extract_location_info import extract_impossible_travel

class DummyCollection:
    pass  # Not used in this test, but required by the function signature

def dummy_find_last_transaction_with_pan(data, collection=None):
    # Simulate a previous transaction 1 hour ago, 1000km away
    return {
        "senderIpLocation": {"coordinates": [10.0, 45.0]},
        "createdAt": data["createdAt"] - timedelta(hours=1)
    }

def test_extract_impossible_travel(monkeypatch):
    # Patch the find_last_transaction_with_pan function
    monkeypatch.setattr(
        "extractors.extract_location_info.find_last_transaction_with_pan",
        dummy_find_last_transaction_with_pan
    )

    # Current transaction: coordinates [20.0, 45.0], now
    now = datetime(2024, 8, 16, 12, 0, 0)
    data = {
        "senderIpLocation": {"coordinates": [20.0, 45.0]},
        "createdAt": now,
        "extSenderInfo": {"pan": "1234"}
    }

    result = extract_impossible_travel(data)
    assert "impossible_travel" in result
    assert "travel_distance_km" in result
    assert "travel_speed_kmh" in result
    assert result["impossible_travel"] in (0, 1)
    assert result["travel_distance_km"] > 0
    assert result["travel_speed_kmh"] > 0

def test_extract_impossible_travel_no_last(monkeypatch):
    # Patch to simulate no previous transaction
    monkeypatch.setattr(
        "extractors.extract_location_info.find_last_transaction_with_pan",
        lambda data, collection=None: None
    )
    now = datetime(2024, 8, 16, 12, 0, 0)
    data = {
        "senderIpLocation": {"coordinates": [20.0, 45.0]},
        "createdAt": now,
        "extSenderInfo": {"pan": "1234"}
    }
    result = extract_impossible_travel(data)
    assert result["impossible_travel"] == 0
    


class MockCollection : 
    def __init__(self , docs) : 
        self.docs = docs 
    def find(self , query , sort=None , limit= 0):
        return self.docs[:limit] if limit else self.docs
    
def test_extract_frequent_timezone_switch():
    #3 transactions with 3 different timezones
    docs = [
        {"senderIpInformation": {"timezone": "Europe/Paris"}},
        {"senderIpInformation": {"timezone": "Africa/Tunis"}},
        {"senderIpInformation": {"timezone": "Asia/Dubai"}},
    ]
    collection = MockCollection(docs)
    data = {"extSenderInfo": {"pan":"1234"}}
    result = extract_frequent_timezone_switch(data , collection=collection , n=3 , threshold=2)
    assert result["frequent_timezone_switch"]==1
    assert result["unique_timezones"]==3

def test_extract_frequent_timezone_switch_not_frequent():
    # Simulate 3 transactions with the same timezone
    docs = [
        {"senderIpInformation": {"timezone": "Europe/Paris"}},
        {"senderIpInformation": {"timezone": "Europe/Paris"}},
        {"senderIpInformation": {"timezone": "Europe/Paris"}},
    ]
    collection = MockCollection(docs)
    data = {"extSenderInfo": {"pan": "1234"}}
    result = extract_frequent_timezone_switch(data, collection=collection, n=3, threshold=2)
    assert result["frequent_timezone_switch"] == 0
    assert result["unique_timezones"] == 1
