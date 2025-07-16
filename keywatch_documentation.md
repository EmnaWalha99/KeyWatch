
# KeyWatch - Microservice de Détection de Fraude

## 🧾 Introduction

**KeyWatch** est un microservice standalone de détection de fraude développé pour **Konnect Networks**, une passerelle de paiement en ligne. Il est conçu avec une architecture **modulaire, scalable et évolutive**, capable de combiner des règles statiques et, potentiellement à terme, un moteur décisionnel ML.

Le service reçoit en entrée une transaction, effectue une **extraction automatique des données comportementales et contextuelles**, puis applique un moteur de règles configurable pour déterminer le **score de risque de fraude** et **recommander une action** (`allow`, `manual_review`, `block`, etc.).

---

## Architecture Générale

### Composants principaux :
- **FastAPI** : API REST exposant les endpoints.
- **MongoDB** : base de données des transactions pour les vérifications d'historique.
- **Feature Extractor** : extraction des patterns de fraude connus (vélocité, géolocalisation, comportement).
- **RuleEngine** : moteur de règles basé sur YAML.
- **Scoreur** : calcule le score de fraude selon les règles déclenchées.

> 🧪 (à venir) Device fingerprinting comme nouvelle source de features.

### Arborescence du projet :
```
/config
/dataAccess
/extractors
/models
/rules
/tests
/transaction_formats
main.py
```

---

## Installation & Démarrage

### Création de l’environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # sous Linux/Mac
venv\Scripts\activate   # sous Windows
pip install -r requirements.txt
```

### Lancer le microservice :
```bash
uvicorn main:app --reload
```

---

## Endpoints disponibles

| Méthode | URL                             | Description                         |
|--------|----------------------------------|-------------------------------------|
| POST   | `/apply-rules`                  | Applique le moteur de règles        |
| POST   | `/extract-features`             | Extrait les features d'une transaction |

---

## Fonctionnement global

1. Réception de la transaction (POST)
2. Extraction des features comportementales et contextuelles
3. Application des règles YAML à ces features
4. Calcul du score de risque de fraude
5. Réponse avec niveau de risque, action recommandée et raisons

### Exemple JSON d’entrée :
```json

{
  "type": "ePayment",
  "method": "bank_card",
  "addPaymentFeesToAmount": false,
  "payment": "2fee7bc0-ec06-495c-97c9-79848e01bdcb",
  "receiverWallet": "db2b46e6-8c57-49a6-95f7-cb9f61bf4b55",
  "underVerification": false,
  "hidden": false,
  "status": "failed_payment",
  "note": {
    "attachments": []
  },
  "comments": [],
  "token": "TND",
  "amount": 3252000000 ,
  "message": "",
  "hideIdentity": false,
  "hideContribution": false,
  "origin": 1,
  "disputeInitiated": false,
  "refunded": false,
  "createdAt": {
    "$date": "2025-07-14T10:46:19.340Z"
  },
  "updatedAt": {
    "$date": "2025-07-14T10:46:19.340Z"
  },
  "from": "smt",
  "amountAfterFee": 3199968000,
  "authRefNum": "758197571373",
  "binInformation": "f458c8e8-e5bf-4a0a-966e-98f2b7764e5f",
  "details": "Request processed successfully",
  "extSenderInfo": {
    "pan": "521265**8210",
    "approvalCode": "037983",
    "expiration": "202612",
    "paymentSystem": "MASTERCARD",
    "name": "SAMI SGHAIER",
    "email": "",
    "bankInfo": {
      "bankCountryCode": "788",
      "bankCountryName": "Tunisiiiia"
    }
  },
  "feeRate": 1.6,
  "paidAt": {
    "$date": "2025-07-14T10:46:19.340Z"
  },
  "senderIP": "197.26.95.0",
  "senderIpInformation": {
    "status": "success",
    "country": "Tunisia",
    "countryCode": "TN",
    "region": "13",
    "regionName": "Ben Arous Governorate",
    "city": "Mégrine",
    "zip": "",
    "lat": 36.7707,
    "lon": 10.2404,
    "timezone": "Africa/TUNI",
    "currency": "TND",
    "isp": "3S INF",
    "org": "ATI - Agence Tunisienne Internet",
    "as": "AS37671 3S INF",
    "mobile": false,
    "proxy": false,
    "hosting": false,
    "query": "197.26.95.0"
  },
  "senderIpLocation": {
    "type": "Point",
    "coordinates": [
      10.2404,
      36.7707
    ],
    "updatedAt": {
      "$date": "2025-07-14T10:46:19.340Z"
    }
  },
  "totalFee": 52032000
}
```

### Exemple de sortie :
```json
{
    "status": "evaluating data successfully",
    "features": {
        "email": "",
        "has_email": 0,
        "name": "SAMI SGHAIER",
        "has_name": 1,
        "senderIP": "197.26.95.0",
        "ip_country": "Tunisia",
        "ip_countryCode": "TN",
        "ip_region": "13",
        "ip_regionName": "Ben Arous Governorate",
        "ip_city": "Mégrine",
        "ip_zip": "",
        "ip_lat": 36.7707,
        "ip_lon": 10.2404,
        "ip_timezone": "Africa/TUNI",
        "ip_currency": "TND",
        "ip_isp": "3S INF",
        "ip_org": "ATI - Agence Tunisienne Internet",
        "ip_as": "AS37671 3S INF",
        "is_mobile": 0,
        "is_proxy": 0,
        "is_hosting": 0,
        "ip_location_type": "Point",
        "ip_location_coordinates": [
            10.2404,
            36.7707
        ],
        "ip_location_updatedAt": "2025-07-14T10:46:19.340Z",
        "amount": 3252000000,
        "merchant_domain": "",
        "local_hour": 10,
        "is_late_night": 0,
        "day_of_week": 0,
        "is_weekend": 0,
        "status": "failed_payment",
        "status_failure_risk": 1,
        "failure_contains_low_balance": 0,
        "ip_country_and_bank_country_mismatch": 1,
        "fee_rate": 1.6,
        "pan": "521265**8210",
        "bin": "521265",
        "impossible_travel": 0,
        "time_difference_with_last_trnx_h": -0.47204138888888886,
        "travel_distance_km": 0.0,
        "travel_speed_kmh": -0.0,
        "avg_amount_last_7d": 3252000000.0,
        "frequent_timezone_switch": 0,
        "unique_timezones": 1,
        "same_card_used_in_last_15m": 0,
        "same_card_used_in_last_60m": 0,
        "same_ip_used_in_last_60m": 0,
        "same_name_used_in_last_300m": 0,
        "same_card_used_by_multiple_names_last_15m": 0,
        "same_card_used_from_multiple_ips_last_15m": 0,
        "same_ip_used_by_multiple_cards_last_60m": 0,
        "same_name_used_with_multiple_cards_last_300m": 0
    },
    "fraud_result": {
        "reasons": [
            "This transaction amount is unusually large and may require additional review.",
            "The IP address location and the card issuer's country do not match, which may indicate a spoofed or foreign origin.",
            "No email address was provided in this transaction, which may reduce traceability and increase risk."
        ],
        "matched_rules": [
            "R105",
            "R201",
            "R500"
        ],
        "raw_score": 60,
        "fraud_risk": "medium",
        "recommanded_action": "manual_review"
    }
}
```

---

## Exemple de règles YAML

```yaml
# R1xx - Card & Payment Behavior

- id: R100
  name: pan_velocity_15m
  description: "Same card used more than 3 times in 15 minutes"
  field: same_card_used_in_last_15m
  context_field: pan
  condition: "gt"
  threshold: 3
  score: 50
  reason: "The same card was used more than 3 times in 15 minutes, which may indicate automated or suspicious activity."

#R5xx - User Identity

- id: R500
  name: missing_email
  description: "Email field is empty"
  field: has_email
  condition: "eq"
  threshold: 0
  score: 10
  reason: "No email address was provided in this transaction, which may reduce traceability and increase risk."


#R3xx - Timing Behavior

- id: R300
  name: late_night_weekend
  description: "Transaction at night during weekend"
  field: is_late_night
  condition: "eq"
  threshold: 1
  extra_condition:
    field: is_weekend
    condition: "eq"
    threshold: 1
  score: 10
  reason: "This transaction was made late at night during the weekend, which can be a risky time for fraud."


# R2xx - Geolocation & IP Behavior

- id: R200
  name: impossible_travel
  description: "Travel speed exceeds plausible maximum"
  field: impossible_travel
  condition: "eq"
  threshold: 1
  score: 40
  reason: "This user appears to have made a transaction from a location too far from the previous one in an unrealistic time, suggesting fraud."

```

---

## Features extraites

Quelques exemples de features générées automatiquement :
- `has_email`, `has_name`
- `amount`, `avg_amount_last_7d`
- `is_late_night`, `is_weekend`, `day_of_week`
- `status_failure_risk`, `failure_contains_low_balance`
- `ip_country_and_bank_country_mismatch`
- `time_difference_with_last_trnx_h`
- `impossible_travel`
- `same_card_used_in_last_15m`, `same_ip_used_in_last_60m`
- `same_name_used_with_multiple_cards_last_300m`
- `same_ip_used_by_multiple_cards_last_60m`


---

## Tests

- Outils : `pytest`
- Modules testés :
  - `rule_engine.py`
  - `feature_extractor.py`
  - `data_access.py`

---

## Auteure

**Emna Walha**  
Juin – Juillet 2025  
