import React from "react";
import { Shield, ShieldAlert, Activity, Lock, Play, RefreshCw, Radio } from "lucide-react";
import { GlobalMetrics } from "../types/events";

interface NavbarProps {
  metrics: GlobalMetrics;
  isConnected: boolean;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onQuickDemo: () => void;
  onReset: () => void;
  simulationRunning: boolean;
  currentScenario: string | null;
}

export const Navbar: React.FC<NavbarProps> = ({
  metrics,
  isConnected,
  activeTab,
  setActiveTab,
  onQuickDemo,
  onReset,
  simulationRunning,
  currentScenario
}) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-cyber-border px-4 lg:px-8 py-3">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand & Connection Badge */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-cyber-border to-cyber-neon p-[1px] flex items-center justify-center shadow-lg shadow-cyber-neon/20">
              <div className="w-full h-full bg-cyber-pitch rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-cyber-neon animate-pulse-glow" />
              </div>
            </div>
            {isConnected && (
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyber-neon opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-cyber-neon"></span>
              </span>
            )}
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-wider text-white flex items-center gap-1.5 font-mono">
                AEGIS<span className="text-cyber-neon font-black tracking-widest text-shadow">AI</span>
              </h1>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-cyber-panel text-cyber-neon border border-cyber-border font-semibold tracking-wider">
                SIH 2026 Edition
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted flex items-center gap-1.5 font-mono">
              Autonomous Adaptive Cyber Defense Agent
              <span className="text-cyber-border">•</span>
              <span className={isConnected ? "text-cyber-neon font-bold" : "text-cyber-amber font-bold"}>
                {isConnected ? "WEBSOCKET LIVE" : "CONNECTING..."}
              </span>
            </p>
          </div>
        </div>

        {/* Global Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-cyber-pitch p-1 rounded-xl border border-cyber-border text-xs font-medium">
          {[
            { id: "dashboard", label: "SOC Overview", icon: Activity },
            { id: "layers", label: "30-Layer Firewall", icon: ShieldAlert },
            { id: "audit", label: "Hash-Chained Audit", icon: Lock },
            { id: "simulator", label: "Attack Simulation", icon: Radio }
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all duration-200 font-mono ${
                  isActive
                    ? "bg-cyber-neon/15 text-cyber-neon border border-cyber-neon/40 shadow-sm shadow-cyber-neon/10 font-bold"
                    : "text-cyber-textMuted hover:text-emerald-200 hover:bg-cyber-panel"
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? "text-cyber-neon" : "text-cyber-textMuted"}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Action Controls & SIH Demo Runner */}
        <div className="flex items-center gap-2">
          {simulationRunning && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-lg bg-red-950/60 border border-red-800 text-cyber-crimson text-xs font-mono animate-pulse">
              <span className="w-2 h-2 rounded-full bg-cyber-crimson animate-ping" />
              SIMULATION: {currentScenario?.toUpperCase()}
            </div>
          )}

          <button
            onClick={onQuickDemo}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyber-neon hover:bg-cyber-lime text-black font-extrabold text-xs font-mono shadow-lg shadow-cyber-neon/25 transition-all transform active:scale-95 border border-cyber-lime"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>5-Min SIH Pitch</span>
          </button>

          <button
            onClick={onReset}
            title="Reset telemetry and states"
            className="p-1.5 rounded-lg bg-cyber-pitch hover:bg-cyber-panel text-cyber-textMuted hover:text-cyber-neon border border-cyber-border transition"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

      </div>

      {/* Real-Time Metrics Strip */}
      <div className="mt-3 pt-2 border-t border-cyber-border grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-[11px] font-mono">
        <div className="bg-cyber-pitch px-3 py-1.5 rounded border border-cyber-border flex items-center justify-between">
          <span className="text-cyber-textMuted">EVENTS:</span>
          <span className="text-cyber-neon font-bold">{metrics.total_events_processed}</span>
        </div>
        <div className="bg-cyber-pitch px-3 py-1.5 rounded border border-cyber-border flex items-center justify-between">
          <span className="text-cyber-textMuted">THREATS:</span>
          <span className="text-cyber-amber font-bold">{metrics.threats_detected}</span>
        </div>
        <div className="bg-cyber-pitch px-3 py-1.5 rounded border border-cyber-border flex items-center justify-between">
          <span className="text-cyber-textMuted">MITIGATED:</span>
          <span className="text-cyber-neon font-bold">{metrics.autonomous_mitigations_executed}</span>
        </div>
        <div className="bg-cyber-pitch px-3 py-1.5 rounded border border-cyber-border flex items-center justify-between">
          <span className="text-cyber-textMuted">KEYS ROTATED:</span>
          <span className="text-cyber-purple font-bold">{metrics.credentials_rotated}</span>
        </div>
        <div className="bg-cyber-pitch px-3 py-1.5 rounded border border-cyber-border flex items-center justify-between">
          <span className="text-cyber-textMuted">AVG MTTR:</span>
          <span className="text-cyber-neon font-bold">{metrics.avg_response_time_ms} ms</span>
        </div>
        <div className="bg-cyber-pitch px-3 py-1.5 rounded border border-cyber-border flex items-center justify-between">
          <span className="text-cyber-textMuted">AUDIT PROOF:</span>
          <span className="text-cyber-neon font-bold">100% SHA-256</span>
        </div>
      </div>
    </header>
  );
};
