import React, { useState } from "react";
import { Terminal, ShieldAlert, Info } from "lucide-react";
import { SecurityEvent } from "../types/events";

interface ThreatFeedProps {
  events: SecurityEvent[];
}

export const ThreatFeed: React.FC<ThreatFeedProps> = ({ events }) => {
  const [filterSeverity, setFilterSeverity] = useState<string>("ALL");

  const filteredEvents = events.filter((e) => {
    if (filterSeverity === "ALL") return true;
    return e.severity === filterSeverity;
  });

  return (
    <div className="glass-panel rounded-2xl flex flex-col h-[500px] overflow-hidden">
      {/* Frosted Glass Header */}
      <div className="p-3.5 bg-cyber-panel/60 backdrop-blur-xl border-b border-cyber-border/80 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-lg bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border">
            <Terminal className="w-3.5 h-3.5 text-cyber-neon" />
          </div>
          <h3 className="text-xs font-bold font-mono tracking-wider text-emerald-200 uppercase">
            Live Telemetry &amp; Ingress Threat Stream
          </h3>
          <span className="text-[10px] font-mono px-2 py-0.5 bg-cyber-pitch/80 text-cyber-neon rounded-full border border-cyber-neon/30 font-extrabold shadow-sm shadow-cyber-neon/10">
            {events.length} Live
          </span>
        </div>

        {/* Severity Filter Glass Buttons */}
        <div className="flex items-center gap-1 text-[10px] font-mono bg-cyber-pitch/60 p-1 rounded-xl border border-cyber-border">
          {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map((sev) => (
            <button
              key={sev}
              onClick={() => setFilterSeverity(sev)}
              className={`px-2.5 py-0.5 rounded-lg transition-all ${
                filterSeverity === sev
                  ? "bg-cyber-neon text-black font-black shadow-sm shadow-cyber-neon/30"
                  : "text-cyber-textMuted hover:text-emerald-100 hover:bg-cyber-panel/60"
              }`}
            >
              {sev}
            </button>
          ))}
        </div>
      </div>

      {/* Stream List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 font-mono text-[11px]">
        {filteredEvents.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-cyber-textMuted gap-2">
            <Info className="w-7 h-7 text-cyber-dim" />
            <span className="text-xs">Awaiting telemetry signals from traffic collector...</span>
          </div>
        ) : (
          filteredEvents.map((evt) => {
            const isCritical = evt.severity === "CRITICAL";
            const isHigh = evt.severity === "HIGH";
            const isMedium = evt.severity === "MEDIUM";

            let badgeColor = "bg-cyber-panel/80 text-cyber-neon border-cyber-border";
            let borderClass = "border-cyber-border/80";

            if (isCritical) {
              badgeColor = "bg-red-950/90 text-cyber-crimson border-red-500 font-extrabold shadow-sm shadow-red-500/20";
              borderClass = "border-red-500/40 bg-red-950/20";
            } else if (isHigh) {
              badgeColor = "bg-amber-950/90 text-cyber-amber border-amber-500 font-extrabold shadow-sm shadow-amber-500/20";
              borderClass = "border-amber-500/40 bg-amber-950/20";
            } else if (isMedium) {
              badgeColor = "bg-blue-950/90 text-blue-300 border-blue-500 font-extrabold";
              borderClass = "border-blue-500/30";
            }

            return (
              <div
                key={evt.event_id}
                className={`glass-card p-3 rounded-xl transition-all flex flex-col gap-1.5 ${borderClass}`}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-cyber-textMuted text-[10px]">
                      {new Date(evt.timestamp).toLocaleTimeString()}
                    </span>
                    <span className={`px-2 py-0.2 rounded-full border text-[9px] uppercase ${badgeColor}`}>
                      {evt.severity}
                    </span>
                    <span className="px-2 py-0.2 bg-cyber-pitch/80 rounded-md border border-cyber-border text-cyber-neon text-[10px] font-bold">
                      {evt.target_service}
                    </span>
                    <span className="text-emerald-100 font-bold">
                      {evt.source_ip}
                    </span>
                  </div>

                  <div className="flex items-center gap-2.5">
                    <span className="text-cyber-textMuted text-[10px]">
                      Score: <strong className={evt.threat_score >= 60 ? "text-cyber-crimson font-black" : "text-emerald-200"}>{evt.threat_score}</strong>
                    </span>
                    <span className="text-cyber-textMuted text-[10px]">
                      ML: {(evt.anomaly_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>

                <div className="text-emerald-100 text-xs pl-2 border-l-2 border-cyber-neon/50 font-mono">
                  {evt.description || `Observed ${evt.event_type} event`}
                </div>

                {evt.suricata_alert && (
                  <div className="text-[10px] text-amber-300 bg-amber-950/40 px-2.5 py-1 rounded-lg border border-amber-900/60 flex items-center gap-1.5">
                    <ShieldAlert className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                    <span>{evt.suricata_alert.msg} [SID: {evt.suricata_alert.sid}]</span>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
