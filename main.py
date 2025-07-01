from fastapi import FastAPI
from extractors.feature_extractor import FeatureExtractor
from rules.rule_engine import RuleEngine

app = FastAPI(title="Key Watch")
extractor = FeatureExtractor()
rule_engine= RuleEngine(config_path="rules/rule_config.json")

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
        result = rule_engine.apply_rules(features)
        return {
            "status": "success",
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
