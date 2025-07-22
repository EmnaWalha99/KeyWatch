from fastapi import FastAPI
from extractors.feature_extractor import FeatureExtractor
from rules.rule_engine import RuleEngine
from dataAccess.logging import log_transaction
from time import time 
from metrics import (
  REQUEST_COUNT,
  EXCEPTION_COUNT,
  REQUEST_DURATION,
  TRANSACTION_COUNT,
  FEATURE_EXTRACTION_TIME
)

from prometheus_client import make_asgi_app

app = FastAPI(title="Key Watch")

metrics_app = make_asgi_app()
app.mount("/metrics" , metrics_app)

extractor = FeatureExtractor()
rules_engine = RuleEngine("rules/rules.yaml")
@app.post("/extract-features")
def extract_features(transaction_data : dict):
  REQUEST_COUNT.inc()
  start= time()
  try : 
    with FEATURE_EXTRACTION_TIME.time():
      features = extractor.extract_features(transaction_data)
    return {
      "status" : "data extracted successfully",
      "features" : features
    }
  except Exception as e : 
    EXCEPTION_COUNT.inc()
    return { 
          "status" :"error" ,
          "message" : str(e)
        }
  finally :
    REQUEST_DURATION.observe(time()-start)
    
@app.post("/apply-rules")
def apply_rules(transaction_data: dict):
    REQUEST_COUNT.inc()
    start = time()
    try:
        with FEATURE_EXTRACTION_TIME.time():
          features = extractor.extract_features(transaction_data)
        result = rules_engine.evaluate(features)
        #TRANSACTION_COUNT.inc()

        #loggin the transactions 
        log_transaction(transaction_data, features, result)
        TRANSACTION_COUNT.inc()

        return {
            "status": "evaluating data successfully",
            "features": features,
            "fraud_result": result
        }
    except Exception as e:
        EXCEPTION_COUNT.inc()
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
      REQUEST_DURATION.observe(time()-start)
@app.get("/")
def root():
    return {"message": "Fraud Detection API - Ready!"}
