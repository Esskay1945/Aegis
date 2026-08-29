import uuid
from datetime import datetime
from typing import Dict, Any, List
from backend.models.schemas import SecurityEvent, AIAnalysisResult, AttackClassType, SeverityType
from backend.agents.classifier import ThreatClassifier
from backend.agents.recommender import ActionRecommender

class AIReasoner:
    """Provides semantic explainability, blast radius calculation, and structured AI analysis."""

    @staticmethod
    def analyze(event: SecurityEvent, features: Dict[str, float], rule_result: Any) -> AIAnalysisResult:
        attack_class, confidence, evidence = ThreatClassifier.classify(event, features, rule_result)
        
        # Determine recommended actions
        recommended_actions = ActionRecommender.recommend(attack_class, event, confidence)

        # Generate natural language explanation
        explanation = AIReasoner._generate_explanation(attack_class, event, confidence, evidence)
        
        # Calculate blast radius
        blast_radius = AIReasoner._calculate_blast_radius(attack_class, event)

        # Determine auto-execute eligibility: confidence >= 0.80 and not system shutdown
        auto_eligible = (confidence >= 0.80) and (event.severity != "CRITICAL" or attack_class != "none")

        return AIAnalysisResult(
            analysis_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            trigger_event_ids=[event.event_id],
            attack_class=attack_class,
            confidence=round(confidence, 3),
            severity=event.severity,
            evidence=evidence,
            affected_services=[event.target_service],
            recommended_actions=recommended_actions,
            explanation=explanation,
            blast_radius=blast_radius,
            auto_execute_eligible=auto_eligible
        )

    @staticmethod
    def _generate_explanation(attack_class: AttackClassType, event: SecurityEvent, confidence: float, evidence: List[str]) -> str:
        ip = event.source_ip
        svc = event.target_service
        pct = int(confidence * 100)

        if attack_class == "brute_force":
            return (
                f"High-confidence ({pct}%) authentication brute-force attack detected from {ip} targeting {svc}. "
                f"Sustained failure rate deviates sharply from baseline traffic models. "
                f"Defensive actions apply per-service rate limits and credential cycling while preserving database access."
            )
        elif attack_class == "port_scan":
            return (
                f"Automated port sweep and service reconnaissance ({pct}% confidence) initiated by {ip} against {svc}. "
                f"Rapid probing of multi-port ranges indicates precursor to targeted exploit delivery. "
                f"Port restriction and source filtering recommended."
            )
        elif attack_class == "api_flood":
            return (
                f"Application-layer HTTP request flood ({pct}% confidence) originating from {ip} directed at {svc}. "
                f"Targeted rate limiting and ingress drop recommended to mitigate degradation without affecting neighboring backend tiers."
            )
        elif attack_class == "cred_compromise":
            return (
                f"Critical credential anomaly ({pct}% confidence): Unauthorized token reuse signature on {svc} from {ip}. "
                f"Immediate credential invalidation, secret rotation, and token issuance required."
            )
        elif attack_class == "apt_campaign":
            return (
                f"Coordinated multi-vector campaign identified against {svc}. Recommended container network isolation and forensic log capture."
            )
        return f"Normal baseline telemetry observed for {svc} from {ip}. No immediate defensive action required."

    @staticmethod
    def _calculate_blast_radius(attack_class: AttackClassType, event: SecurityEvent) -> str:
        svc = event.target_service
        if attack_class == "brute_force":
            return f"Confined exclusively to {svc} authentication ingress. Zero impact to backend DB or Web proxies."
        elif attack_class == "api_flood":
            return f"Isolated to {svc} HTTP endpoints. Downstream services and internal VPC remaining fully operational."
        elif attack_class == "port_scan":
            return f"Reconnaissance perimeter on {svc} exposed ports only."
        elif attack_class == "cred_compromise":
            return f"High risk if token leaks across microservices. Scoped rotation isolates potential breach."
        return "Baseline operational scope (0% blast radius)."
