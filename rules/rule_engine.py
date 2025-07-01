import json 


class RuleEngine:
    def __init__(self, config_path="rules/rule_config.json"):
        with open(config_path) as f:
            self.rules = json.load(f)
    def apply_rules(self, features:dict):
        score=0
        reasons=[]
        max_score=sum(rules.get("score", 0) for rules in self.rules.values())
        
        for key,rules in self.rules.items():
            feature_value = features.get(key)
            if feature_value is not None and str(feature_value) ==str(rules.get("value")):
                score+= rules.get("score", 0 )
                reasons.append(f"{key} matched rule ->+{rules.get('score', 0)} points")
        fraud_percentage = (score/max_score *100) if max_score > 0 else 0
        return {
            "fraud_percentage": round(fraud_percentage, 2),
            "reasons": reasons}