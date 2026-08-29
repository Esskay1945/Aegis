import React, { useState } from "react";
import { Play, Square, ShieldCheck, Terminal, Globe, Server, Key, Flame, Zap, AlertTriangle } from "lucide-react";
import { triggerSimulation, stopSimulation } from "../services/api";

interface AttackSimulatorProps {
  simulationRunning: boolean;
  currentScenario: string | null;
  onRefresh: () => void;
}

export const AttackSimulator: React.FC<AttackSimulatorProps> = ({
  simulationRunning,
  currentScenario,
  onRefresh
}) => {
  const [intensity] = useState<string>("high");
  const [customIp] = useState<string>("");

  const handleLaunch = async (scenario: string, duration = 25) => {
    try {
      await triggerSimulation(scenario, duration, intensity, customIp || undefined);
      onRefresh();
    } catch (err) {
      console.error("Simulation error:", err);
    }
  };

  const handleStop = async () => {
    try {
      await stopSimulation();
      onRefresh();
    } catch (err) {
      console.error("Stop error:", err);
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-7 border border-cyber-border flex flex-col gap-6 font-mono">
      {/* Title & Status */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-cyber-border/80 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border shadow-inner">
              <Flame className="w-4.5 h-4.5 text-cyber-crimson animate-pulse" />
            </div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Adversarial Attack Simulation Suite
            </h2>
          </div>
          <p className="text-xs text-cyber-textMuted mt-1">
            Simulate real-world adversary tactics to demonstrate closed-loop detection, policy gating, and autonomous defense.
          </p>
        </div>

        {simulationRunning ? (
          <button
            onClick={handleStop}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-cyber-crimson hover:bg-red-600 text-white font-black text-xs shadow-lg shadow-red-500/30 transition transform active:scale-95 border border-red-400"
          >
            <Square className="w-4 h-4 fill-current" />
            <span>Halt Current Simulation ({currentScenario})</span>
          </button>
        ) : (
          <div className="flex items-center gap-2 text-xs text-cyber-textMuted glass-card px-3.5 py-1.5 rounded-xl">
            <span className="w-2.5 h-2.5 rounded-full bg-cyber-neon shadow-sm shadow-cyber-neon" />
            <span className="text-cyber-neon font-bold">Simulator Ready</span>
          </div>
        )}
      </div>

      {/* Primary 5-Minute SIH Demo Card */}
      <div className="p-5 rounded-2xl glass-panel-glow flex flex-col md:flex-row items-center justify-between gap-5">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <Zap className="w-4.5 h-4.5 text-cyber-neon animate-pulse" />
            <h3 className="text-sm font-bold text-white tracking-wide">
              5-Minute Smart India Hackathon Live Pitch Script
            </h3>
          </div>
          <p className="text-xs text-emerald-200/80 font-sans leading-relaxed">
            Automates the complete end-to-end hackathon presentation: Baseline → SSH Brute Force → Autonomous Policy Lockdown → Credential Rotation (V1 → V2) → API Flooding Distraction → Self-Recovery.
          </p>
        </div>

        <button
          onClick={() => handleLaunch("sih_demo_5min", 45)}
          disabled={simulationRunning}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-cyber-neon hover:bg-cyber-lime text-black font-black text-xs shadow-xl shadow-cyber-neon/30 transition transform active:scale-95 shrink-0 disabled:opacity-50 border border-cyber-lime"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>Launch 5-Min Pitch Demo</span>
        </button>
      </div>

      {/* Attack Vectors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        
        {/* 1. SSH Brute Force */}
        <div className="glass-card p-4.5 rounded-2xl flex flex-col justify-between gap-3.5">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-cyber-crimson flex items-center gap-1.5">
                <Terminal className="w-4 h-4" />
                SSH Brute Force
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-red-950/80 text-cyber-crimson border border-red-800 font-bold">
                Port 22
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted font-sans leading-relaxed">
              High-rate credential spray on OpenSSH server from novel source IP. Triggers L3 drop &amp; token rotation.
            </p>
          </div>

          <button
            onClick={() => handleLaunch("ssh_brute_force", 20)}
            disabled={simulationRunning}
            className="w-full py-2.5 rounded-xl bg-red-950/80 hover:bg-red-900 text-cyber-crimson border border-red-700/80 font-black text-xs flex items-center justify-center gap-1.5 transition shadow-sm"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Launch SSH Attack</span>
          </button>
        </div>

        {/* 2. Port Scan Reconnaissance */}
        <div className="glass-card p-4.5 rounded-2xl flex flex-col justify-between gap-3.5">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-cyber-amber flex items-center gap-1.5">
                <Globe className="w-4 h-4" />
                Port Sweep (Nmap)
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-950/80 text-cyber-amber border border-amber-800 font-bold">
                Multi-Port
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted font-sans leading-relaxed">
              Probes multi-port range across services. Triggers Layer 4 transport guard and port restriction.
            </p>
          </div>

          <button
            onClick={() => handleLaunch("port_scan", 20)}
            disabled={simulationRunning}
            className="w-full py-2.5 rounded-xl bg-amber-950/80 hover:bg-amber-900 text-cyber-amber border border-amber-700/80 font-black text-xs flex items-center justify-center gap-1.5 transition shadow-sm"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Launch Port Sweep</span>
          </button>
        </div>

        {/* 3. API Flood */}
        <div className="glass-card p-4.5 rounded-2xl flex flex-col justify-between gap-3.5">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-cyber-neon flex items-center gap-1.5">
                <Server className="w-4 h-4" />
                API HTTP Flood
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyber-panel text-cyber-neon border border-cyber-neon/40 font-bold">
                Port 8000
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted font-sans leading-relaxed">
              Application-layer HTTP request surge. Triggers L14 dynamic rate-limiting (leaves DB untouched).
            </p>
          </div>

          <button
            onClick={() => handleLaunch("api_flood", 20)}
            disabled={simulationRunning}
            className="w-full py-2.5 rounded-xl bg-cyber-panel hover:bg-cyber-dark text-cyber-neon border border-cyber-neon/60 font-black text-xs flex items-center justify-center gap-1.5 transition shadow-sm shadow-cyber-neon/10"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Launch HTTP Flood</span>
          </button>
        </div>

        {/* 4. Credential Compromise */}
        <div className="glass-card p-4.5 rounded-2xl flex flex-col justify-between gap-3.5">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-cyber-purple flex items-center gap-1.5">
                <Key className="w-4 h-4" />
                Credential Token Leak
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-950/80 text-purple-300 border border-purple-800 font-bold">
                Layer 11
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted font-sans leading-relaxed">
              Anomalous token replay from rogue foreign ASN. Triggers immediate secret revocation and V2 rotation.
            </p>
          </div>

          <button
            onClick={() => handleLaunch("cred_compromise", 10)}
            disabled={simulationRunning}
            className="w-full py-2.5 rounded-xl bg-purple-950/80 hover:bg-purple-900 text-purple-200 border border-purple-700/80 font-black text-xs flex items-center justify-center gap-1.5 transition shadow-sm"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Simulate Token Breach</span>
          </button>
        </div>

        {/* 5. APT Campaign */}
        <div className="glass-card p-4.5 rounded-2xl flex flex-col justify-between gap-3.5">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-pink-400 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4" />
                Multi-Vector APT Campaign
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-pink-950/80 text-pink-300 border border-pink-800 font-bold">
                Sequential
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted font-sans leading-relaxed">
              Coordinated 3-stage Advanced Persistent Threat: Reconnaissance → Initial Access → Privilege Escalation.
            </p>
          </div>

          <button
            onClick={() => handleLaunch("apt_chain", 30)}
            disabled={simulationRunning}
            className="w-full py-2.5 rounded-xl bg-pink-950/80 hover:bg-pink-900 text-pink-200 border border-pink-700/80 font-black text-xs flex items-center justify-center gap-1.5 transition shadow-sm"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Launch APT Campaign</span>
          </button>
        </div>

        {/* 6. Autonomous Recovery Trigger */}
        <div className="glass-card p-4.5 rounded-2xl flex flex-col justify-between gap-3.5 border-emerald-500/30">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-cyber-neon flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4" />
                Threat Clearance &amp; Recovery
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyber-panel text-cyber-neon border border-cyber-neon/40 font-bold">
                Baseline
              </span>
            </div>
            <p className="text-xs text-cyber-textMuted font-sans leading-relaxed">
              Signals that hostile traffic has ceased. Triggers recovery engine to revert temporary rules and restore baseline.
            </p>
          </div>

          <button
            onClick={() => handleLaunch("threat_clearance", 5)}
            className="w-full py-2.5 rounded-xl bg-cyber-panel hover:bg-cyber-neon hover:text-black text-cyber-neon border border-cyber-neon/80 font-black text-xs flex items-center justify-center gap-1.5 transition shadow-md shadow-cyber-neon/15"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Trigger Threat Clearance</span>
          </button>
        </div>

      </div>
    </div>
  );
};
