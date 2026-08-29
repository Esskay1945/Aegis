from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from backend.models.schemas import DefenseAction, FirewallRule, FirewallLayer

# Complete 30-Layer Deep Defense Architecture Definitions
THIRTY_LAYERS: List[Dict[str, Any]] = [
    # 1-7: Network & Transport
    {"layer_id": 1, "name": "Physical Anomaly Guard", "category": "Network & Transport", "description": "Signal & PHY layer link anomaly detector"},
    {"layer_id": 2, "name": "Data Link MAC Filter", "category": "Network & Transport", "description": "L2 ARP spoofing and MAC table drift prevention"},
    {"layer_id": 3, "name": "Network IP Filter", "category": "Network & Transport", "description": "L3 IP filtering, CIDR drops, and spoofed route suppression"},
    {"layer_id": 4, "name": "Transport Port Guard", "category": "Network & Transport", "description": "L4 TCP SYN flood, UDP amplification, and port sweep blocker"},
    {"layer_id": 5, "name": "Session Handshake Filter", "category": "Network & Transport", "description": "TLS 1.3 handshake anomaly & cipher downgrade filter"},
    {"layer_id": 6, "name": "Presentation Encoding Shield", "category": "Network & Transport", "description": "Payload decoding, gzip bomb, and unicode obfuscation stripper"},
    {"layer_id": 7, "name": "Application HTTP/DNS Filter", "category": "Network & Transport", "description": "L7 WAF, HTTP method constraints, and DNS tunneling detector"},
    
    # 8-12: Identity, Access & Session
    {"layer_id": 8, "name": "Zero-Trust Posture Broker", "category": "Identity & Access", "description": "Continuous ZTNA device health and compliance evaluator"},
    {"layer_id": 9, "name": "Multi-Factor Sentinel", "category": "Identity & Access", "description": "Adaptive step-up MFA and geofence velocity enforcer"},
    {"layer_id": 10, "name": "Session Hijacking Watcher", "category": "Identity & Access", "description": "Session token fingerprinting and IP-binding validator"},
    {"layer_id": 11, "name": "Token Lifecycle & Rotation", "category": "Identity & Access", "description": "Autonomous JWT/API key revocation and rapid secret rotator"},
    {"layer_id": 12, "name": "Behavioral Biometric Profiler", "category": "Identity & Access", "description": "Keystroke & interaction dynamics insider threat detector"},

    # 13-17: API, Service & Protocol
    {"layer_id": 13, "name": "REST OpenAPI Validator", "category": "API & Protocol", "description": "Strict JSON schema enforcement and payload fuzzing barrier"},
    {"layer_id": 14, "name": "Dynamic API Rate Limiter", "category": "API & Protocol", "description": "Token-bucket sliding-window rate limiter per client"},
    {"layer_id": 15, "name": "gRPC / Protobuf Inspector", "category": "API & Protocol", "description": "Binary payload serialization inspection & method gating"},
    {"layer_id": 16, "name": "Shadow API Endpoint Sniffer", "category": "API & Protocol", "description": "Detects undocumented endpoints and rogue parameter injection"},
    {"layer_id": 17, "name": "Service Mesh mTLS Enforcer", "category": "API & Protocol", "description": "Strict mutual TLS authentication between internal microservices"},

    # 18-22: OS & Kernel Execution
    {"layer_id": 18, "name": "eBPF Syscall Interceptor", "category": "OS & Kernel", "description": "Kernel-level system call filtering without panic risk"},
    {"layer_id": 19, "name": "Memory Integrity & ROP Guard", "category": "OS & Kernel", "description": "Stack canary, buffer overflow, and ROP chain suppressor"},
    {"layer_id": 20, "name": "Container Namespace Quarantine", "category": "OS & Kernel", "description": "Dynamic cgroup & network namespace isolation orchestrator"},
    {"layer_id": 21, "name": "Dynamic AppArmor Synthesizer", "category": "OS & Kernel", "description": "Real-time security profile generation per process"},
    {"layer_id": 22, "name": "Process Execution Anomaly Filter", "category": "OS & Kernel", "description": "Parent-child process tree anomaly and fork-bomb blocker"},

    # 23-26: AI & Semantic Reasoning
    {"layer_id": 23, "name": "LLM Prompt Injection Shield", "category": "AI & Semantic", "description": "Adversarial prompt injection, jailbreak, and system prompt leak guard"},
    {"layer_id": 24, "name": "Semantic Exfiltration Sentinel", "category": "AI & Semantic", "description": "DLP engine scanning LLM completions for PII/secret leakage"},
    {"layer_id": 25, "name": "DGA & Fast-Flux Classifier", "category": "AI & Semantic", "description": "ML classifier for algorithmically generated malicious domains"},
    {"layer_id": 26, "name": "Payload Vector Clustered Filter", "category": "AI & Semantic", "description": "High-dimensional embedding similarity filter for novel exploits"},

    # 27-30: Cryptographic & Data State
    {"layer_id": 27, "name": "Confidential Computing Enclave", "category": "Cryptographic & State", "description": "Data-in-use SGX/SEV memory enclave attestation"},
    {"layer_id": 28, "name": "Ransomware Entropy Halter", "category": "Cryptographic & State", "description": "Process-kill trigger upon rapid file encryption entropy spike"},
    {"layer_id": 29, "name": "Homomorphic Query Verifier", "category": "Cryptographic & State", "description": "Zero-knowledge verification on encrypted database queries"},
    {"layer_id": 30, "name": "Immutable State Rollback Engine", "category": "Cryptographic & State", "description": "Atomic system snapshot restoration upon threat clearance"}
]

class FirewallRuleGenerator:
    """Generates nftables rules and maps policy actions to 30-Layer Deep Defense matrix."""

    @staticmethod
    def get_all_layers() -> List[FirewallLayer]:
        layers = []
        for l in THIRTY_LAYERS:
            layers.append(FirewallLayer(
                layer_id=l["layer_id"],
                name=l["name"],
                category=l["category"],
                status="ACTIVE",
                active_filters=0,
                description=l["description"]
            ))
        return layers

    @staticmethod
    def generate_rule(action: DefenseAction) -> FirewallRule:
        now = datetime.utcnow()
        expires = now + timedelta(seconds=action.ttl) if action.ttl > 0 else None
        
        # Determine target layer
        layer_num = action.layer_target or 3
        layer_meta = next((l for l in THIRTY_LAYERS if l["layer_id"] == layer_num), THIRTY_LAYERS[2])

        # Generate nftables syntax
        nft_syntax = ""
        svc = action.scope
        port_map = {"ssh_server": 22, "web_server": 80, "api_server": 8000, "database": 5432}
        port = port_map.get(svc, 80)

        if action.type == "block_ip":
            nft_syntax = f"nft add rule inet aegis_filter input ip saddr {action.target} tcp dport {port} drop comment \"AegisAI-{svc}-block\""
        elif action.type == "rate_limit":
            limit = action.threshold or "60/minute"
            nft_syntax = f"nft add rule inet aegis_filter input tcp dport {port} ct state new limit rate {limit} accept comment \"AegisAI-{svc}-ratelimit\""
        elif action.type == "port_restrict":
            nft_syntax = f"nft add rule inet aegis_filter input tcp dport != {port} drop comment \"AegisAI-{svc}-port-restrict\""
        elif action.type == "isolate_service":
            nft_syntax = f"docker network disconnect protected_net {svc} && docker network connect quarantine_net {svc}"
        elif action.type == "rotate_credential":
            nft_syntax = f"vault kv put secret/{svc} key_version=V2 status=active"

        return FirewallRule(
            service_scope=action.scope,
            layer_number=layer_num,
            layer_name=layer_meta["name"],
            source_ip=action.target if action.type == "block_ip" else None,
            port=port,
            action="drop" if action.type in ["block_ip", "port_restrict"] else "rate_limit",
            rate_limit=action.threshold,
            ttl_seconds=action.ttl,
            created_at=now.isoformat(),
            expires_at=expires.isoformat() if expires else None,
            active=True,
            nft_syntax=nft_syntax
        )
