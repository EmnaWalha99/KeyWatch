from pymongo import MongoClient
from datetime import datetime
import pytz
import uuid

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # or your connection string
db = client["fraud-detection"]
collection = db["transactions"]
def create_transaction(
    pan="521265**8210",
    name="SAMI SGHAIER",
    amount=3252000000,
    ip="197.26.95.0",
    city="Mégrine",
    lat=36.7707,
    lon=10.2404,
    timezone="Africa/TUNI",
    country="Tunisia"
):
    now = datetime.now(pytz.utc)

    transaction = {
        "type": "ePayment",
        "method": "bank_card",
        "addPaymentFeesToAmount": False,
        "payment": str(uuid.uuid4()),
        "receiverWallet": str(uuid.uuid4()),
        "underVerification": False,
        "hidden": False,
        "status": "success",
        "note": {"attachments": []},
        "comments": [],
        "token": "TND",
        "amount": amount,
        "message": "",
        "hideIdentity": False,
        "hideContribution": False,
        "origin": 1,
        "disputeInitiated": False,
        "refunded": False,
        "createdAt": now,
        "updatedAt": now,
        "ext_payment_ref": str(uuid.uuid4()),
        "from": "smt",
        "amountAfterFee": round(amount * 0.984, 2),
        "authRefNum": str(uuid.uuid4().int)[:12],
        "binInformation": str(uuid.uuid4()),
        "details": "Request processed successfully",
        "extSenderInfo": {
            "pan": pan,
            "approvalCode": "037983",
            "expiration": "202612",
            "paymentSystem": "MASTERCARD",
            "name": name,
            "email": "",
            "bankInfo": {
                "bankCountryCode": "788",
                "bankCountryName": country
            }
        },
        "feeRate": 1.6,
        "paidAt": now,
        "senderIP": ip,
        "senderIpInformation": {
            "status": "success",
            "country": country,
            "countryCode": "TN",
            "region": "13",
            "regionName": "Ben Arous Governorate",
            "city": city,
            "zip": "",
            "lat": lat,
            "lon": lon,
            "timezone": timezone,
            "currency": "TND",
            "isp": "3S INF",
            "org": "ATI - Agence Tunisienne Internet",
            "as": "AS37671 3S INF",
            "mobile": False,
            "proxy": False,
            "hosting": False,
            "query": ip
        },
        "senderIpLocation": {
            "type": "Point",
            "coordinates": [lon, lat],
            "updatedAt": now
        },
        "totalFee": round(amount * 0.016, 2)
    }

    return transaction

# Insert example
new_trx = create_transaction()
result = collection.insert_one(new_trx)
print(f"Inserted transaction with _id: {result.inserted_id}")
