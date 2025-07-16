

class RuleEngine:
    def __init__(self, rules_path="rules/rules.yaml"):
       self.rules = self.load_rules(rules_path)
       
    def load_rules(self, path):
        import yaml
        with open(path , "r") as f : 
            return yaml.safe_load(f)
    
    def evaluate(self, features: dict) -> dict:
        matched = []
        total_score = 0
        reasons = []
        for rule in self.rules:
            if self.rule_matched(rule , features):
                matched.append(rule)
                reasons.append(rule["reason"])
                total_score += rule["score"]
        # Normalize to percentage (optional logic)
        max_possible_score = sum(rule["score"] for rule in self.rules)
        #fraud_percentage = (total_score / max_possible_score) * 100 if max_possible_score else 0
        if total_score>= 120 : 
            risk="critical"
            recommanded_action = "block_and_alert"
        elif 80<=total_score<=119 : 
            risk = "high"
            recommanded_action ="block"
        elif 50<= total_score <=79 : 
            risk = "medium"
            recommanded_action = "manual_review"
        else : 
            risk= "low"
            recommanded_action ="allow"
        return {
            #"fraud_percentage": round(fraud_percentage, 2),
            "reasons": reasons,
            "matched_rules": [r["id"] for r in matched],
            "raw_score": total_score,
            "fraud_risk" : risk,
            "recommanded_action" : recommanded_action,
            #"max_score": max_possible_score
        }
                
                
        
    
    def rule_matched(self, rule , features):
        value = features.get(rule["field"])
        condition = rule["condition"]
        threshold = rule["threshold"]
        
        if value is None : 
            return False
        if condition =="eq" :
            match = value ==threshold
        elif condition=="gt" : 
            match = value > threshold
        
        
        else : 
            match= False
        
        return match
    