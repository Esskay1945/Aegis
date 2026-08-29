from datetime import datetime
from typing import List, Dict, Any
from backend.firewall.executor import FirewallExecutor

class FirewallRollback:
    """Manages TTL-based rule expiration and baseline firewall rollbacks."""

    def __init__(self, executor: FirewallExecutor):
        self.executor = executor

    def check_expired_rules(self) -> List[Dict[str, Any]]:
        now = datetime.utcnow()
        expired_diffs = []
        for rule_id, rule in list(self.executor.active_rules.items()):
            if rule.expires_at:
                exp_dt = datetime.fromisoformat(rule.expires_at)
                if now >= exp_dt:
                    diff = self.executor.remove_rule(rule_id)
                    if diff:
                        expired_diffs.append(diff)
        return expired_diffs

    def rollback_all_service_rules(self, service_id: str) -> List[Dict[str, Any]]:
        reverted = []
        for rule_id, rule in list(self.executor.active_rules.items()):
            if rule.service_scope == service_id:
                diff = self.executor.remove_rule(rule_id)
                if diff:
                    reverted.append(diff)
        return reverted

    def rollback_all(self) -> List[Dict[str, Any]]:
        reverted = []
        for rule_id in list(self.executor.active_rules.keys()):
            diff = self.executor.remove_rule(rule_id)
            if diff:
                reverted.append(diff)
        return reverted
