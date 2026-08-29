import { useState, useEffect, useRef, useCallback } from "react";
import {
  SecurityEvent,
  AIAnalysisResult,
  PolicyDecision,
  FirewallLayer,
  FirewallRule,
  ServiceStatus,
  CredentialRecord,
  GlobalMetrics
} from "../types/events";

export function useAegisWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [services, setServices] = useState<Record<string, ServiceStatus>>({
    ssh_server: { service_id: "ssh_server", name: "Secure Shell (SSH)", port: 22, status: "HEALTHY", threat_score: 5, active_connections: 4, requests_per_min: 8, failed_auth_count: 0, current_credential_version: "V1", active_policies: [], is_quarantined: false, last_updated: "" },
    api_server: { service_id: "api_server", name: "Core REST API", port: 8000, status: "HEALTHY", threat_score: 5, active_connections: 12, requests_per_min: 45, failed_auth_count: 0, current_credential_version: "V1", active_policies: [], is_quarantined: false, last_updated: "" },
    web_server: { service_id: "web_server", name: "Web Application (Nginx)", port: 80, status: "HEALTHY", threat_score: 5, active_connections: 28, requests_per_min: 80, failed_auth_count: 0, current_credential_version: "V1", active_policies: [], is_quarantined: false, last_updated: "" },
    database: { service_id: "database", name: "PostgreSQL Cluster", port: 5432, status: "HEALTHY", threat_score: 5, active_connections: 6, requests_per_min: 15, failed_auth_count: 0, current_credential_version: "V1", active_policies: [], is_quarantined: false, last_updated: "" }
  });

  const [layers, setLayers] = useState<FirewallLayer[]>([]);
  const [activeRules, setActiveRules] = useState<FirewallRule[]>([]);
  const [ruleDiffs, setRuleDiffs] = useState<any[]>([]);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [analyses, setAnalyses] = useState<AIAnalysisResult[]>([]);
  const [decisions, setDecisions] = useState<PolicyDecision[]>([]);
  const [credentials, setCredentials] = useState<CredentialRecord[]>([]);
  const [metrics, setMetrics] = useState<GlobalMetrics>({
    total_events_processed: 0,
    threats_detected: 0,
    autonomous_mitigations_executed: 0,
    credentials_rotated: 0,
    avg_response_time_ms: 1.4,
    audit_integrity_pass: true
  });
  const [simulationRunning, setSimulationRunning] = useState(false);
  const [currentScenario, setCurrentScenario] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const connect = useCallback(() => {
    try {
      const wsUrl = window.location.hostname === "localhost" 
        ? "ws://localhost:8000/ws" 
        : `ws://${window.location.host}/ws`;
        
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (evt) => {
        try {
          const msg = JSON.parse(evt.data);
          const { type, data } = msg;

          if (type === "INITIAL_SNAPSHOT") {
            if (data.services) setServices(data.services);
            if (data.layers) setLayers(data.layers);
            if (data.active_rules) setActiveRules(data.active_rules);
            if (data.rule_diffs) setRuleDiffs(data.rule_diffs);
            if (data.recent_events) setEvents(data.recent_events);
            if (data.recent_analyses) setAnalyses(data.recent_analyses);
            if (data.metrics) setMetrics(data.metrics);
            setSimulationRunning(data.simulation_running || false);
            setCurrentScenario(data.current_scenario || null);
          } else if (type === "SECURITY_EVENT") {
            setEvents((prev) => [data, ...prev.slice(0, 49)]);
            setMetrics((prev) => ({
              ...prev,
              total_events_processed: prev.total_events_processed + 1
            }));
          } else if (type === "AI_ANALYSIS") {
            setAnalyses((prev) => [data, ...prev.slice(0, 19)]);
            setMetrics((prev) => ({
              ...prev,
              threats_detected: prev.threats_detected + 1
            }));
          } else if (type === "POLICY_DECISION") {
            setDecisions((prev) => [data, ...prev.slice(0, 19)]);
          } else if (type === "FIREWALL_DIFF") {
            setRuleDiffs((prev) => [data, ...prev.slice(0, 29)]);
            setMetrics((prev) => ({
              ...prev,
              autonomous_mitigations_executed: prev.autonomous_mitigations_executed + 1
            }));
          } else if (type === "ACTIVE_RULES") {
            setActiveRules(data);
          } else if (type === "LAYERS_UPDATE") {
            setLayers(data);
          } else if (type === "CREDENTIAL_ROTATED") {
            setCredentials((prev) => [data, ...prev]);
            setMetrics((prev) => ({
              ...prev,
              credentials_rotated: prev.credentials_rotated + 1
            }));
          } else if (type === "SERVICES_STATUS") {
            setServices(data);
          } else if (type === "SYSTEM_RESET") {
            setEvents([]);
            setAnalyses([]);
            setDecisions([]);
            setActiveRules([]);
            setRuleDiffs([]);
            setCredentials([]);
          }
        } catch (e) {
          console.error("Error parsing WebSocket message:", e);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        reconnectTimeoutRef.current = window.setTimeout(() => {
          connect();
        }, 2000);
      };

      ws.onerror = () => {
        ws.close();
      };
    } catch (err) {
      console.error("WebSocket connection error:", err);
      reconnectTimeoutRef.current = window.setTimeout(() => {
        connect();
      }, 2000);
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (wsRef.current) wsRef.current.close();
    };
  }, [connect]);

  return {
    isConnected,
    services,
    layers,
    activeRules,
    ruleDiffs,
    events,
    analyses,
    decisions,
    credentials,
    metrics,
    simulationRunning,
    currentScenario
  };
}
