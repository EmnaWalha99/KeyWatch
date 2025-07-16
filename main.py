from fastapi import FastAPI
from extractors.feature_extractor import FeatureExtractor
from rules.rule_engine import RuleEngine
from dataAccess.logging import log_transaction

app = FastAPI(title="Key Watch")
extractor = FeatureExtractor()
rules_engine = RuleEngine("rules/rules.yaml")
@app.post("/extract-features")
def extract_features(transaction_data : dict):
  
  try : 
    features = extractor.extract_features(transaction_data)
    return {
      "status" : "data extracted successfully",
      "features" : features
    }
  except Exception as e : 
    return { 
          "status" :"error" ,
          "message" : str(e)
        }
    
@app.post("/apply-rules")
def apply_rules(transaction_data: dict):
    try:
        features = extractor.extract_features(transaction_data)
        result = rules_engine.evaluate(features)
        
        #loggin the transactions 
        log_transaction(transaction_data, features, result)

        return {
            "status": "evaluating data successfully",
            "features": features,
            "fraud_result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
@app.get("/")
def root():
    return {"message": "Fraud Detection API - Ready!"}
