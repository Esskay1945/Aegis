import React from "react";
import { Key, RefreshCw, ShieldCheck } from "lucide-react";
import { CredentialRecord } from "../types/events";

interface CredentialEventLogProps {
  credentials: CredentialRecord[];
}

export const CredentialEventLog: React.FC<CredentialEventLogProps> = ({ credentials }) => {
  return (
    <div className="glass-panel rounded-2xl flex flex-col h-[360px] overflow-hidden">
      <div className="p-3.5 bg-cyber-panel/60 backdrop-blur-xl border-b border-cyber-border/80 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-lg bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border">
            <Key className="w-3.5 h-3.5 text-cyber-purple" />
          </div>
          <h3 className="text-xs font-bold font-mono tracking-wider text-emerald-200 uppercase">
            Autonomous Credential &amp; Key Engine
          </h3>
        </div>
        <span className="text-[10px] font-mono px-2.5 py-0.5 bg-cyber-pitch/80 text-purple-400 rounded-full border border-purple-500/40 font-extrabold shadow-sm shadow-purple-500/10">
          Vault KMS
        </span>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-3 font-mono text-xs">
        {credentials.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-cyber-textMuted gap-2">
            <ShieldCheck className="w-6 h-6 text-cyber-purple" />
            <span>All service credentials in primary V1 baseline state.</span>
          </div>
        ) : (
          credentials.map((cred, idx) => {
            const isRevoked = cred.status === "REVOKED";

            return (
              <div
                key={idx}
                className={`glass-card p-3 rounded-xl transition-all flex flex-col gap-2 ${
                  isRevoked
                    ? "opacity-60 border-cyber-border"
                    : "border-purple-500/40 shadow-sm shadow-purple-500/10"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-white font-bold">{cred.service_id.toUpperCase()}</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold border ${
                      isRevoked ? "bg-red-950/80 text-cyber-crimson border-red-800" : "bg-cyber-panel/90 text-cyber-neon border-cyber-neon/80"
                    }`}>
                      {cred.version} ({cred.status})
                    </span>
                  </div>

                  <span className="text-[10px] text-cyber-textMuted">
                    {new Date(cred.created_at).toLocaleTimeString()}
                  </span>
                </div>

                <div className="text-[11px] text-cyber-textMuted flex items-center justify-between">
                  <span>Key ID: <strong className="text-purple-300">{cred.credential_id}</strong></span>
                  <span className="text-[10px] text-cyber-textMuted">{cred.trigger}</span>
                </div>

                {cred.new_version_id && (
                  <div className="text-[10px] text-cyber-neon bg-cyber-pitch/80 px-2.5 py-1.5 rounded-lg border border-cyber-neon/40 flex items-center gap-2 font-bold shadow-inner">
                    <RefreshCw className="w-3.5 h-3.5 text-cyber-neon animate-spin" />
                    <span>Rotated &amp; Promoted To: <strong>{cred.new_version_id}</strong></span>
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
