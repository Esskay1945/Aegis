export type ServiceId = "ssh_server" | "api_server" | "web_server" | "database";
export type AttackClassType = "brute_force" | "port_scan" | "api_flood" | "cred_compromise" | "apt_campaign" | "none";
export type SeverityType = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface SecurityEvent {
  event_id: string;
  timestamp: string;
  source_ip: string;
  target_service: ServiceId;
  event_type: string;
  raw_data: Record<string, any>;
  suricata_alert?: Record<string, any>;
  anomaly_score: number;
  threat_score: number;
  severity: SeverityType;
  description: string;
}

export interface DefenseAction {
  action_id: string;
  type: string;
  target: string;
  scope: ServiceId;
  ttl: number;
  threshold?: string;
  credential_id?: string;
  reason: string;
  layer_target?: number;
}

export interface AIAnalysisResult {
  analysis_id: string;
  timestamp: string;
  trigger_event_ids: string[];
  attack_class: AttackClassType;
  confidence: number;
  severity: SeverityType;
  evidence: string[];
  affected_services: ServiceId[];
  recommended_actions: DefenseAction[];
  explanation: string;
  blast_radius: string;
  auto_execute_eligible: boolean;
}

export interface ActionValidationResult {
  action: DefenseAction;
  verdict: "APPROVED" | "BLOCKED" | "HELD_FOR_APPROVAL";
  reason: string;
  executed: boolean;
  execution_result?: string;
}

export interface PolicyDecision {
  analysis_id: string;
  timestamp: string;
  actions_validated: ActionValidationResult[];
  actions_blocked: ActionValidationResult[];
  human_approval_required: boolean;
  execution_timestamp?: string;
  summary: string;
}

export interface FirewallLayer {
  layer_id: number;
  name: string;
  category: string;
  status: "ACTIVE" | "FILTERING" | "MONITORING" | "BYPASS";
  active_filters: number;
  last_intercept?: string;
  description: string;
}

export interface FirewallRule {
  rule_id: string;
  table: string;
  chain: string;
  layer_number: number;
  layer_name: string;
  service_scope: ServiceId;
  source_ip?: string;
  port?: number;
  action: string;
  rate_limit?: string;
  ttl_seconds: number;
  created_at: string;
  expires_at?: string;
  active: boolean;
  nft_syntax: string;
}

export interface ServiceStatus {
  service_id: ServiceId;
  name: string;
  port: number;
  status: "HEALTHY" | "UNDER_ATTACK" | "MITIGATED" | "ISOLATED";
  threat_score: number;
  active_connections: number;
  requests_per_min: number;
  failed_auth_count: number;
  current_credential_version: string;
  active_policies: string[];
  is_quarantined: boolean;
  last_updated: string;
}

export interface CredentialRecord {
  credential_id: string;
  service_id: ServiceId;
  version: string;
  status: "ACTIVE" | "REVOKED" | "ROTATING";
  created_at: string;
  revoked_at?: string;
  new_version_id?: string;
  trigger: string;
}

export interface AuditLogEntry {
  log_id: string;
  timestamp: string;
  entry_type: "detection" | "ai_decision" | "policy_verdict" | "action_executed" | "credential_rotation" | "recovery" | "tamper_alert";
  content: Record<string, any>;
  previous_hash: string;
  current_hash: string;
}

export interface GlobalMetrics {
  total_events_processed: number;
  threats_detected: number;
  autonomous_mitigations_executed: number;
  credentials_rotated: number;
  avg_response_time_ms: number;
  audit_integrity_pass: boolean;
}
