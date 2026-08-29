from typing import List
from backend.models.schemas import AttackClassType, ServiceId, DefenseAction, SecurityEvent

class ActionRecommender:
    """Generates attack-appropriate, resource-scoped defensive recommendations."""

    @staticmethod
    def recommend(attack_class: AttackClassType, event: SecurityEvent, confidence: float) -> List[DefenseAction]:
        actions: List[DefenseAction] = []
        source_ip = event.source_ip
        svc = event.target_service

        if attack_class == "brute_force":
            # 1. Block attacker IP specifically on the targeted service
            actions.append(DefenseAction(
                type="block_ip",
                target=source_ip,
                scope=svc,
                ttl=3600,
                layer_target=3,
                reason=f"Drop malicious authentication ingress traffic from {source_ip}"
            ))
            # 2. Rate limit authentication endpoint
            actions.append(DefenseAction(
                type="rate_limit",
                target=svc,
                scope=svc,
                ttl=1800,
                threshold="5/min",
                layer_target=14,
                reason=f"Enforce dynamic rate throttling on {svc} auth ingress"
            ))
            # 3. Rotate credential to safeguard against successful spray
            actions.append(DefenseAction(
                type="rotate_credential",
                target="SERVICE_AUTH_KEY",
                scope=svc,
                ttl=0,
                credential_id=f"{svc.upper()}_KEY_V1",
                layer_target=11,
                reason=f"Proactively cycle secret keys for {svc} to invalidate enumerated tokens"
            ))

        elif attack_class == "port_scan":
            # 1. Close or throttle probed ports
            actions.append(DefenseAction(
                type="port_restrict",
                target="DYNAMIC_PORTS",
                scope=svc,
                ttl=1800,
                layer_target=4,
                reason=f"Restrict exposed non-essential ports on {svc}"
            ))
            # 2. Block scanning source IP
            actions.append(DefenseAction(
                type="block_ip",
                target=source_ip,
                scope=svc,
                ttl=3600,
                layer_target=3,
                reason=f"Drop all packets from port scanner IP {source_ip}"
            ))

        elif attack_class == "api_flood":
            # 1. Rate limit API service
            actions.append(DefenseAction(
                type="rate_limit",
                target=svc,
                scope=svc,
                ttl=1800,
                threshold="60/min",
                layer_target=14,
                reason=f"Throttle excessive request flood targeting {svc} (leaves DB untouched)"
            ))
            # 2. Block flooding IP
            actions.append(DefenseAction(
                type="block_ip",
                target=source_ip,
                scope=svc,
                ttl=3600,
                layer_target=7,
                reason=f"Filter application layer HTTP flood from {source_ip}"
            ))

        elif attack_class == "cred_compromise":
            # 1. Immediate credential revocation & rotation
            actions.append(DefenseAction(
                type="rotate_credential",
                target="SERVICE_BEARER_TOKEN",
                scope=svc,
                ttl=0,
                credential_id=f"{svc.upper()}_BEARER_V1",
                layer_target=11,
                reason=f"Instantly revoke leaked/compromised credential on {svc} and distribute V2"
            ))
            # 2. Block anomalous source IP
            actions.append(DefenseAction(
                type="block_ip",
                target=source_ip,
                scope=svc,
                ttl=7200,
                layer_target=9,
                reason=f"Blacklist rogue unauthorized IP {source_ip} exploiting token"
            ))

        elif attack_class == "apt_campaign":
            # Multi-vector APT response
            actions.append(DefenseAction(
                type="isolate_service",
                target=svc,
                scope=svc,
                ttl=900,
                layer_target=20,
                reason=f"Move {svc} to isolated quarantine container network for forensic containment"
            ))
            actions.append(DefenseAction(
                type="rotate_credential",
                target="ALL_KEYS",
                scope=svc,
                ttl=0,
                credential_id=f"{svc.upper()}_ROOT_V1",
                layer_target=11,
                reason=f"Complete credential rotation for {svc} during multi-stage campaign"
            ))

        return actions
