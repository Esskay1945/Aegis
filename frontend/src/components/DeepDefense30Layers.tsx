import React, { useState } from "react";
import { Shield, ShieldAlert, Cpu, Lock, Terminal, Globe, Layers } from "lucide-react";
import { FirewallLayer } from "../types/events";

interface DeepDefense30LayersProps {
  layers: FirewallLayer[];
}

const CATEGORY_STYLES: Record<string, { border: string; bg: string; text: string; icon: any }> = {
  "Network & Transport": { border: "border-cyber-border", bg: "bg-cyber-panel/60", text: "text-emerald-300", icon: Globe },
  "Identity & Access": { border: "border-cyber-border", bg: "bg-cyber-panel/60", text: "text-purple-400", icon: Lock },
  "API & Protocol": { border: "border-cyber-border", bg: "bg-cyber-panel/60", text: "text-cyber-neon", icon: Terminal },
  "OS & Kernel": { border: "border-cyber-border", bg: "bg-cyber-panel/60", text: "text-amber-400", icon: Cpu },
  "AI & Semantic": { border: "border-cyber-border", bg: "bg-cyber-panel/60", text: "text-pink-400", icon: ShieldAlert },
  "Cryptographic & State": { border: "border-cyber-border", bg: "bg-cyber-panel/60", text: "text-cyber-neon", icon: Shield }
};

export const DeepDefense30Layers: React.FC<DeepDefense30LayersProps> = ({ layers }) => {
  const [selectedLayer, setSelectedLayer] = useState<FirewallLayer | null>(null);

  const categories = Array.from(new Set(layers.map((l) => l.category)));

  return (
    <div className="glass-panel rounded-2xl p-5 lg:p-7 border border-cyber-border flex flex-col gap-6">
      {/* Title & Stats with Glass Highlight */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-cyber-border/80 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border shadow-inner">
              <Layers className="w-4.5 h-4.5 text-cyber-neon" />
            </div>
            <h2 className="text-lg font-bold text-white tracking-wide font-mono">
              30-Layer Deep Defense Firewall Architecture
            </h2>
          </div>
          <p className="text-xs text-cyber-textMuted font-mono mt-1">
            Granular multi-plane inspection extending from physical signaling down to kernel eBPF &amp; secure memory enclaves.
          </p>
        </div>

        <div className="flex items-center gap-2.5 font-mono text-xs">
          <div className="glass-card px-3.5 py-1.5 rounded-xl flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyber-neon shadow-sm shadow-cyber-neon" />
            <span className="text-cyber-textMuted">Active Layers: <strong className="text-white">{layers.length}</strong></span>
          </div>
          <div className="glass-panel-glow px-3.5 py-1.5 rounded-xl text-cyber-neon flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyber-neon animate-ping" />
            <span>Filtering: <strong className="font-black">{layers.filter(l => l.status === "FILTERING").length}</strong></span>
          </div>
        </div>
      </div>

      {/* Layer Grid by Categories */}
      <div className="space-y-6">
        {categories.map((cat) => {
          const style = CATEGORY_STYLES[cat] || CATEGORY_STYLES["Network & Transport"];
          const Icon = style.icon;
          const catLayers = layers.filter((l) => l.category === cat);

          return (
            <div key={cat} className="space-y-3">
              <div className="flex items-center gap-2">
                <Icon className={`w-4 h-4 ${style.text}`} />
                <h3 className={`text-xs font-bold font-mono uppercase tracking-wider ${style.text}`}>
                  {cat} ({catLayers[0]?.layer_id} - {catLayers[catLayers.length - 1]?.layer_id})
                </h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
                {catLayers.map((layer) => {
                  const isFiltering = layer.status === "FILTERING";
                  const isSelected = selectedLayer?.layer_id === layer.layer_id;

                  return (
                    <button
                      key={layer.layer_id}
                      onClick={() => setSelectedLayer(layer)}
                      className={`text-left p-3.5 rounded-xl border transition-all duration-200 flex flex-col justify-between min-h-[95px] relative overflow-hidden font-mono ${
                        isFiltering
                          ? "glass-panel-glow border-cyber-neon shadow-lg shadow-cyber-neon/20"
                          : isSelected
                          ? "glass-card border-cyber-neon bg-cyber-neon/10"
                          : "glass-card hover:border-cyber-neon/40 hover:bg-cyber-panel/80"
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1 w-full mb-1">
                        <span className="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded-md bg-cyber-pitch/80 text-cyber-neon border border-cyber-border shadow-inner">
                          L{layer.layer_id}
                        </span>

                        <span
                          className={`text-[9px] font-mono font-extrabold px-2 py-0.5 rounded-full border uppercase ${
                            isFiltering
                              ? "bg-cyber-panel text-cyber-neon border-cyber-neon shadow-sm shadow-cyber-neon/30 animate-pulse"
                              : "bg-cyber-pitch/80 text-cyber-textMuted border-cyber-border"
                          }`}
                        >
                          {layer.status}
                        </span>
                      </div>

                      <div className="text-xs font-semibold text-emerald-100 line-clamp-1 mt-1">
                        {layer.name}
                      </div>

                      <div className="text-[10px] text-cyber-textMuted font-mono mt-1.5 flex items-center justify-between">
                        <span>Filters: <strong className={layer.active_filters > 0 ? "text-cyber-neon font-black" : "text-cyber-textMuted"}>{layer.active_filters}</strong></span>
                        {isFiltering && (
                          <span className="text-[10px] text-cyber-neon animate-ping font-bold">●</span>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Layer Inspector Modal / Drawer */}
      {selectedLayer && (
        <div className="mt-4 p-5 rounded-2xl glass-panel-glow font-mono text-xs flex flex-col gap-2.5 animate-in fade-in duration-200">
          <div className="flex items-center justify-between border-b border-cyber-border/80 pb-2.5">
            <div className="flex items-center gap-2.5">
              <span className="px-2.5 py-0.5 rounded-full bg-cyber-pitch text-cyber-neon border border-cyber-neon font-extrabold shadow-sm shadow-cyber-neon/20">
                LAYER {selectedLayer.layer_id}
              </span>
              <h4 className="text-sm font-bold text-white">{selectedLayer.name}</h4>
              <span className="text-cyber-textMuted">({selectedLayer.category})</span>
            </div>
            <button
              onClick={() => setSelectedLayer(null)}
              className="text-cyber-textMuted hover:text-white text-xs px-2.5 py-1 rounded-lg bg-cyber-pitch/80 border border-cyber-border hover:border-cyber-neon/50 transition"
            >
              Close
            </button>
          </div>

          <p className="text-emerald-100 font-sans leading-relaxed text-sm">
            {selectedLayer.description}
          </p>

          <div className="flex items-center gap-5 text-[11px] text-cyber-textMuted pt-1.5">
            <span>Status: <strong className="text-cyber-neon font-bold">{selectedLayer.status}</strong></span>
            <span>Active Intercept Filters: <strong className="text-cyber-neon font-bold">{selectedLayer.active_filters}</strong></span>
            {selectedLayer.last_intercept && (
              <span>Last Intercept: <strong className="text-white">{new Date(selectedLayer.last_intercept).toLocaleTimeString()}</strong></span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
