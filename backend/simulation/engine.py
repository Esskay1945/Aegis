import asyncio
import random
import time
import uuid
from typing import Callable, Optional, Dict, Any
from backend.models.schemas import RawEvent, ServiceId

class SimulationEngine:
    """Generates synthetic multi-vector attack traffic and orchestrates live demo scenarios."""

    def __init__(self, event_callback: Optional[Callable[[RawEvent], Any]] = None):
        self.event_callback = event_callback
        self.is_running = False
        self.current_scenario: Optional[str] = None
        self._task: Optional[asyncio.Task] = None

    async def emit(self, raw: RawEvent):
        if self.event_callback:
            res = self.event_callback(raw)
            if asyncio.iscoroutine(res):
                await res

    async def start_scenario(self, scenario_name: str, duration_sec: int = 30, intensity: str = "high", custom_ip: Optional[str] = None):
        await self.stop_simulation()
        self.is_running = True
        self.current_scenario = scenario_name

        if scenario_name == "ssh_brute_force":
            self._task = asyncio.create_task(self._run_ssh_brute_force(duration_sec, intensity, custom_ip))
        elif scenario_name == "port_scan":
            self._task = asyncio.create_task(self._run_port_scan(duration_sec, intensity, custom_ip))
        elif scenario_name == "api_flood":
            self._task = asyncio.create_task(self._run_api_flood(duration_sec, intensity, custom_ip))
        elif scenario_name == "cred_compromise":
            self._task = asyncio.create_task(self._run_cred_compromise(custom_ip))
        elif scenario_name == "apt_chain":
            self._task = asyncio.create_task(self._run_apt_chain(duration_sec))
        elif scenario_name == "sih_demo_5min":
            self._task = asyncio.create_task(self._run_sih_demo_scenario())

    async def stop_simulation(self):
        self.is_running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None
        self.current_scenario = None

    # --- Individual Attack Generators ---
    async def _run_ssh_brute_force(self, duration: int, intensity: str, ip: Optional[str]):
        attacker_ip = ip or f"192.168.1.{random.randint(150, 240)}"
        usernames = ["root", "admin", "ubuntu", "deploy", "guest", "postgres"]
        passwords = ["123456", "admin", "password", "toor", "letmein", "master"]
        interval = 0.15 if intensity == "high" else 0.4
        end_time = time.time() + duration

        while self.is_running and time.time() < end_time:
            user = random.choice(usernames)
            pwd = random.choice(passwords)
            ev = RawEvent(
                source_ip=attacker_ip,
                target_service="ssh_server",
                event_type="auth_failure",
                raw_data={"username": user, "password": "***", "port": 22, "protocol": "SSH-2.0-OpenSSH_8.9"},
                suricata_alert={"sid": 2001, "msg": "ET SCAN Potential SSH Scan / Brute Force Outbound"}
            )
            await self.emit(ev)
            await asyncio.sleep(interval)

    async def _run_port_scan(self, duration: int, intensity: str, ip: Optional[str]):
        attacker_ip = ip or f"10.0.4.{random.randint(50, 100)}"
        target_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 1433, 3306, 3389, 5432, 6379, 8000, 8080, 8443, 9000, 27017]
        interval = 0.08 if intensity == "high" else 0.25
        end_time = time.time() + duration

        while self.is_running and time.time() < end_time:
            p = random.choice(target_ports)
            ev = RawEvent(
                source_ip=attacker_ip,
                target_service="web_server" if p in [80, 443, 8080] else ("api_server" if p in [8000, 9000] else "ssh_server"),
                event_type="port_sweep",
                raw_data={"port": p, "flags": "SYN", "scan_type": "SYN Stealth Scan (Nmap)"},
                suricata_alert={"sid": 1002, "msg": "ET SCAN Nmap Scripting Engine / Sweep"}
            )
            await self.emit(ev)
            await asyncio.sleep(interval)

    async def _run_api_flood(self, duration: int, intensity: str, ip: Optional[str]):
        attacker_ip = ip or f"172.16.20.{random.randint(10, 99)}"
        endpoints = ["/api/v1/auth/login", "/api/v1/users", "/api/v1/checkout", "/api/v1/search", "/api/v1/data/export"]
        interval = 0.05 if intensity == "high" else 0.15
        end_time = time.time() + duration

        while self.is_running and time.time() < end_time:
            ep = random.choice(endpoints)
            ev = RawEvent(
                source_ip=attacker_ip,
                target_service="api_server",
                event_type="api_flood",
                raw_data={"endpoint": ep, "method": "POST", "payload_size_bytes": 1024, "user_agent": "AegisAttackBot/2.1"},
                suricata_alert={"sid": 3001, "msg": "ET DOS High Frequency HTTP Flood Detected"}
            )
            await self.emit(ev)
            await asyncio.sleep(interval)

    async def _run_cred_compromise(self, ip: Optional[str]):
        attacker_ip = ip or "203.0.113.45"
        for _ in range(5):
            ev = RawEvent(
                source_ip=attacker_ip,
                target_service="api_server",
                event_type="cred_compromise",
                raw_data={"token_anomaly": True, "token_id": "API_SERVER_BEARER_V1", "geo_asn": "AS9009 Foreign ASN"},
                suricata_alert={"sid": 4001, "msg": "ET POLICY Suspicious Token Geolocation Velocity"}
            )
            await self.emit(ev)
            await asyncio.sleep(0.3)

    async def _run_apt_chain(self, duration: int):
        attacker_ip = "198.51.100.88"
        # Stage 1: Port Scan
        for _ in range(15):
            if not self.is_running: return
            await self.emit(RawEvent(
                source_ip=attacker_ip,
                target_service="web_server",
                event_type="port_sweep",
                raw_data={"port": random.randint(20, 1000), "phase": "1. Reconnaissance"}
            ))
            await asyncio.sleep(0.1)

        await asyncio.sleep(1.0)

        # Stage 2: Targeted SSH Brute Force
        for _ in range(20):
            if not self.is_running: return
            await self.emit(RawEvent(
                source_ip=attacker_ip,
                target_service="ssh_server",
                event_type="auth_failure",
                raw_data={"username": "admin", "phase": "2. Initial Access"}
            ))
            await asyncio.sleep(0.12)

        await asyncio.sleep(1.0)

        # Stage 3: Credential compromise
        for _ in range(5):
            if not self.is_running: return
            await self.emit(RawEvent(
                source_ip=attacker_ip,
                target_service="api_server",
                event_type="cred_compromise",
                raw_data={"phase": "3. Privilege Escalation", "token_anomaly": True}
            ))
            await asyncio.sleep(0.2)

    async def _run_sih_demo_scenario(self):
        """Automated 5-Minute SIH Demo Progression Script."""
        # Stage 1: SSH Brute Force
        await self._run_ssh_brute_force(duration=15, intensity="high", ip="192.168.1.188")
        await asyncio.sleep(3.0)

        # Stage 2: Second Vector (API Flood)
        await self._run_api_flood(duration=15, intensity="high", ip="172.16.20.55")
        await asyncio.sleep(3.0)

        # Stage 3: Credential Compromise
        await self._run_cred_compromise(ip="203.0.113.45")
