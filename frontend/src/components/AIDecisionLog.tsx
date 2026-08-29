import React from "react";
import { Cpu, ShieldCheck, CheckCircle2, Zap, Target, FileText } from "lucide-react";
import { AIAnalysisResult } from "../types/events";

interface AIDecisionLogProps {
  analyses: AIAnalysisResult[];
}

export const AIDecisionLog: React.FC<AIDecisionLogProps> = ({ analyses }) => {
  return (
    <div className="glass-panel rounded-2xl flex flex-col h-[500px] overflow-hidden">
      {/* Frosted Glass Header */}
      <div className="p-3.5 bg-cyber-panel/60 backdrop-blur-xl border-b border-cyber-border/80 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-lg bg-cyber-pitch/80 flex items-center justify-center border border-cyber-border">
            <Cpu className="w-3.5 h-3.5 text-cyber-neon" />
          </div>
          <h3 className="text-xs font-bold font-mono tracking-wider text-emerald-200 uppercase">
            AI Security Agent Reasoning &amp; Policy Gate
          </h3>
        </div>
        <span className="text-[10px] font-mono px-2.5 py-0.5 bg-cyber-pitch/80 text-cyber-neon rounded-full border border-cyber-neon/30 font-extrabold shadow-sm shadow-cyber-neon/10">
          Deterministic Guardrails Active
        </span>
      </div>

      {/* Analysis Cards Stream */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3.5 font-mono text-xs">
        {analyses.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-cyber-textMuted gap-2">
            <ShieldCheck className="w-7 h-7 text-cyber-dim" />
            <span className="text-xs">AI Reasoning Layer idle. System monitoring baseline traffic.</span>
          </div>
        ) : (
          analyses.map((item) => {
            const confPct = Math.round(item.confidence * 100);

            return (
              <div
                key={item.analysis_id}
                className="glass-card rounded-xl p-3.5 transition-all flex flex-col gap-3 hover:border-cyber-neon/40 shadow-sm"
              >
                {/* Title & Classification Bar */}
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-cyber-textMuted text-[10px]">
                      {new Date(item.timestamp).toLocaleTimeString()}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full bg-cyber-panel text-cyber-neon border border-cyber-neon/40 font-extrabold uppercase text-[11px] flex items-center gap-1 shadow-sm shadow-cyber-neon/10">
                      <Target className="w-3.5 h-3.5 text-cyber-neon" />
                      {item.attack_class.replace("_", " ")}
                    </span>
                    <span className="text-cyber-textMuted text-[11px]">
                      Scope: <strong className="text-cyber-neon">{item.affected_services.join(", ")}</strong>
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-cyber-textMuted text-[11px]">Confidence:</span>
                    <span className="font-extrabold text-black bg-cyber-neon px-2.5 py-0.5 rounded-full shadow-md shadow-cyber-neon/30 text-xs">
                      {confPct}%
                    </span>
                  </div>
                </div>

                {/* Natural Language Explanation Card */}
                <div className="p-3 rounded-xl bg-cyber-pitch/70 backdrop-blur-md border border-cyber-border/80 text-emerald-100 text-xs leading-relaxed">
                  <p className="flex items-start gap-2 font-sans">
                    <FileText className="w-4 h-4 text-cyber-neon shrink-0 mt-0.5" />
                    <span>{item.explanation}</span>
                  </p>
                </div>

                {/* Behavioral Evidence */}
                {item.evidence.length > 0 && (
                  <div className="bg-cyber-panel/40 p-2.5 rounded-xl border border-cyber-border/60">
                    <span className="text-[10px] text-cyber-textMuted font-extrabold block mb-1.5 uppercase">
                      Extracted Behavioral Indicators:
                    </span>
                    <ul className="space-y-1 text-[11px] text-emerald-200/90">
                      {item.evidence.map((ev, idx) => (
                        <li key={idx} className="flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-cyber-neon shadow-sm shadow-cyber-neon shrink-0" />
                          <span>{ev}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Recommended Actions & Policy Engine Verdict */}
                <div className="pt-2.5 border-t border-cyber-border/60 flex flex-col gap-2">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-cyber-textMuted font-bold flex items-center gap-1.5">
                      <Zap className="w-3.5 h-3.5 text-cyber-amber" />
                      PROPOSED ACTIONS ({item.recommended_actions.length}):
                    </span>
                    <span className="text-cyber-neon font-black text-[10px] flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-cyber-neon" />
                      POLICY ENGINE APPROVED
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    {item.recommended_actions.map((act, aIdx) => (
                      <span
                        key={aIdx}
                        className="px-2.5 py-1 rounded-lg bg-cyber-pitch/80 text-cyber-neon border border-cyber-border text-[10px] flex items-center gap-1.5 font-bold shadow-inner"
                      >
                        <span className="text-cyber-textMuted uppercase">{act.type}:</span>
                        <span className="text-white">{act.target}</span>
                        {act.layer_target && (
                          <span className="text-[9px] bg-cyber-panel text-cyber-neon px-1.5 py-0.2 rounded border border-cyber-neon/30">
                            L{act.layer_target}
                          </span>
                        )}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
