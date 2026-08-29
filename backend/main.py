import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.models.schemas import (
    RawEvent, SecurityEvent, AIAnalysisResult, PolicyDecision,
    ServiceStatus, SimulationCommand, ServiceId
)
from backend.detection.normalizer import EventNormalizer
from backend.agents.reasoner import AIReasoner
from backend.policy.engine import PolicyEngine
from backend.firewall.generator import FirewallRuleGenerator
from backend.firewall.executor import FirewallExecutor
from backend.firewall.rollback import FirewallRollback
from backend.isolation.quarantine import IsolationEngine
from backend.credentials.rotator import CredentialEngine
from backend.recovery.monitor import RecoveryEngine
from backend.audit.logger import AuditLogger
from backend.audit.verifier import AuditVerifier
from backend.simulation.engine import SimulationEngine
from backend.api.websocket import ws_manager

# --- Global State Orchestrator ---
class AegisOrchestrator:
    def __init__(self):
        self.normalizer = EventNormalizer()
        self.firewall_executor = FirewallExecutor()
        self.firewall_rollback = FirewallRollback(self.firewall_executor)
        self.isolation_engine = IsolationEngine()
        self.credential_engine = CredentialEngine()
        self.recovery_engine = RecoveryEngine(self.firewall_executor, self.isolation_engine)
        self.audit_logger = AuditLogger()
        self.recent_events: List[SecurityEvent] = []
        self.recent_analyses: List[AIAnalysisResult] = []
        self.recent_decisions: List[PolicyDecision] = []
        
        # Initial Service Statuses
        self.services: Dict[ServiceId, ServiceStatus] = {
            "ssh_server": ServiceStatus(service_id="ssh_server", name="Secure Shell (SSH)", port=22, status="HEALTHY"),
            "api_server": ServiceStatus(service_id="api_server", name="Core REST API", port=8000, status="HEALTHY"),
            "web_server": ServiceStatus(service_id="web_server", name="Web Application (Nginx)", port=80, status="HEALTHY"),
            "database": ServiceStatus(service_id="database", name="PostgreSQL Cluster", port=5432, status="HEALTHY")
        }

        self.simulation = SimulationEngine(event_callback=self.process_raw_event)
        self.metrics = {
            "total_events_processed": 0,
            "threats_detected": 0,
            "autonomous_mitigations_executed": 0,
            "credentials_rotated": 0,
            "avg_response_time_ms": 1.4,
            "audit_integrity_pass": True
        }

    async def process_raw_event(self, raw: RawEvent):
        t0 = time.time()
        self.metrics["total_events_processed"] += 1

        # 1. Normalization & Anomaly Detection
        sec_event, features, rule_result = self.normalizer.process_raw_event(raw)
        self.recent_events.append(sec_event)
        if len(self.recent_events) > 100:
            self.recent_events.pop(0)

        # Broadcast raw security event
        await ws_manager.broadcast("SECURITY_EVENT", sec_event.model_dump())

        # Update per-service real-time metrics
        svc = self.services.get(sec_event.target_service)
        if svc:
            svc.threat_score = max(svc.threat_score, sec_event.threat_score)
            svc.requests_per_min = int(features.get("requests_per_minute", 10))
            svc.failed_auth_count = int(features.get("login_failures_60s", 0))
            if sec_event.threat_score >= 60:
                svc.status = "UNDER_ATTACK"
            svc.last_updated = datetime.utcnow().isoformat()

        # 2. AI Reasoning Layer (Triggered if Threat Score >= 35 or rule fired)
        if sec_event.threat_score >= 35 or rule_result[0] is not None:
            self.metrics["threats_detected"] += 1
            analysis = AIReasoner.analyze(sec_event, features, rule_result)
            self.recent_analyses.append(analysis)
            if len(self.recent_analyses) > 50: self.recent_analyses.pop(0)

            await ws_manager.broadcast("AI_ANALYSIS", analysis.model_dump())
            self.audit_logger.log_event("ai_decision", analysis.model_dump())

            # 3. Policy Engine Validation (Trust Boundary)
            decision = PolicyEngine.evaluate(analysis)
            self.recent_decisions.append(decision)
            if len(self.recent_decisions) > 50: self.recent_decisions.pop(0)

            await ws_manager.broadcast("POLICY_DECISION", decision.model_dump())
            self.audit_logger.log_event("policy_verdict", decision.model_dump())

            # 4. Infrastructure Control Execution for Approved Actions
            for item in decision.actions_validated:
                if item.verdict == "APPROVED":
                    action = item.action
                    self.metrics["autonomous_mitigations_executed"] += 1

                    if action.type in ["block_ip", "rate_limit", "port_restrict"]:
                        rule = FirewallRuleGenerator.generate_rule(action)
                        diff = self.firewall_executor.apply_rule(rule)
                        item.executed = True
                        item.execution_result = diff["nft_syntax"]
                        
                        await ws_manager.broadcast("FIREWALL_DIFF", diff)
                        await ws_manager.broadcast("ACTIVE_RULES", [r.model_dump() for r in self.firewall_executor.get_active_rules()])
                        await ws_manager.broadcast("LAYERS_UPDATE", [l.model_dump() for l in self.firewall_executor.get_layers_status()])
                        self.audit_logger.log_event("action_executed", diff)

                        if svc:
                            svc.status = "MITIGATED"
                            svc.active_policies.append(f"{action.type.upper()}:{action.target}")

                    elif action.type == "rotate_credential":
                        cred = self.credential_engine.rotate_credential(action.scope, action.reason)
                        self.metrics["credentials_rotated"] += 1
                        item.executed = True
                        item.execution_result = f"Rotated {cred.credential_id} -> {cred.version}"

                        if svc:
                            svc.current_credential_version = cred.version

                        await ws_manager.broadcast("CREDENTIAL_ROTATED", cred.model_dump())
                        self.audit_logger.log_event("credential_rotation", cred.model_dump())

                    elif action.type == "isolate_service":
                        iso = self.isolation_engine.isolate_service(action.scope, action.reason)
                        item.executed = True
                        item.execution_result = f"Quarantined {action.scope} to isolated network"
                        if svc:
                            svc.is_quarantined = True
                            svc.status = "ISOLATED"

                        await ws_manager.broadcast("SERVICE_ISOLATED", iso)
                        self.audit_logger.log_event("action_executed", iso)

            # Update latency metric
            t_elapsed = (time.time() - t0) * 1000
            self.metrics["avg_response_time_ms"] = round(t_elapsed, 1)

        # Broadcast service status update
        await ws_manager.broadcast("SERVICES_STATUS", {k: v.model_dump() for k, v in self.services.items()})

    async def perform_threat_clearance(self, reason: str = "Threat neutralized. Restoring baseline."):
        # Revert firewall and isolation
        recovery_rec = self.recovery_engine.perform_full_recovery(reason)
        self.normalizer.reset()
        
        # Reset services to healthy
        for svc in self.services.values():
            svc.status = "HEALTHY"
            svc.threat_score = 10
            svc.is_quarantined = False
            svc.active_policies.clear()
            svc.last_updated = datetime.utcnow().isoformat()

        self.audit_logger.log_event("recovery", recovery_rec)
        await ws_manager.broadcast("RECOVERY_EVENT", recovery_rec)
        await ws_manager.broadcast("ACTIVE_RULES", [])
        await ws_manager.broadcast("LAYERS_UPDATE", [l.model_dump() for l in self.firewall_executor.get_layers_status()])
        await ws_manager.broadcast("SERVICES_STATUS", {k: v.model_dump() for k, v in self.services.items()})
        return recovery_rec

    def reset_all(self):
        self.normalizer.reset()
        self.firewall_executor.reset()
        self.isolation_engine.reset()
        self.credential_engine.reset()
        self.recovery_engine.reset()
        self.audit_logger.reset()
        self.recent_events.clear()
        self.recent_analyses.clear()
        self.recent_decisions.clear()
        self.metrics["threats_detected"] = 0
        self.metrics["autonomous_mitigations_executed"] = 0
        self.metrics["credentials_rotated"] = 0
        for svc in self.services.values():
            svc.status = "HEALTHY"
            svc.threat_score = 8
            svc.current_credential_version = "V1"
            svc.is_quarantined = False
            svc.active_policies.clear()

orchestrator = AegisOrchestrator()

# --- Background Task: Rule Expiry & Telemetry Normalizer ---
async def background_monitoring_loop():
    while True:
        try:
            # Check expired firewall rules
            expired = orchestrator.firewall_rollback.check_expired_rules()
            if expired:
                await ws_manager.broadcast("ACTIVE_RULES", [r.model_dump() for r in orchestrator.firewall_executor.get_active_rules()])
                await ws_manager.broadcast("LAYERS_UPDATE", [l.model_dump() for l in orchestrator.firewall_executor.get_layers_status()])

            # Slowly decay threat scores if no ongoing attack
            if not orchestrator.simulation.is_running:
                for svc in orchestrator.services.values():
                    if svc.threat_score > 12:
                        svc.threat_score = max(8, svc.threat_score - 3)
                        if svc.threat_score < 30 and svc.status == "UNDER_ATTACK":
                            svc.status = "HEALTHY"
                await ws_manager.broadcast("SERVICES_STATUS", {k: v.model_dump() for k, v in orchestrator.services.items()})
        except Exception:
            pass
        await asyncio.sleep(2.0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop_task = asyncio.create_task(background_monitoring_loop())
    yield
    loop_task.cancel()
    await orchestrator.simulation.stop_simulation()

app = FastAPI(
    title="AegisAI — Autonomous Cyber Defense API",
    description="Deterministic Trust Boundary, AI Reasoning, and 30-Layer Deep Defense Firewall",
    version="1.0.0-SIH",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- WebSocket Route ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send initial snapshot upon connection
        snapshot = {
            "services": {k: v.model_dump() for k, v in orchestrator.services.items()},
            "layers": [l.model_dump() for l in orchestrator.firewall_executor.get_layers_status()],
            "active_rules": [r.model_dump() for r in orchestrator.firewall_executor.get_active_rules()],
            "rule_diffs": orchestrator.firewall_executor.get_rule_history(),
            "recent_events": [e.model_dump() for e in orchestrator.recent_events[-20:]],
            "recent_analyses": [a.model_dump() for a in orchestrator.recent_analyses[-10:]],
            "metrics": orchestrator.metrics,
            "simulation_running": orchestrator.simulation.is_running,
            "current_scenario": orchestrator.simulation.current_scenario
        }
        await websocket.send_json({"type": "INITIAL_SNAPSHOT", "data": snapshot})

        while True:
            data = await websocket.receive_text()
            # Heartbeat ping/pong support
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# --- REST Endpoints ---
@app.get("/api/dashboard")
def get_dashboard_state():
    return {
        "services": {k: v.model_dump() for k, v in orchestrator.services.items()},
        "layers": [l.model_dump() for l in orchestrator.firewall_executor.get_layers_status()],
        "active_rules": [r.model_dump() for r in orchestrator.firewall_executor.get_active_rules()],
        "rule_diffs": orchestrator.firewall_executor.get_rule_history(),
        "recent_events": [e.model_dump() for e in orchestrator.recent_events[-30:]],
        "recent_analyses": [a.model_dump() for a in orchestrator.recent_analyses[-15:]],
        "credential_history": [c.model_dump() for c in orchestrator.credential_engine.get_rotation_history()],
        "metrics": orchestrator.metrics,
        "simulation_running": orchestrator.simulation.is_running,
        "current_scenario": orchestrator.simulation.current_scenario
    }

@app.post("/api/events/ingest")
async def ingest_event(event: RawEvent):
    await orchestrator.process_raw_event(event)
    return {"status": "INGESTED", "event_id": event.event_id}

@app.post("/api/simulation/start")
async def start_simulation(cmd: SimulationCommand):
    if cmd.scenario == "threat_clearance":
        rec = await orchestrator.perform_threat_clearance()
        return {"status": "THREAT_CLEARED", "recovery": rec}
    elif cmd.scenario == "reset":
        orchestrator.reset_all()
        await orchestrator.simulation.stop_simulation()
        await ws_manager.broadcast("SYSTEM_RESET", {})
        return {"status": "SYSTEM_RESET_COMPLETED"}

    await orchestrator.simulation.start_scenario(
        cmd.scenario,
        duration_sec=cmd.duration_seconds,
        intensity=cmd.intensity,
        custom_ip=cmd.source_ip
    )
    return {
        "status": "SIMULATION_STARTED",
        "scenario": cmd.scenario,
        "duration": cmd.duration_seconds,
        "intensity": cmd.intensity
    }

@app.post("/api/simulation/stop")
async def stop_simulation():
    await orchestrator.simulation.stop_simulation()
    return {"status": "SIMULATION_STOPPED"}

@app.get("/api/audit/ledger")
def get_audit_ledger():
    return {
        "total_entries": len(orchestrator.audit_logger.chain),
        "entries": [e.model_dump() for e in orchestrator.audit_logger.get_entries(100)]
    }

@app.get("/api/audit/verify")
def verify_audit_ledger():
    res = AuditVerifier.verify_chain(orchestrator.audit_logger.chain)
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
