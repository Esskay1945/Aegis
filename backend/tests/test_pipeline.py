import unittest
import asyncio
from backend.models.schemas import RawEvent
from backend.detection.normalizer import EventNormalizer
from backend.agents.reasoner import AIReasoner
from backend.policy.engine import PolicyEngine
from backend.firewall.generator import FirewallRuleGenerator
from backend.firewall.executor import FirewallExecutor
from backend.credentials.rotator import CredentialEngine
from backend.audit.logger import AuditLogger
from backend.audit.verifier import AuditVerifier

class TestAegisPipeline(unittest.TestCase):

    def setUp(self):
        self.normalizer = EventNormalizer()
        self.firewall = FirewallExecutor()
        self.credentials = CredentialEngine()
        self.audit = AuditLogger()

    def test_brute_force_closed_loop(self):
        """Tests end-to-end SSH brute force detection, policy validation, and rule generation."""
        # 1. Simulate 12 failed logins
        ip = "192.168.1.150"
        for i in range(12):
            raw = RawEvent(
                source_ip=ip,
                target_service="ssh_server",
                event_type="auth_failure",
                raw_data={"username": f"user_{i}", "port": 22}
            )
            sec_event, features, rule_result = self.normalizer.process_raw_event(raw)

        # 2. Verify Rule Trigger & Anomaly Score
        self.assertEqual(rule_result[0], "brute_force")
        self.assertGreaterEqual(rule_result[1], 0.85)
        self.assertGreaterEqual(sec_event.threat_score, 60)

        # 3. AI Reasoning
        analysis = AIReasoner.analyze(sec_event, features, rule_result)
        self.assertEqual(analysis.attack_class, "brute_force")
        self.assertGreaterEqual(len(analysis.recommended_actions), 2)

        # 4. Policy Engine Gating
        decision = PolicyEngine.evaluate(analysis)
        self.assertGreater(len(decision.actions_validated), 0)
        self.assertFalse(decision.human_approval_required)

        # 5. Firewall & Credential Execution
        for item in decision.actions_validated:
            if item.verdict == "APPROVED":
                if item.action.type in ["block_ip", "rate_limit"]:
                    rule = FirewallRuleGenerator.generate_rule(item.action)
                    diff = self.firewall.apply_rule(rule)
                    self.assertIn("inet aegis_filter", diff["nft_syntax"])
                elif item.action.type == "rotate_credential":
                    cred = self.credentials.rotate_credential("ssh_server", item.action.reason)
                    self.assertEqual(cred.version, "V2")

        # 6. Audit Logging & Verification
        self.audit.log_event("ai_decision", analysis.model_dump())
        self.audit.log_event("policy_verdict", decision.model_dump())
        verification = AuditVerifier.verify_chain(self.audit.chain)
        self.assertTrue(verification["is_valid"])

    def test_thirty_layers_generation(self):
        """Verifies that all 30 layers are properly initialized and queryable."""
        layers = self.firewall.get_layers_status()
        self.assertEqual(len(layers), 30)
        categories = {l.category for l in layers}
        self.assertIn("Network & Transport", categories)
        self.assertIn("Identity & Access", categories)
        self.assertIn("API & Protocol", categories)
        self.assertIn("OS & Kernel", categories)
        self.assertIn("AI & Semantic", categories)
        self.assertIn("Cryptographic & State", categories)

    def test_audit_tamper_detection(self):
        """Verifies that tampering with historical audit blocks is caught immediately."""
        self.audit.log_event("detection", {"data": "authentic"})
        self.audit.log_event("detection", {"data": "authentic"})
        
        # Valid state
        res = AuditVerifier.verify_chain(self.audit.chain)
        self.assertTrue(res["is_valid"])

        # Tamper with block 1
        self.audit.chain[1].content["data"] = "tampered_by_attacker"
        
        # Invalid state
        tampered_res = AuditVerifier.verify_chain(self.audit.chain)
        self.assertFalse(tampered_res["is_valid"])
        self.assertEqual(tampered_res["tamper_detected_at_index"], 1)

if __name__ == "__main__":
    unittest.main()
