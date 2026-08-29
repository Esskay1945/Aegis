export const API_BASE = "http://localhost:8000/api";

export async function fetchDashboardState() {
  const res = await fetch(`${API_BASE}/dashboard`);
  if (!res.ok) throw new Error("Failed to fetch dashboard state");
  return res.json();
}

export async function triggerSimulation(scenario: string, duration = 30, intensity = "high", ip?: string) {
  const res = await fetch(`${API_BASE}/simulation/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      scenario,
      duration_seconds: duration,
      intensity,
      source_ip: ip
    })
  });
  if (!res.ok) throw new Error("Failed to trigger simulation");
  return res.json();
}

export async function stopSimulation() {
  const res = await fetch(`${API_BASE}/simulation/stop`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to stop simulation");
  return res.json();
}

export async function fetchAuditLedger() {
  const res = await fetch(`${API_BASE}/audit/ledger`);
  if (!res.ok) throw new Error("Failed to fetch audit ledger");
  return res.json();
}

export async function verifyAuditLedger() {
  const res = await fetch(`${API_BASE}/audit/verify`);
  if (!res.ok) throw new Error("Failed to verify audit ledger");
  return res.json();
}
