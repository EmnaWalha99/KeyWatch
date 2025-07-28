# 📘 KeyWatch - Documentation Technique Complète

**KeyWatch** est un microservice de détection de fraude construit en Python avec FastAPI et MongoDB, conçu pour analyser des transactions bancaires en temps réel. Il repose sur un système modulaire d'extraction de features et un moteur de règles déclaratives (YAML).

---

## 🚀 Prérequis & Installation

### 1. Cloner le repo

```bash
git clone https://github.com/EmnaWalha99/KeyWatch.git
cd KeyWatch
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
uvicorn main:app --reload
```

---

## 🧱 Stack Technique

### 🔹 Backend

* **Langage** : Python 3.11+
* **Framework** : FastAPI

### 🔹 Base de données

* **MongoDB** 
* **Nom de la base** : `fraud-detection`
* **Collections** :

  * `transactions` : transactions brutes reçues
  * `Logs` : logs des transactions traitées avec features + résultat

---

## 📂 Structure Principale du Projet

```
/config             -> Connexion DB et chargement .env
/extractors         -> Modules d'extraction de features
/rules              -> Moteur de règles YAML
/dataAccess         -> Accès à MongoDB, stats historiques
/transaction_formats -> Exemples de payloads JSON
/tests              -> Unit tests (pytest)
main.py             -> Entrée FastAPI
```
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

## 🔌 Fichier `main.py` - FastAPI Entrypoint

```python

app = FastAPI(title="Key Watch")
extractor = FeatureExtractor()
rules_engine = RuleEngine("rules/rules.yaml")

@app.post("/extract-features")
def extract_features(transaction_data: dict):

@app.post("/apply-rules")
def apply_rules(transaction_data: dict):

@app.get("/")
def root():
```

---

## 📁 config/ – Connexion à MongoDB

### `.env`

Contient les paramètres sensibles :

```env
MONGO_URI = mongodb://localhost:27017
DB_NAME = fraud-detection
COLLECTION_NAME = transactions
LOGS_COLLECTION = Logs
```

### `settings.py`

Utilise `python-decouple` pour charger les variables de `.env` :

```python
from decouple import Config, RepositoryEnv
config = Config(repository=RepositoryEnv("config/.env"))
MONGO_URI = config("MONGO_URI")
DB_NAME = config("DB_NAME")
COLLECTION_NAME = config("COLLECTION_NAME")
LOGS_COLLECTION = config("LOGS_COLLECTION")
```

### `db.py`

Expose les accès aux collections MongoDB :

```python
from pymongo import MongoClient
from config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME, LOGS_COLLECTION

def get_mongo_client():
    return MongoClient(MONGO_URI)

def get_transactions_collection():
    client = get_mongo_client()
    return client[DB_NAME][COLLECTION_NAME]

def get_logs_collection():
    client = get_mongo_client()
    return client[DB_NAME][LOGS_COLLECTION]
```

---

## 📁 extractors/ – Moteur d’extraction de features

Ce dossier contient tous les modules d’analyse statique de la transaction. Chaque fichier correspond à une catégorie de features.

### ✅ `extract_status.py`

* `extract_status(data)` : extrait le champ `status` et flag le status_failure_risk=1 en cas de failed_payment
* `extract_many_failed_attempts(data)` : détecte plus de 3 échecs de paiement

### 🕓 `extract_time_info.py`

* `extract_late_hour(data)` : calcule l’heure locale du paiement + `is_late_night`
* `extract_day(data)` : jour de la semaine + détection week-end

### 👤 `extract_sender_info.py`

* `extract_sender_info(data)` : extrait nom + email + flags `has_name`, `has_email`

### 🛍️ `extract_merchant_domain.py`

* `extract_merchant_domain(data)` : isole le domaine marchand (utile contre phishing)

### 🌍 `extract_location_info.py`

Contient les méthodes géo-IP, incohérences et comportements suspects :

* `extract_ip_info(data)` : ISP, ASN, proxy, hosting, lat/lon, etc.
* `extract_country_mismatch(data)` : compare pays IP vs banque
* `extract_impossible_travel(data)` : 🌌 Détecte un déplacement géographique impossible

      Principe :

      - Pour un même PAN, on récupère la dernière transaction

      - On calcule la distance entre les deux IP (coordonnées)

      - On calcule le temps entre les deux transactions

      - Si la vitesse estimée > 1000 km/h → flag impossible_travel = 1

      Exemples de fraude détectés :

      - Utilisation d’une même carte à Tunis à 10h01 et à Tokyo à 10h15 (surement VPN ou vol)

      - Multi-comptes avec partage de carte (fraude collaborative)
* `extract_frequent_timezone_switch(...)` : mesure le nombre de fuseaux horaires différents utilisés pour un PAN dans les N dernières transactions. Flag si seuil dépassé.

      Exemples de fraude :

      - Changement très fréquent de timezone sur une période courte

      - Comportement suspect de bots, attaques coordonnées

### 💳 `extract_card_and_payment_info.py`

* `extract_pan_info(data)` : extrait PAN + BIN
* `extract_amount(data)` : montant brut de la transaction
* `extract_avg_amount_last_7d(data)` : moyenne historique 7 jours (via `dataAccess.amount_stats`)
* `extract_fee_rate(data)` : taux de frais appliqué






## 🗃️ Module `dataAccess/` – Accès Données & Comportements Historiques

Ce dossier regroupe les fonctions liées à l’analyse des historiques de transaction, telles que la moyenne d’achat, le nombre de tentatives échouées, ou encore les comportements suspects comme les "velocity attacks".

### 💰 `amount_stats.py`

* `get_avg_amount_last_7d(pan, collection=None)` :

  * Calcule la **moyenne des montants** effectués par un PAN (carte) sur les **7 derniers jours**.
  * Utile pour détecter un **montant anormalement élevé** par rapport à l’historique du client.

### ❌ `count_failed_attempts.py`

* `count_failed_attempts(transaction, collection=None, time_window_minutes=1)` :

  * Compte le nombre d’**échecs de paiement** associés à un PAN dans une **fenêtre temporelle (ex: 1 min)**.
  * Permet de détecter des **tentatives de brute-force** ou des bots.

### 📈 `counting_transactions.py`

Module clé pour la détection de **velocity** (fréquence anormale) et **diversité** (variations de comportements). Il repose sur un fichier `velocity_config.yaml` configurable.

#### 🔁 `get_velocity_counts(transaction)`

* Calcule combien de fois un **champ donné** (PAN, IP, email, etc.) a été utilisé dans une certaine **fenêtre de temps**.
* Exemple : "La même IP utilisée 10 fois en 60 min" → `same_ip_used_in_last_60m`
* Permet de détecter des **attaques massives à partir d’un même canal**.

#### 🔀 `get_distinct_counts(transaction)`

* Compte le **nombre de valeurs distinctes** associées à un champ :

  * Ex: "Un même nom est lié à 5 PAN différents dans 30 minutes" → `name_to_pan_last_30m`
* Indicateur de **fraude organisée ou multi-cartes**.

#### 🧩 Fonctions utilitaires

* `get_nested_value()` : accède à des champs imbriqués comme `extSenderInfo.pan`
* `field_name()` : convertit une clé pointée en format lisible pour labels

### 🕵️ `find_last_trnx.py`

* `find_last_transaction_with_pan(transaction, collection)` :

  * Récupère la **dernière transaction** connue avec le même PAN.
  * Indispensable pour `impossible_travel`, permet la comparaison des coordonnées + timestamps.

### 🪵 `logging.py`

* `log_transaction(transaction: dict, features: dict, fraud_result: dict)` :

  * Enregistre chaque transaction enrichie (features + résultat règles) dans la **collection Logs** avec un timestamp `logged_at`.
  * Sert à la **traçabilité** des décisions et à l’évaluation future du système.



## Tests

- Outils : `pytest`
- Modules testés :
  - `rule_engine.py`
  - `feature_extractor.py`
  - `data_access.py`

pour lancer les tests il suffit d'execute pytest dans le terminal 

---

## 🧠 Module `rules/` – Moteur de Règles & Scoring de Fraude

Le dossier `rules/` contient la logique de **décision basée sur des règles déclaratives**. C’est ici que les features extraites sont confrontées à un ensemble de règles YAML pondérées.

### 📋 Fonctionnement

Le moteur de règles lit un fichier `rules.yaml`, itère sur chaque règle, et vérifie si une condition est remplie à partir des `features` extraites.

```python
engine = RuleEngine("rules/rules.yaml")
result = engine.evaluate(features)
```

### 📂 Structure d’une règle (YAML)

```yaml
- id: R100
  name: pan_velocity_15m
  field: same_card_used_in_last_15m
  condition: gt
  threshold: 3
  score: 50
  reason: "La carte a été utilisée plus de 3 fois en 15 min."
```

### ⚙️ `RuleEngine` – Fichier `rule_engine.py`

#### 🔧 Méthodes principales

* `__init__(rules_path)` : charge le fichier YAML des règles.

* `evaluate(features)` : applique chaque règle sur les données d’entrée, accumule le score, et retourne :

  * `matched_rules` : règles déclenchées
  * `reasons` : explication humaine
  * `raw_score` : score total
  * `fraud_risk` : niveau de risque (`low`, `medium`, `high`, `critical`)
  * `recommanded_action` : action proposée (`allow`, `manual_review`, `block`, `block_and_alert`)

* `rule_matched(rule, features)` : vérifie si une règle est satisfaite selon :

  * `eq` : égalité stricte
  * `gt` : strictement supérieur
  * `gt_relative_avg` : comparaison avec une valeur moyenne (ex : montant > 3x moyenne)

### 🧪 Exemples de Détection

#### 💳 Comportements Carte & Paiement

* `pan_velocity` : carte utilisée plusieurs fois en 15 ou 60 minutes
* `big_amount_relative_to_avg` : montant > 3x moyenne utilisateur
* `card_used_by_multiple_names` : carte utilisée avec différents noms récemment
* `many_failed_attempts` : plusieurs échecs avec la même carte

#### 🌐 Géolocalisation & IP

* `impossible_travel` : 2 transactions trop distantes en temps/espace → vitesse > 1000 km/h
* `country_mismatch` : pays IP ≠ pays de la banque
* `frequent_timezone_switch` : trop de changements de fuseaux horaires
* `same_ip_multiple_cards` : même IP utilisée pour plusieurs cartes
* `is_proxy`, `is_hosting` : IP suspecte (proxy, hébergeur)

#### ⏱️ Timing suspect

* `late_night_weekend` : paiement effectué la nuit pendant le weekend

#### 👤 Identité Utilisateur

* `missing_name`, `missing_email` : absence d’informations clés
* `name_used_with_multiple_cards` : un même nom utilisé avec plusieurs cartes


## 🔄 Configuration & Modularité des Règles

Le moteur de règles de **KeyWatch** est conçu pour être **entièrement configurable** et **modulaire** afin de faciliter son adaptation à différents scénarios de détection de fraude.

### 🗂️ Fichier `rules.yaml`

- Toutes les règles sont déclarées dans un fichier YAML unique (`rules/rules.yaml`).
- Chaque règle décrit :
  - L’`id` unique de la règle.
  - Le `field` (feature) à évaluer.
  - La `condition` (ex: `eq`, `gt`, `gt_relative_avg`).
  - Le `threshold` (seuil) à comparer.
  - Le `score` associé à la règle.
  - Le `reason` (explication humaine) pour le résultat.
- Les **fenêtres temporelles** (ex : "15 minutes", "60 minutes") sont aussi paramétrables via les features calculées, ce qui rend la durée d’analyse flexible et ajustable.

### 🧩 Architecture Modulaire

- Les **features** sont extraites par des modules indépendants (dans le dossier `/extractors`).
- Il est facile d’**ajouter de nouvelles features** sans modifier le moteur de règles.
- Le moteur applique les règles sur les features reçues, ce qui garantit une séparation claire entre extraction de données et logique métier.

### ⚙️ Extensibilité Facile

- Pour **ajouter une nouvelle règle**, il suffit d’écrire une nouvelle entrée YAML dans `rules.yaml`.
- Pour **intégrer une nouvelle feature**, il faut :
  1. Ajouter une fonction d’extraction dans `/extractors`.
  2. Mettre à jour la chaîne d’extraction pour inclure cette feature.
  3. Ajouter une règle utilisant cette nouvelle feature dans `rules.yaml`.

Cette architecture permet une **évolution rapide** et une **maintenance facilitée**, idéale pour un projet en constante adaptation comme la détection de fraude.



