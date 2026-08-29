from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
import uuid

# --- Core Enums & Types ---
AttackClassType = Literal["brute_force", "port_scan", "api_flood", "cred_compromise", "apt_campaign", "none"]
SeverityType = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
ServiceId = Literal["ssh_server", "api_server", "web_server", "database"]
ActionType = Literal["block_ip", "rate_limit", "isolate_service", "rotate_credential", "port_restrict", "custom_rule"]
VerdictType = Literal["APPROVED", "BLOCKED", "HELD_FOR_APPROVAL"]

# --- Event Models ---
class RawEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    source_ip: str
    target_service: ServiceId
    event_type: str
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    suricata_alert: Optional[Dict[str, Any]] = None

class SecurityEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    source_ip: str
    target_service: ServiceId
    event_type: str
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    suricata_alert: Optional[Dict[str, Any]] = None
    anomaly_score: float = 0.0
    threat_score: int = 0
    severity: SeverityType = "LOW"
    description: str = ""

# --- Action & Recommendation Models ---
class DefenseAction(BaseModel):
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ActionType
    target: str
    scope: ServiceId
    ttl: int = 3600  # seconds
    threshold: Optional[str] = None
    credential_id: Optional[str] = None
    reason: str = ""
    layer_target: Optional[int] = None

class AIAnalysisResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    trigger_event_ids: List[str] = Field(default_factory=list)
    attack_class: AttackClassType
    confidence: float
    severity: SeverityType
    evidence: List[str] = Field(default_factory=list)
    affected_services: List[ServiceId] = Field(default_factory=list)
    recommended_actions: List[DefenseAction] = Field(default_factory=list)
    explanation: str
    blast_radius: str = "Confined to single service endpoint"
    auto_execute_eligible: bool = True

# --- Policy Engine Models ---
class ActionValidationResult(BaseModel):
    action: DefenseAction
    verdict: VerdictType
    reason: str
    executed: bool = False
    execution_result: Optional[str] = None

class PolicyDecision(BaseModel):
    analysis_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    actions_validated: List[ActionValidationResult] = Field(default_factory=list)
    actions_blocked: List[ActionValidationResult] = Field(default_factory=list)
    human_approval_required: bool = False
    execution_timestamp: Optional[str] = None
    summary: str = ""

# --- 30-Layer Firewall Models ---
class FirewallLayer(BaseModel):
    layer_id: int
    name: str
    category: str
    status: Literal["ACTIVE", "FILTERING", "MONITORING", "BYPASS"]
    active_filters: int
    last_intercept: Optional[str] = None
    description: str

class FirewallRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    table: str = "inet aegis_filter"
    chain: str = "input"
    layer_number: int = 3
    layer_name: str = "Network Filtering"
    service_scope: ServiceId
    source_ip: Optional[str] = None
    port: Optional[int] = None
    action: str = "drop"
    rate_limit: Optional[str] = None
    ttl_seconds: int = 3600
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    expires_at: Optional[str] = None
    active: bool = True
    nft_syntax: str = ""

# --- Service State Models ---
class ServiceStatus(BaseModel):
    service_id: ServiceId
    name: str
    port: int
    status: Literal["HEALTHY", "UNDER_ATTACK", "MITIGATED", "ISOLATED"]
    threat_score: int = 0
    active_connections: int = 0
    requests_per_min: int = 0
    failed_auth_count: int = 0
    current_credential_version: str = "V1"
    active_policies: List[str] = Field(default_factory=list)
    is_quarantined: bool = False
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# --- Credential Models ---
class CredentialRecord(BaseModel):
    credential_id: str
    service_id: ServiceId
    version: str
    status: Literal["ACTIVE", "REVOKED", "ROTATING"]
    created_at: str
    revoked_at: Optional[str] = None
    new_version_id: Optional[str] = None
    trigger: str = ""

# --- Audit Log Models ---
class AuditLogEntry(BaseModel):
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    entry_type: Literal["detection", "ai_decision", "policy_verdict", "action_executed", "credential_rotation", "recovery", "tamper_alert"]
    content: Dict[str, Any]
    previous_hash: str
    current_hash: str

# --- Simulation Models ---
class SimulationCommand(BaseModel):
    scenario: Literal["ssh_brute_force", "port_scan", "api_flood", "cred_compromise", "apt_chain", "threat_clearance", "reset"]
    duration_seconds: int = 30
    intensity: Literal["low", "medium", "high"] = "high"
    source_ip: Optional[str] = None
