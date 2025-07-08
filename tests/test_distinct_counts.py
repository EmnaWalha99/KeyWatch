import pytest
import mongomock
from datetime import datetime, timedelta, timezone
from dataAccess.counting_transactions import get_distinct_counts


@pytest.fixture
def mock_collection():
    client =mongomock.MongoClient()
    db = client['fraud-detection']
    return db['transactions']

def insert_distinct_mock_transactions(collection , base_time):
    #transaction with different combinations 
    docs = [
        #same pan different names and senderIPs
        {
            "createdAt" : base_time , 
            "extSenderInfo": {"pan": "1111","name":"EMNA"},
            "senderIP":"1.1.1.1"
        },
        {
            "createdAt" : base_time , 
            "extSenderInfo": {"pan": "1111","name":"ARIJ"},
            "senderIP":"2.2.2.2"
            
        },
        {
            "createdAt" : base_time , 
            "extSenderInfo": {"pan": "1111","name":"ABIR"},
            "senderIP":"3.3.3.3"
            
        },
        # same senderIP and different pans 
        {
            "createdAt" : base_time , 
            "extSenderInfo": {"pan": "1234","name":"HACKER"},
            "senderIP":"1.1.1.1"
        },
        {
            "createdAt" : base_time , 
            "extSenderInfo": {"pan": "5678","name":"HACKER"},
            "senderIP":"1.1.1.1"
        } , 
        #same name differnet pans
        { 
            "createdAt" : base_time , 
            "extSenderInfo": {"pan": "1234","name":"HACKER"},
            "senderIP":"4.4.4.4"
        }
    ]
    collection.insert_many(docs)

def test_distinct_count_returns_correct_counts(mock_collection):
    now = datetime.now(timezone.utc)
    
    insert_distinct_mock_transactions(mock_collection, now)
    
    #test for PAN 
    transaction = {
        "extSenderInfo":{"pan":"1111", "name":"EMNA"},
        "senderIP":"1.1.1.1"
    }
    result = get_distinct_counts(transaction , now=now , collection=mock_collection)
    print(result.keys())
    assert result["same_card_used_by_multiple_names_last_15m"]==3
    assert result["same_card_used_from_multiple_ips_last_15m"] ==3
    
    #test for senderIP
    transaction = { 
        "extSenderInfo": {"pan":"1234","name":"HACKER"},
        "senderIP" : "1.1.1.1"
        }
    result = get_distinct_counts(transaction , now=now,collection=mock_collection)
    print(result.keys())
    
    #for senderip 1.1.1.1 should find 3 distinct pans (1111,1234, 5678)
    assert result["same_ip_used_by_multiple_cards_last_60m"]== 3
    
    #test for extSenderInfo.name
    transaction = { 
        "extSenderInfo" : {"pan":"1234", "name":"HACKER"},
        "senderIP" : "4.4.4.4"
        }
    result = get_distinct_counts(transaction , now=now , collection=mock_collection)
    print(result.keys())
    assert result["same_name_used_with_multiple_cards_last_300m"]==2
    