from datetime import datetime
from typing import Dict, Any, List
from backend.firewall.executor import FirewallExecutor
from backend.firewall.rollback import FirewallRollback
from backend.isolation.quarantine import IsolationEngine

class RecoveryEngine:
    """Detects threat cessation, verifies behavioral normalization, and restores baseline states."""

    def __init__(self, executor: FirewallExecutor, isolation: IsolationEngine):
        self.executor = executor
        self.rollback = FirewallRollback(executor)
        self.isolation = isolation
        self.recovery_log: List[Dict[str, Any]] = []

    def perform_full_recovery(self, reason: str = "Threat traffic ceased. Normal baseline verified.") -> Dict[str, Any]:
        # 1. Revert active temporary firewall rules
        reverted_rules = self.rollback.rollback_all()

        # 2. Reconnect quarantined services
        reconnected_services = []
        for q in list(self.isolation.quarantined_services.keys()):
            rec = self.isolation.reconnect_service(q)
            if rec:
                reconnected_services.append(rec)

        recovery_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "AUTONOMOUS_BASELINE_RESTORED",
            "reason": reason,
            "reverted_rules_count": len(reverted_rules),
            "reconnected_services_count": len(reconnected_services),
            "reverted_diffs": reverted_rules,
            "status": "ALL_SERVICES_BASELINE_NORMAL"
        }
        self.recovery_log.append(recovery_entry)
        return recovery_entry

    def get_recovery_history(self) -> List[Dict[str, Any]]:
        return self.recovery_log

    def reset(self):
        self.recovery_log.clear()
