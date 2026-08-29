import React from "react";
import { ShieldAlert, PlusCircle, MinusCircle, Terminal, Clock, CheckCircle2 } from "lucide-react";
import { FirewallRule } from "../types/events";

interface FirewallRuleDiffProps {
  activeRules: FirewallRule[];
  ruleDiffs: any[];
}

export const FirewallRuleDiff: React.FC<FirewallRuleDiffProps> = ({ activeRules, ruleDiffs }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      
      {/* Active nftables Rule Table */}
      <div className="glass-panel rounded-2xl flex flex-col h-[360px] overflow-hidden">
        <div className="p-3.5 bg-cyber-panel/60 backdrop-blur-xl border-b border-cyber-border/80 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-6 h-6 rounded-lg bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border">
              <Terminal className="w-3.5 h-3.5 text-cyber-neon" />
            </div>
            <h3 className="text-xs font-bold font-mono tracking-wider text-emerald-200 uppercase">
              Active nftables / Dynamic Rulebase ({activeRules.length})
            </h3>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 bg-cyber-pitch/80 text-cyber-neon rounded-full border border-cyber-neon/30 font-extrabold shadow-sm shadow-cyber-neon/10">
            Per-Service Scoped
          </span>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2 font-mono text-[11px]">
          {activeRules.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-cyber-textMuted gap-2">
              <CheckCircle2 className="w-6 h-6 text-cyber-neon/80" />
              <span>Standard baseline firewall state. Zero active quarantine drops.</span>
            </div>
          ) : (
            activeRules.map((rule) => (
              <div
                key={rule.rule_id}
                className="glass-card p-3 rounded-xl flex flex-col gap-2 shadow-sm border-cyber-neon/30"
              >
                <div className="flex items-center justify-between text-[10px]">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-md bg-cyber-pitch text-cyber-neon border border-cyber-neon/40 font-extrabold">
                      L{rule.layer_number}
                    </span>
                    <span className="text-white font-bold">{rule.service_scope}</span>
                    <span className="text-cyber-textMuted">Port {rule.port}</span>
                  </div>

                  <div className="flex items-center gap-1.5 text-cyber-textMuted">
                    <Clock className="w-3 h-3 text-cyber-neon" />
                    <span>TTL: {rule.ttl_seconds}s</span>
                  </div>
                </div>

                <div className="bg-cyber-pitch/80 backdrop-blur-md p-2.5 rounded-lg border border-cyber-border text-cyber-neon text-xs overflow-x-auto whitespace-pre font-mono shadow-inner">
                  <code>{rule.nft_syntax}</code>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Real-time Before/After Rule Diff Log */}
      <div className="glass-panel rounded-2xl flex flex-col h-[360px] overflow-hidden">
        <div className="p-3.5 bg-cyber-panel/60 backdrop-blur-xl border-b border-cyber-border/80 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-6 h-6 rounded-lg bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border">
              <ShieldAlert className="w-3.5 h-3.5 text-cyber-amber" />
            </div>
            <h3 className="text-xs font-bold font-mono tracking-wider text-emerald-200 uppercase">
              Autonomous Rule Diff Provenance
            </h3>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 bg-cyber-pitch/80 text-cyber-textMuted rounded-full border border-cyber-border font-bold">
            Audit Stream
          </span>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2 font-mono text-[11px]">
          {ruleDiffs.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-cyber-textMuted">
              <span>No dynamic policy adaptations recorded yet.</span>
            </div>
          ) : (
            ruleDiffs.map((diff, i) => {
              const isAdded = diff.action === "RULE_ADDED";
              return (
                <div
                  key={i}
                  className="glass-card p-2.5 rounded-xl flex flex-col gap-1.5"
                >
                  <div className="flex items-center justify-between text-[10px]">
                    <div className="flex items-center gap-1.5">
                      {isAdded ? (
                        <PlusCircle className="w-3.5 h-3.5 text-cyber-neon" />
                      ) : (
                        <MinusCircle className="w-3.5 h-3.5 text-cyber-amber" />
                      )}
                      <span className={`font-black ${isAdded ? "text-cyber-neon" : "text-cyber-amber"}`}>
                        {diff.action}
                      </span>
                      <span className="text-cyber-textMuted">•</span>
                      <span className="text-emerald-300">L{diff.layer_number} {diff.layer_name}</span>
                    </div>
                    <span className="text-cyber-textMuted">
                      {new Date(diff.timestamp).toLocaleTimeString()}
                    </span>
                  </div>

                  <div className="text-emerald-100 text-xs font-mono bg-cyber-pitch/70 p-2 rounded-lg border border-cyber-border truncate">
                    <code>{diff.nft_syntax}</code>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

    </div>
  );
};
