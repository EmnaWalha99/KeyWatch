import yaml

class RuleEngine:
    def __init__(self, rules_path="rules/rules.yaml"):
        self.rules = self.load_rules(rules_path)
        self.max_possible_score = sum(rule.get("score", 0) for rule in self.rules)

    def load_rules(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f) or []

    def evaluate(self, features: dict) -> dict:
        matched = []
        total_score = 0
        reasons = []

        for rule in self.rules:
            if self.rule_matched(rule, features):
                matched.append(rule)
                reasons.append(rule.get("reason", "No reason provided"))
                total_score += rule.get("score", 0)

        # Classement risque selon score
        if total_score >= 120:
            risk = "critical"
            recommended_action = "block_and_alert"
        elif 80 <= total_score < 120:
            risk = "high"
            recommended_action = "block"
        elif 50 <= total_score < 80:
            risk = "medium"
            recommended_action = "manual_review"
        else:
            risk = "low"
            recommended_action = "allow"

        return {
            "reasons": reasons,
            "matched_rules": [r.get("id") for r in matched],
            "raw_score": total_score,
            "fraud_risk": risk,
            "recommended_action": recommended_action,
            "max_score": self.max_possible_score,
            # "fraud_percentage": round((total_score / self.max_possible_score) * 100, 2) if self.max_possible_score else 0
        }

    def rule_matched(self, rule, features):
        value = features.get(rule.get("field"))
        condition = rule.get("condition")
        threshold = rule.get("threshold")

        if value is None or condition is None or threshold is None:
            return False

        # Support pour différents types de conditions
        if condition == "eq":
            return value == threshold
        elif condition == "gt":
            return value > threshold
        elif condition == "gte":
            return value >= threshold
        elif condition == "lt":
            return value < threshold
        elif condition == "lte":
            return value <= threshold
        elif condition == "neq":
            return value != threshold
        else:
            # Condition non supportée
            return False
