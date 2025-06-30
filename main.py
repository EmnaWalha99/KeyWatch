from fastapi import FastAPI
from extractors.feature_extractor import FeatureExtractor

app = FastAPI(title="Key Watch")
extractor = FeatureExtractor()

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
@app.get("/")
def root():
    return {"message": "Fraud Detection API - Ready!"}
