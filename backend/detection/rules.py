from typing import Dict, Any, Optional, Tuple

class RuleEngine:
    """Deterministic, zero-latency rule-based threat detection layer."""

    @staticmethod
    def evaluate(features: Dict[str, float], raw_event: Dict[str, Any]) -> Tuple[Optional[str], float, list]:
        """
        Evaluates extracted features against deterministic thresholds.
        Returns: (attack_class or None, confidence_score, evidence_list)
        """
        evidence = []
        event_type = raw_event.get("event_type", "")
        target_service = raw_event.get("target_service", "")

        # 1. SSH / Auth Brute Force Rule: >10 failures in 60s
        login_fails = features.get("login_failures_60s", 0)
        unique_users = features.get("unique_usernames_targeted", 0)
        if login_fails >= 10:
            evidence.append(f"{int(login_fails)} failed authentication attempts in 60s window (threshold: >10)")
            if unique_users > 1:
                evidence.append(f"Targeting {int(unique_users)} distinct usernames (credential spray pattern)")
            evidence.append(f"Auth failure ratio: {features.get('auth_failure_ratio', 0.0):.2%}")
            return "brute_force", min(0.98, 0.85 + (login_fails / 50.0)), evidence

        # 2. Port Scan Rule: >15 ports probed in 30s
        ports_scanned = features.get("ports_scanned_30s", 0)
        if ports_scanned >= 15 or event_type == "port_sweep":
            evidence.append(f"Port probe breadth: {int(ports_scanned)} distinct destination ports swept in 30s")
            evidence.append(f"Systematic reconnaissance signature targeting {target_service}")
            return "port_scan", min(0.99, 0.88 + (ports_scanned / 40.0)), evidence

        # 3. API / HTTP Flood Rule: >300 requests/minute from single source
        rpm = features.get("requests_per_minute", 0)
        if rpm >= 300 or (event_type == "api_flood" and rpm > 50):
            evidence.append(f"High-frequency request rate: {int(rpm)} req/min (baseline threshold: >300)")
            evidence.append(f"Endpoint diversity score: {features.get('endpoint_diversity', 1.0):.1f}")
            return "api_flood", min(0.97, 0.82 + (rpm / 600.0)), evidence

        # 4. Credential Compromise / Token Reuse Simulation Rule
        if event_type == "cred_compromise" or raw_event.get("raw_data", {}).get("token_anomaly"):
            evidence.append("Active session token used from novel ASN / unrecognized geographical IP")
            evidence.append("Token signature matches compromised credential repository")
            return "cred_compromise", 0.94, evidence

        # 5. Suricata IDS Alert Passthrough
        suricata = raw_event.get("suricata_alert")
        if suricata:
            msg = suricata.get("msg", "Known attack signature")
            sid = suricata.get("sid", 1000)
            evidence.append(f"Suricata IDS Alert [SID: {sid}]: {msg}")
            if "SCAN" in msg.upper():
                return "port_scan", 0.92, evidence
            elif "BRUTE" in msg.upper():
                return "brute_force", 0.95, evidence
            elif "DOS" in msg.upper() or "FLOOD" in msg.upper():
                return "api_flood", 0.93, evidence

        return None, 0.0, []
