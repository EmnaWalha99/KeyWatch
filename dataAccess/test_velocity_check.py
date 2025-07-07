import pytest
import mongomock
from datetime import datetime, timedelta, timezone
from dataAccess.counting_transactions import get_velocity_counts  # importe ta méthode ici

@pytest.fixture
def mock_collection():
    # Création d'une collection MongoDB mockée
    client = mongomock.MongoClient()
    db = client['fraud-detection']
    return db['transactions']

def insert_mock_transactions(collection, base_time):
    pan = "521265**8218"
    sender_ip = "197.26.95.0"
    name = "SAMI SGHAIER"

    for i in range(5):  # 5 transactions à 1 min d'écart
        doc = {
            "createdAt": base_time - timedelta(minutes=i),
            "extSenderInfo": {
                "pan": pan,
                "email": "",
                "name": name
            },
            "senderIP": sender_ip
        }
        collection.insert_one(doc)

def test_velocity_check_returns_correct_counts(mock_collection):
    now = datetime.now(timezone.utc)
    insert_mock_transactions(mock_collection, now)

    transaction = {
        "extSenderInfo": {
            "pan": "521265**8218",
            "email": "",
            "name": "SAMI SGHAIER"
        },
        "senderIP": "197.26.95.0"
    }

    result = get_velocity_counts(transaction, now=now, collection=mock_collection)

    assert result["pan_15m_velocity"] == 5
    assert result["senderIP_60m_velocity"] == 5
    assert result["name_300m_velocity"]== 5
