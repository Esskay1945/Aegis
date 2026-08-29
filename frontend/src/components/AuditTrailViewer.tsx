import React, { useState, useEffect } from "react";
import { Lock, ShieldCheck, CheckCircle2, AlertTriangle, RefreshCw, FileCode } from "lucide-react";
import { fetchAuditLedger, verifyAuditLedger } from "../services/api";
import { AuditLogEntry } from "../types/events";

export const AuditTrailViewer: React.FC = () => {
  const [entries, setEntries] = useState<AuditLogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [verifyResult, setVerifyResult] = useState<any | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [selectedEntry, setSelectedEntry] = useState<AuditLogEntry | null>(null);

  const loadLedger = async () => {
    try {
      setIsLoading(true);
      const data = await fetchAuditLedger();
      setEntries(data.entries || []);
    } catch (err) {
      console.error("Failed to load audit ledger:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerify = async () => {
    try {
      setIsVerifying(true);
      const res = await verifyAuditLedger();
      setVerifyResult(res);
    } catch (err) {
      console.error("Failed to verify audit ledger:", err);
    } finally {
      setIsVerifying(false);
    }
  };

  useEffect(() => {
    loadLedger();
  }, []);

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-7 border border-cyber-border flex flex-col gap-6 font-mono">
      {/* Title & Verification Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-cyber-border/80 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border shadow-inner">
              <Lock className="w-4.5 h-4.5 text-cyber-neon" />
            </div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Hash-Chained Immutable Audit Ledger
            </h2>
          </div>
          <p className="text-xs text-cyber-textMuted mt-1">
            Tamper-evident cryptographically chained record: H(n) = SHA256(H(n-1) + Timestamp + Content).
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={loadLedger}
            disabled={isLoading}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-cyber-pitch/80 hover:bg-cyber-panel text-cyber-textMuted hover:text-white text-xs border border-cyber-border transition shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin text-cyber-neon" : ""}`} />
            <span>Refresh</span>
          </button>

          <button
            onClick={handleVerify}
            disabled={isVerifying}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyber-neon hover:bg-cyber-lime text-black font-black text-xs shadow-lg shadow-cyber-neon/30 transition transform active:scale-95 border border-cyber-lime"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{isVerifying ? "Verifying Hashes..." : "Verify Chain Integrity"}</span>
          </button>
        </div>
      </div>

      {/* Verification Result Banner */}
      {verifyResult && (
        <div
          className={`p-4 rounded-2xl border flex items-center justify-between text-xs backdrop-blur-xl ${
            verifyResult.is_valid
              ? "glass-panel-glow border-cyber-neon text-cyber-neon shadow-lg shadow-cyber-neon/20"
              : "glass-panel-danger border-cyber-crimson text-cyber-crimson animate-pulse"
          }`}
        >
          <div className="flex items-center gap-3">
            {verifyResult.is_valid ? (
              <CheckCircle2 className="w-6 h-6 text-cyber-neon shrink-0" />
            ) : (
              <AlertTriangle className="w-6 h-6 text-cyber-crimson shrink-0" />
            )}
            <div>
              <span className="font-bold text-sm block font-mono">
                {verifyResult.status}
              </span>
              <span className="text-cyber-textMuted text-[11px]">
                Total Cryptographic Blocks: {verifyResult.total_blocks}
              </span>
            </div>
          </div>

          <button
            onClick={() => setVerifyResult(null)}
            className="text-cyber-textMuted hover:text-white text-xs px-2.5 py-1 bg-cyber-pitch/80 rounded-lg border border-cyber-border"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Chain Block Explorer */}
      <div className="space-y-3">
        {entries.map((entry, idx) => (
          <div
            key={entry.log_id}
            onClick={() => setSelectedEntry(entry)}
            className="p-3.5 glass-card rounded-xl hover:border-cyber-neon/50 cursor-pointer transition text-xs flex flex-col gap-2.5"
          >
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-cyber-pitch text-cyber-neon border border-cyber-neon/80 font-black shadow-sm shadow-cyber-neon/10">
                  BLOCK #{idx + 1}
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-cyber-panel text-emerald-300 border border-cyber-border uppercase text-[10px] font-bold">
                  {entry.entry_type}
                </span>
                <span className="text-cyber-textMuted text-[11px]">
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </span>
              </div>

              <span className="text-cyber-textMuted text-[10px]">ID: {entry.log_id.slice(0, 8)}...</span>
            </div>

            {/* Cryptographic Hashes */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[10px] bg-cyber-pitch/80 backdrop-blur-md p-2.5 rounded-xl border border-cyber-border/80">
              <div className="truncate">
                <span className="text-cyber-textMuted block">PREVIOUS HASH:</span>
                <span className="text-cyber-dim font-mono">{entry.previous_hash}</span>
              </div>
              <div className="truncate">
                <span className="text-cyber-textMuted block">CURRENT SHA-256 HASH:</span>
                <span className="text-cyber-neon font-mono font-bold">{entry.current_hash}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detail Inspector Modal */}
      {selectedEntry && (
        <div className="p-5 glass-panel-glow rounded-2xl text-xs flex flex-col gap-2.5 animate-in fade-in duration-200">
          <div className="flex items-center justify-between border-b border-cyber-border/80 pb-2.5">
            <div className="flex items-center gap-2.5">
              <FileCode className="w-4 h-4 text-cyber-neon" />
              <h4 className="font-bold text-white">Block Content Inspector</h4>
              <span className="text-cyber-textMuted">({selectedEntry.entry_type})</span>
            </div>
            <button
              onClick={() => setSelectedEntry(null)}
              className="text-cyber-textMuted hover:text-white px-2.5 py-1 rounded-lg bg-cyber-pitch/80 border border-cyber-border"
            >
              Close
            </button>
          </div>

          <pre className="bg-cyber-pitch/90 backdrop-blur-md p-3.5 rounded-xl text-cyber-neon text-xs overflow-x-auto max-h-[280px] border border-cyber-border shadow-inner">
            {JSON.stringify(selectedEntry.content, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};
