from typing import Dict, Any, List, Tuple
from backend.models.schemas import AttackClassType, SeverityType, SecurityEvent

class ThreatClassifier:
    """Classifies attack category and assigns confidence levels from normalized signals."""

    @staticmethod
    def classify(event: SecurityEvent, features: Dict[str, float], rule_result: Tuple[Any, float, list]) -> Tuple[AttackClassType, float, List[str]]:
        rule_match, rule_conf, rule_evidence = rule_result

        # If rule matched with high confidence, use it with ML-augmented features
        if rule_match:
            evidence = list(rule_evidence)
            # Add ML confirmation
            if event.anomaly_score > 0.7:
                evidence.append(f"Isolation Forest ML Anomaly Score: {event.anomaly_score:.2f} (Elevated)")
            return rule_match, rule_conf, evidence

        # Fallback to ML-based heuristic classification
        if event.anomaly_score >= 0.75:
            evidence = [
                f"Isolation Forest identified non-baseline behavioral anomaly (score: {event.anomaly_score:.2f})",
                f"Target Service: {event.target_service}",
                f"Observed Rate: {features.get('requests_per_minute', 0)} req/min"
            ]
            if features.get("login_failures_60s", 0) > 4:
                return "brute_force", 0.78, evidence
            elif features.get("ports_scanned_30s", 0) > 5:
                return "port_scan", 0.81, evidence
            elif features.get("requests_per_minute", 0) > 100:
                return "api_flood", 0.79, evidence
            else:
                return "apt_campaign", 0.72, evidence

        return "none", 0.15, ["Traffic conforms to learned baseline behavioral metrics"]
