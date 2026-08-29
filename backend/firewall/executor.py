import platform
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from backend.models.schemas import FirewallRule, FirewallLayer, ServiceId
from backend.firewall.generator import FirewallRuleGenerator

class FirewallExecutor:
    """Manages active rules table, 30-layer status, diff generation, and execution."""

    def __init__(self):
        self.is_linux = platform.system().lower() == "linux"
        self.active_rules: Dict[str, FirewallRule] = {}
        self.rule_history: List[Dict[str, Any]] = []
        self.layers: Dict[int, FirewallLayer] = {l.layer_id: l for l in FirewallRuleGenerator.get_all_layers()}

    def apply_rule(self, rule: FirewallRule) -> Dict[str, Any]:
        """Applies rule to active table and updates 30-layer deep defense telemetry."""
        before_state = list(self.active_rules.keys())

        # Store in active table
        self.active_rules[rule.rule_id] = rule

        # Update layer status
        layer = self.layers.get(rule.layer_number)
        if layer:
            layer.status = "FILTERING"
            layer.active_filters += 1
            layer.last_intercept = datetime.utcnow().isoformat()

        # If on Linux with root, try applying actual nftables command
        sys_status = "EMULATED_VIRTUAL_FIREWALL"
        if self.is_linux and rule.nft_syntax.startswith("nft"):
            try:
                # Attempt real system execution
                res = subprocess.run(rule.nft_syntax, shell=True, capture_output=True, text=True, timeout=2)
                sys_status = "NFTABLES_SYSTEM_APPLIED" if res.returncode == 0 else f"NFTABLES_ERR: {res.stderr.strip()}"
            except Exception as e:
                sys_status = f"SYSTEM_EXEC_EXCEPTION: {str(e)}"

        after_state = list(self.active_rules.keys())

        diff_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "rule_id": rule.rule_id,
            "action": "RULE_ADDED",
            "service_scope": rule.service_scope,
            "layer_number": rule.layer_number,
            "layer_name": rule.layer_name,
            "nft_syntax": rule.nft_syntax,
            "system_execution_status": sys_status,
            "before_count": len(before_state),
            "after_count": len(after_state)
        }
        self.rule_history.append(diff_record)

        return diff_record

    def remove_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        rule = self.active_rules.pop(rule_id, None)
        if not rule:
            return None

        layer = self.layers.get(rule.layer_number)
        if layer:
            layer.active_filters = max(0, layer.active_filters - 1)
            if layer.active_filters == 0:
                layer.status = "ACTIVE"

        diff_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "rule_id": rule.rule_id,
            "action": "RULE_EXPIRED_OR_REVERTED",
            "service_scope": rule.service_scope,
            "layer_number": rule.layer_number,
            "layer_name": rule.layer_name,
            "nft_syntax": f"# Reverted: {rule.nft_syntax}"
        }
        self.rule_history.append(diff_record)
        return diff_record

    def get_active_rules(self) -> List[FirewallRule]:
        return list(self.active_rules.values())

    def get_layers_status(self) -> List[FirewallLayer]:
        return list(self.layers.values())

    def get_rule_history(self) -> List[Dict[str, Any]]:
        return self.rule_history[-50:]

    def reset(self):
        self.active_rules.clear()
        self.rule_history.clear()
        self.layers = {l.layer_id: l for l in FirewallRuleGenerator.get_all_layers()}
