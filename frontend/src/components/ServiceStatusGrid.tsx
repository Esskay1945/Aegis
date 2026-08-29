import React from "react";
import { Terminal, Globe, Server, Database, Key, AlertTriangle } from "lucide-react";
import { ServiceStatus } from "../types/events";

interface ServiceStatusGridProps {
  services: Record<string, ServiceStatus>;
}

const SERVICE_ICONS: Record<string, any> = {
  ssh_server: Terminal,
  api_server: Server,
  web_server: Globe,
  database: Database
};

export const ServiceStatusGrid: React.FC<ServiceStatusGridProps> = ({ services }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      {Object.values(services).map((svc) => {
        const Icon = SERVICE_ICONS[svc.service_id] || Server;
        const isAttacked = svc.status === "UNDER_ATTACK";
        const isMitigated = svc.status === "MITIGATED";
        const isIsolated = svc.is_quarantined || svc.status === "ISOLATED";

        let panelClass = "glass-panel";
        let statusBadge = "bg-cyber-panel/90 text-cyber-neon border-cyber-border";

        if (isAttacked) {
          panelClass = "glass-panel-danger animate-pulse";
          statusBadge = "bg-red-950/90 text-cyber-crimson border-red-500 shadow-md shadow-red-500/30";
        } else if (isMitigated) {
          panelClass = "glass-panel-glow";
          statusBadge = "bg-cyber-panel/90 text-cyber-neon border-cyber-neon/80 shadow-md shadow-cyber-neon/20";
        } else if (isIsolated) {
          panelClass = "glass-panel border-purple-500/60 shadow-lg shadow-purple-500/15";
          statusBadge = "bg-purple-950/90 text-purple-300 border-purple-500";
        }

        return (
          <div
            key={svc.service_id}
            className={`${panelClass} rounded-2xl p-4.5 transition-all duration-300 relative overflow-hidden flex flex-col justify-between`}
          >
            {/* Top Row: Service Icon, Name & Status Pill */}
            <div>
              <div className="flex items-center justify-between gap-2 mb-3.5">
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-xl bg-cyber-pitch/80 backdrop-blur-md flex items-center justify-center border border-cyber-border shadow-inner">
                    <Icon className="w-4.5 h-4.5 text-cyber-neon" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white tracking-wide font-mono">{svc.name}</h3>
                    <span className="text-[11px] text-cyber-textMuted font-mono">Port {svc.port}</span>
                  </div>
                </div>

                <span className={`text-[10px] font-mono font-extrabold px-2.5 py-0.5 rounded-full border uppercase tracking-wider backdrop-blur-md ${statusBadge}`}>
                  {svc.status.replace("_", " ")}
                </span>
              </div>

              {/* Threat Gauge with Glass Track */}
              <div className="mb-3.5">
                <div className="flex items-center justify-between text-xs font-mono mb-1.5">
                  <span className="text-cyber-textMuted flex items-center gap-1.5">
                    Threat Score
                    {svc.threat_score >= 60 && <AlertTriangle className="w-3.5 h-3.5 text-cyber-crimson inline animate-bounce" />}
                  </span>
                  <span className={`font-extrabold ${svc.threat_score >= 60 ? "text-cyber-crimson" : svc.threat_score >= 30 ? "text-cyber-amber" : "text-cyber-neon"}`}>
                    {svc.threat_score} / 100
                  </span>
                </div>
                <div className="w-full bg-cyber-pitch/80 backdrop-blur-sm rounded-full h-2 overflow-hidden border border-cyber-border/80 shadow-inner">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      svc.threat_score >= 60
                        ? "bg-gradient-to-r from-amber-500 to-red-500 shadow-md shadow-red-500/60"
                        : svc.threat_score >= 30
                        ? "bg-gradient-to-r from-cyber-neon to-amber-400"
                        : "bg-cyber-neon shadow-md shadow-cyber-neon/60"
                    }`}
                    style={{ width: `${Math.min(100, Math.max(5, svc.threat_score))}%` }}
                  />
                </div>
              </div>

              {/* Glass Inset Telemetry Box */}
              <div className="grid grid-cols-2 gap-2 text-[11px] font-mono glass-card p-2.5 rounded-xl mb-3.5">
                <div>
                  <span className="text-cyber-textMuted block text-[10px] uppercase">Auth Fails (60s)</span>
                  <span className={`font-extrabold text-xs ${svc.failed_auth_count > 5 ? "text-cyber-crimson" : "text-emerald-100"}`}>
                    {svc.failed_auth_count}
                  </span>
                </div>
                <div>
                  <span className="text-cyber-textMuted block text-[10px] uppercase">Req Volume</span>
                  <span className={`font-extrabold text-xs ${svc.requests_per_min > 200 ? "text-cyber-amber" : "text-emerald-100"}`}>
                    {svc.requests_per_min} <span className="text-[10px] font-normal text-cyber-textMuted">/min</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Bottom Row: Key Version & Rule Count */}
            <div className="flex items-center justify-between text-[11px] font-mono pt-2.5 border-t border-cyber-border/60">
              <div className="flex items-center gap-1.5 text-cyber-textMuted">
                <Key className="w-3.5 h-3.5 text-cyber-purple" />
                <span>Secret: <strong className="text-purple-300 font-bold">{svc.current_credential_version}</strong></span>
              </div>

              {svc.active_policies.length > 0 ? (
                <span className="text-[10px] bg-cyber-panel/90 text-cyber-neon border border-cyber-neon/50 px-2 py-0.5 rounded-full font-extrabold shadow-sm shadow-cyber-neon/10">
                  {svc.active_policies.length} Active Rule{svc.active_policies.length > 1 ? "s" : ""}
                </span>
              ) : (
                <span className="text-[10px] text-cyber-textMuted">Baseline Rule</span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
