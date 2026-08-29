import React, { useState } from "react";
import { useAegisWebSocket } from "./hooks/useWebSocket";
import { Navbar } from "./components/Navbar";
import { ServiceStatusGrid } from "./components/ServiceStatusGrid";
import { ThreatFeed } from "./components/ThreatFeed";
import { AIDecisionLog } from "./components/AIDecisionLog";
import { FirewallRuleDiff } from "./components/FirewallRuleDiff";
import { CredentialEventLog } from "./components/CredentialEventLog";
import { DeepDefense30Layers } from "./components/DeepDefense30Layers";
import { AuditTrailViewer } from "./components/AuditTrailViewer";
import { AttackSimulator } from "./components/AttackSimulator";
import { triggerSimulation } from "./services/api";

export function App() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const {
    isConnected,
    services,
    layers,
    activeRules,
    ruleDiffs,
    events,
    analyses,
    credentials,
    metrics,
    simulationRunning,
    currentScenario
  } = useAegisWebSocket();

  const handleQuickDemo = async () => {
    try {
      await triggerSimulation("sih_demo_5min", 45);
    } catch (e) {
      console.error(e);
    }
  };

  const handleReset = async () => {
    try {
      await triggerSimulation("reset", 1);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-pitch flex flex-col text-emerald-100 selection:bg-cyber-neon/30 selection:text-cyber-neon relative overflow-hidden">
      
      {/* Background Ambient Refraction Glows for Glassmorphism */}
      <div className="ambient-glow-green top-[-100px] left-[10%] opacity-70" />
      <div className="ambient-glow-emerald top-[35%] right-[5%] opacity-60" />
      <div className="ambient-glow-purple bottom-[10%] left-[20%] opacity-50" />
      <div className="ambient-glow-green bottom-[-150px] right-[25%] opacity-60" />

      {/* Top Navbar with Glassmorphic Frosted Blur */}
      <div className="relative z-20">
        <Navbar
          metrics={metrics}
          isConnected={isConnected}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          onQuickDemo={handleQuickDemo}
          onReset={handleReset}
          simulationRunning={simulationRunning}
          currentScenario={currentScenario}
        />
      </div>

      {/* Main Body */}
      <main className="flex-1 p-4 lg:p-8 max-w-[1800px] w-full mx-auto space-y-6 relative z-10">
        
        {/* Tab 1: SOC Overview */}
        {activeTab === "dashboard" && (
          <div className="space-y-6">
            {/* Top: 4 Protected Service Cards with Refractive Glassmorphism */}
            <ServiceStatusGrid services={services} />

            {/* Middle: Live Ingress Feed + AI Reasoning & Policy Gating */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ThreatFeed events={events} />
              <AIDecisionLog analyses={analyses} />
            </div>

            {/* Bottom: Dynamic nftables Rule Diff + Credential Rotator */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <FirewallRuleDiff activeRules={activeRules} ruleDiffs={ruleDiffs} />
              </div>
              <div className="lg:col-span-1">
                <CredentialEventLog credentials={credentials} />
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: 30-Layer Deep Defense Firewall */}
        {activeTab === "layers" && (
          <DeepDefense30Layers layers={layers} />
        )}

        {/* Tab 3: Hash-Chained Audit Ledger */}
        {activeTab === "audit" && (
          <AuditTrailViewer />
        )}

        {/* Tab 4: Attack Simulation Suite */}
        {activeTab === "simulator" && (
          <AttackSimulator
            simulationRunning={simulationRunning}
            currentScenario={currentScenario}
            onRefresh={() => {}}
          />
        )}

      </main>

      {/* Footer with Frosted Glass Header */}
      <footer className="glass-panel border-t border-cyber-border/80 px-4 py-3 text-center text-xs text-cyber-textMuted font-mono relative z-20">
        <span className="flex items-center justify-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyber-neon shadow-sm shadow-cyber-neon animate-pulse" />
          AegisAI v1.0 — Smart India Hackathon Architecture — Powered by Deterministic Policy Trust Boundaries &amp; 30-Layer Deep Defense
        </span>
      </footer>

    </div>
  );
}

export default App;
