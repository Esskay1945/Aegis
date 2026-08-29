from typing import Tuple, Set
from backend.models.schemas import DefenseAction, SeverityType

class SafetyConstraints:
    """Safety checks to prevent self-inflicted denial of service and unconstrained AI execution."""

    PROTECTED_IPS: Set[str] = {
        "127.0.0.1",
        "localhost",
        "::1",
        "10.0.0.1", # Gateway
        "8.8.8.8",
        "1.1.1.1"
    }

    HUMAN_APPROVAL_ACTIONS: Set[str] = {
        "full_system_shutdown",
        "database_wipe",
        "bulk_credential_revocation",
        "global_network_partition"
    }

    @classmethod
    def validate_action(cls, action: DefenseAction, severity: SeverityType) -> Tuple[bool, str, bool]:
        """
        Validates action safety.
        Returns: (is_safe: bool, reason: str, human_approval_required: bool)
        """
        # 1. Reject blocking critical infrastructure / loopback
        if action.type == "block_ip" and action.target in cls.PROTECTED_IPS:
            return False, f"Constraint violation: Target IP {action.target} is in PROTECTED_IPS list", False

        # 2. Check if action requires mandatory human operator approval
        if action.type in cls.HUMAN_APPROVAL_ACTIONS or action.target in cls.HUMAN_APPROVAL_ACTIONS:
            return False, "Dangerous action rejected by safety constraints", True

        if action.type == "isolate_service" and action.scope == "database" and severity == "CRITICAL":
            return True, "Database quarantine requires mandatory Human-in-the-Loop confirmation", True

        # 3. Check TTL bounds (max 24 hours for automated rules)
        if action.ttl > 86400:
            return False, "Constraint violation: TTL exceeds maximum autonomous duration (86400s)", False

        return True, "Action satisfies all safety invariants and bounds", False
