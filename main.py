from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from extractors.feature_extractor import FeatureExtractor
from rules.rule_engine import RuleEngine
from dataAccess.logging import log_transaction

app = FastAPI(title="Key Watch")

extractor = FeatureExtractor()
rules_engine = RuleEngine("rules/rules.yaml")


@app.post("/extract-features")
async def extract_features(transaction_data: dict):
    try:
        features = await extractor.extract_features(transaction_data)
        return {"status": "data extracted successfully", "features": features}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


@app.post("/apply-rules")
async def apply_rules(transaction_data: dict):
    try:
        features = await extractor.extract_features(transaction_data)
        result = rules_engine.evaluate(features)

        # Log transaction asynchronously if possible
        # Consider making log_transaction async if it involves I/O
        log_transaction(transaction_data, features, result)

        return {
            "status": "evaluating data successfully",
            "features": features,
            "fraud_result": result,
        }
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


@app.get("/")
def root():
    return {"message": "Fraud Detection API - Ready!"}
