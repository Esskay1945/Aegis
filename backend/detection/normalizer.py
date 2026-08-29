import uuid
import time
from typing import Dict, Any, Tuple
from backend.models.schemas import RawEvent, SecurityEvent, SeverityType
from backend.detection.features import FeatureExtractor
from backend.detection.rules import RuleEngine
from backend.detection.anomaly import AnomalyDetector

class EventNormalizer:
    """Ingests raw telemetry, deduplicates, extracts features, computes anomaly & threat scores."""

    def __init__(self):
        self.feature_extractor = FeatureExtractor(window_seconds=60)
        self.anomaly_detector = AnomalyDetector()
        self.processed_ids = set()

    def process_raw_event(self, raw: RawEvent) -> Tuple[SecurityEvent, Dict[str, float], Tuple[Any, float, list]]:
        # Deduplication check
        if raw.event_id in self.processed_ids:
            # Generate new id if duplicate
            event_id = str(uuid.uuid4())
        else:
            event_id = raw.event_id
            self.processed_ids.add(event_id)

        # 1. Update temporal feature store
        self.feature_extractor.record_event(raw.source_ip, raw.event_type, raw.raw_data)
        features = self.feature_extractor.extract_features(raw.source_ip)
        feature_vector = self.feature_extractor.get_feature_vector(raw.source_ip)

        # 2. Compute ML Anomaly Score (0.0 to 1.0)
        anomaly_score = self.anomaly_detector.compute_anomaly_score(feature_vector)

        # 3. Evaluate Rule-based Engine
        rule_match, rule_conf, evidence = RuleEngine.evaluate(features, raw.model_dump())

        # 4. Compute composite Threat Score (0-100)
        # Combines rule confidence + ML anomaly score + raw indicators
        base_threat = (anomaly_score * 40.0)
        if rule_match:
            base_threat += (rule_conf * 60.0)
        threat_score = int(min(100.0, max(5.0, base_threat)))

        # Assign Severity
        if threat_score >= 80:
            severity: SeverityType = "CRITICAL"
        elif threat_score >= 60:
            severity: SeverityType = "HIGH"
        elif threat_score >= 35:
            severity: SeverityType = "MEDIUM"
        else:
            severity: SeverityType = "LOW"

        # Generate human-readable event description
        desc = self._generate_description(raw, threat_score, rule_match)

        sec_event = SecurityEvent(
            event_id=event_id,
            timestamp=raw.timestamp,
            source_ip=raw.source_ip,
            target_service=raw.target_service,
            event_type=raw.event_type,
            raw_data=raw.raw_data,
            suricata_alert=raw.suricata_alert,
            anomaly_score=round(anomaly_score, 3),
            threat_score=threat_score,
            severity=severity,
            description=desc
        )

        return sec_event, features, (rule_match, rule_conf, evidence)

    def _generate_description(self, raw: RawEvent, threat_score: int, rule_match: Any) -> str:
        t = raw.event_type
        ip = raw.source_ip
        svc = raw.target_service
        if t == "auth_failure":
            user = raw.raw_data.get("username", "unknown")
            return f"Failed login attempt for user '{user}' on {svc} from {ip}"
        elif t == "port_sweep" or t == "port_probe":
            p = raw.raw_data.get("port", "multi")
            return f"Port reconnaissance activity probing port {p} on {svc} from {ip}"
        elif t == "api_flood" or t == "api_request":
            ep = raw.raw_data.get("endpoint", "/")
            return f"High-velocity HTTP request to '{ep}' on {svc} from {ip}"
        elif t == "cred_compromise":
            return f"Anomalous session token reuse detected targeting {svc} from {ip}"
        return f"Observed {t} activity targeting {svc} from {ip}"

    def reset(self):
        self.feature_extractor.reset_all()
        self.processed_ids.clear()
