# AegisAI — Autonomous Adaptive Cyber Defense Agent
### Comprehensive Technical Documentation
**Version:** 1.0 | **Date:** August 2026 | **Classification:** SIH Internal

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Research Landscape & Identified Gaps](#2-research-landscape--identified-gaps)
3. [Novelty & Positioning](#3-novelty--positioning)
4. [System Architecture](#4-system-architecture)
5. [Feature Specification](#5-feature-specification)
6. [AI/ML Pipeline](#6-aiml-pipeline)
7. [Tech Stack](#7-tech-stack)
8. [Module-Level Design](#8-module-level-design)
9. [Security Design Decisions](#9-security-design-decisions)
10. [Demo Environment](#10-demo-environment)
11. [Evaluation Metrics](#11-evaluation-metrics)
12. [Future Roadmap](#12-future-roadmap)
13. [References](#13-references)

---

## 1. Project Overview

### 1.1 Title
**AegisAI — Autonomous Adaptive Cyber Defense Agent**

### 1.2 Tagline
> *Detect. Decide. Defend. Adapt. Recover.*

### 1.3 Problem Statement

Modern cyberattacks are increasingly dynamic, automated, and multi-vector. Conventional defenses — static firewall rules, signature-based IDS, and manual SOC workflows — fail to keep pace. When an attack occurs, the typical response chain looks like:

```
Attack detected
    ↓
Alert to administrator (minutes to hours)
    ↓
Manual investigation
    ↓
Manual firewall modification
    ↓
Manual credential rotation
    ↓
Manual service recovery
```

This introduces two critical failure windows:
- **Detection-to-response gap** — averaging 258 days in real-world breach lifecycles (IBM, 2024)
- **Coarse-grained response** — blocking at network level without understanding service-specific blast radius

**There is no widely deployed system that closes the loop from detection → classification → service-level policy adaptation → credential rotation → recovery → audit, autonomously and in real time.**

### 1.4 Proposed Solution

AegisAI is an AI-driven autonomous cyber-defense platform implementing a complete closed-loop security mechanism:

```
Monitor → Detect → Analyze → Classify → Decide → Validate → Execute → Observe → Recover → Learn
```

The system operates with a **policy engine as the trust boundary** between the AI reasoning layer and the infrastructure control layer — ensuring no unconstrained autonomous command execution.

---

## 2. Research Landscape & Identified Gaps

### 2.1 Current State of the Art

A systematic review of 2023–2026 literature reveals four dominant paradigms:

| Paradigm | Representative Work | Limitation |
|---|---|---|
| Rule-based SOAR | Traditional SIEM/SOAR | Static playbooks; no learning |
| RL-based Autonomous Agents | CybORG, CAGE Challenges | Non-transferable policies; opaque decisions |
| LLM-augmented SOC | AutoGen, LangChain-based agents | Hallucination risk; no execution guardrails |
| Multi-agent IDS | AgentSec (federated, IoT) | Detection-only; no integrated response |

**Benchmarking of five leading agentic frameworks (LangChain, AutoGen, CrewAI, MetaGPT, AgentVerse) on CyberSecEval showed significant variance in multi-step reasoning and coordination under novel attack scenarios (Garcia et al., 2024).**

DARPA's AIxCC (2024–2025) demonstrated that AI agents can find and patch open-source vulnerabilities faster than human teams in controlled settings — but this remains confined to code-level defense, not live infrastructure response.

### 2.2 Identified Research Gaps

The following gaps are drawn from systematic analysis of 2024–2026 literature and are **directly addressed by AegisAI's design**:

---

#### GAP 1: Absence of Resource-Level (Per-Service) Policy Adaptation

**What exists:** Most autonomous defense systems apply network-wide or host-wide policies. A brute-force attack on SSH results in either global IP blocking or nothing.

**What's missing:** No existing prototype demonstrates *per-service* security policy generation and enforcement — where the Web Server, API Server, and Database each receive independently computed, attack-appropriate policies.

**AegisAI's answer:** The Policy Engine maintains a per-resource policy graph. Each service has its own current policy state, and the AI agent generates service-scoped actions rather than system-wide ones.

**Supporting gap evidence:**
> *"Existing multi-agent security systems improve decomposition yet frequently lack verifiable workflow restrictions."* — ScienceDirect, Explainable Autonomous Cyber Defense (2026)

---

#### GAP 2: LLM Hallucination Risk in Autonomous Execution

**What exists:** LLMs are increasingly used for threat classification and response recommendation. Studies across 167 reviewed papers (2022–2025) confirm LLMs contribute through enhanced semantic reasoning rather than raw detection accuracy.

**What's missing:** Unconstrained LLM-to-execution pipelines are documented to amplify operational risk — hallucinated threat attribution, false-positive escalation, and unsafe autonomous responses have been observed in real deployments.

**AegisAI's answer:** The LLM is used **only** for threat explanation, incident summarization, and response recommendation. It cannot directly execute infrastructure commands. Every proposed action passes through a deterministic, rule-constrained Policy Engine before execution. This mirrors the "automate the routine, escalate the consequential" design pattern recommended by ISACA (2025).

**Supporting gap evidence:**
> *"Unconstrained agent reasoning can amplify operational risk under uncertainty."* — Huang et al., 2025; Xu et al., LLM Hallucination Survey

---

#### GAP 3: No Integrated Credential Rotation in Autonomous Response

**What exists:** Credential rotation is treated as a separate, manual security process — completely decoupled from attack response workflows. Existing autonomous defense platforms (CybORG, CAGE, Microsoft CyberBattleSim) do not model credential lifecycle as a defensive action.

**What's missing:** When a brute-force or credential-stuffing attack is detected, no existing prototype automatically revokes the targeted credential, generates a replacement, and re-establishes service connectivity — all within the incident response loop.

**AegisAI's answer:** The Credential Engine is a first-class component in the response pipeline. Upon classification of a credential-compromise or brute-force attack, the engine revokes, rotates, and re-establishes credentials for the affected service, with the new credential version logged in the audit trail.

---

#### GAP 4: Explainability Disconnected from Executable Constraints

**What exists:** Explainable AI (XAI) has made significant advances in interpretability — SHAP, LIME, causal analytics. Post-hoc explanations are now common in security dashboards.

**What's missing:** Explanations are typically decorative — they describe what the model did, but are not mechanistically linked to what actions the model is *permitted* to take.

**AegisAI's answer:** AegisAI's explanations are structurally tied to the policy engine's permission set. The LLM generates an explanation *and* a proposed action. The policy engine validates the action against permitted action categories before execution. The displayed explanation therefore always corresponds to an actually-executable or actually-blocked action — not a post-hoc rationalization.

**Supporting gap evidence:**
> *"Causal analytics improve post hoc reasoning but often remain detached from executable policy constraints; explainable AI improves interpretability but does not enforce admissible action trajectories."* — ScienceDirect, 2026

---

#### GAP 5: Absence of Self-Recovery After Autonomous Containment

**What exists:** Autonomous defense research overwhelmingly focuses on the containment phase. The recovery phase — restoring baseline security policy, re-enabling blocked services, re-establishing rotated credentials — is treated as a manual post-incident task.

**What's missing:** No prototype demonstrates time-bounded automatic rollback of temporary containment policies after threat clearance, combined with verification that the environment is safe before rollback.

**AegisAI's answer:** After the Monitoring Module detects threat clearance (attack traffic ceases, behavioral metrics normalize), the Recovery Engine initiates a controlled rollback: temporary firewall rules are expired, temporary blocks are lifted, and the SOC dashboard reflects the transition to baseline state. The audit log records every rollback event.

---

#### GAP 6: Alert Fatigue and False-Positive Rates in Autonomous Pipelines

**What exists:** SOC automation has reduced mean detection time significantly, but high false-positive rates remain a leading cause of analyst burnout and misconfigured automated responses.

**What's missing:** Autonomous systems that tune their detection threshold dynamically based on recent false-positive feedback, rather than using a fixed confidence cutoff.

**AegisAI's answer (partial, roadmap):** In v1, the system uses a hybrid rule + ML approach (Isolation Forest) with a configurable confidence threshold. False-positive feedback from the dashboard flags events for retraining. Full dynamic threshold adaptation is scoped for v2.

---

#### GAP 7: Lack of Multi-Vector Coordinated Attack Handling

**What exists:** Most prototypes handle single attack types (brute force, port scan, DDoS) in isolation.

**What's missing:** Coordinated multi-vector attacks (e.g., port scan to identify open services → brute force on discovered SSH → API flooding as a distraction) require cross-event correlation that single-attack detection pipelines miss.

**AegisAI's answer (partial):** The Event Normalizer aggregates events across services into a shared timeline. The AI Security Agent has access to the multi-service event window, enabling it to classify related events as a coordinated campaign. Full APT-chain modeling is scoped for v2.

---

## 3. Novelty & Positioning

### 3.1 Core Novelty Statement

> *AegisAI introduces a resource-aware, closed-loop cyber-defense mechanism that dynamically generates and applies security policies for individual services based on real-time behavioral threat analysis, while coordinating firewall adaptation, service isolation, credential rotation, and automated recovery — with every AI-generated action gated through a deterministic policy engine.*

### 3.2 Four Novelty Components

**1. Resource-Level Adaptive Defense**
Each protected service (Web, API, DB, SSH) maintains its own independently evolving security policy. Attacks on one service do not trigger blanket system-wide response.

**2. Attack-Specific Policy Generation**
Response is attack-class-aware, not generic. Brute force → auth restriction + rate limit. Port scan → port restriction. Credential compromise → revoke + rotate + force re-auth. API flooding → rate limit + source block (DB untouched).

**3. Complete Closed-Loop Autonomous Operation**
The system moves from detection through recovery without human intervention, with the option to require human approval for high-severity irreversible actions (configurable by policy).

**4. Structurally Grounded Explainability**
Every displayed explanation corresponds to an actually-validated action. The LLM's output and the policy engine's decision are jointly logged, creating a verifiable audit trail.

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
                        INTERNET / ATTACKER
                               │
                               ▼
               ┌──────────────────────────────┐
               │       Traffic Collector      │
               │  Network + API + Auth Logs   │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │      Event Normalizer        │
               │  Dedup · Enrich · Timeline   │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │    IDS / Anomaly Engine      │
               │  Suricata + Isolation Forest │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │      AI SECURITY AGENT       │
               │                              │
               │  Threat Classification       │
               │  Risk Assessment             │
               │  Attack Analysis             │
               │  Response Recommendation     │
               │  Explainability Generation   │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │        POLICY ENGINE         │
               │                              │
               │  Validate AI Decision        │
               │  Check Permission Matrix     │
               │  Apply Safety Constraints    │
               │  Human-in-loop Gate (opt.)   │
               └──────────────┬───────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐
  │  FIREWALL   │    │  ISOLATION   │    │   CREDENTIAL     │
  │   ENGINE    │    │   ENGINE     │    │     ENGINE       │
  │             │    │              │    │                  │
  │ nftables    │    │ Docker nets  │    │ Revoke · Rotate  │
  │ Dynamic     │    │ Service      │    │ Re-establish     │
  │ rule gen    │    │ quarantine   │    │ Secret store     │
  └──────┬──────┘    └──────┬───────┘    └────────┬─────────┘
         │                  │                     │
         ▼                  ▼                     ▼
  Service A/C          Service B            Token / API Key
         │                  │                     │
         └──────────────────┼─────────────────────┘
                            ▼
               ┌──────────────────────────────┐
               │        EVENT DATABASE        │
               │    PostgreSQL · Redis        │
               │    Hash-Chained Audit Log    │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │   MONITORING + RECOVERY      │
               │                              │
               │  Threat clearance detection  │
               │  Baseline policy rollback    │
               │  Service health verification │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │       SOC DASHBOARD          │
               │                              │
               │  Real-time threat feed       │
               │  Per-service policy state    │
               │  AI decision log             │
               │  Incident timeline           │
               │  System health metrics       │
               │  Audit trail viewer          │
               └──────────────────────────────┘
```

### 4.2 Trust Boundary Model

```
┌────────────────────────────────────────────┐
│             AI REASONING LAYER             │
│    (LLM + ML — recommendations only)      │
└─────────────────┬──────────────────────────┘
                  │  Proposed Action
                  ▼
┌────────────────────────────────────────────┐  ← TRUST BOUNDARY
│             POLICY ENGINE                  │
│   Deterministic · Rule-constrained         │
│   Permission matrix · Safety checks        │
└─────────────────┬──────────────────────────┘
                  │  Validated, permitted action
                  ▼
┌────────────────────────────────────────────┐
│         INFRASTRUCTURE CONTROLS           │
│  Firewall · Isolation · Credentials       │
└────────────────────────────────────────────┘
```

The AI does not directly control infrastructure. This is the single most important architectural decision — it makes the system auditable, predictable, and safe.

### 4.3 The 30-Layer Deep Defense Firewall Architecture

To achieve absolute granular control over every aspect of the infrastructure, AegisAI implements an unprecedented **30-Layer Deep Defense Firewall Model**. This extends far beyond traditional OSI layers, filtering threats down to the cryptographic and kernel instruction level:

*   **Layers 1-7 (Network & Transport Base):** Traditional OSI model inspection, from physical signaling anomalies up to basic Application Layer (HTTP/DNS) filtering.
*   **Layers 8-12 (Identity, Access & Session):** Zero-Trust Network Access (ZTNA) Broker, Multi-Factor Authentication enforcement, continuous session hijacking monitoring, token lifecycle management, and behavioral biometric profiling.
*   **Layers 13-17 (API, Service & Protocol):** GraphQL/REST precise schema validation, gRPC payload inspection, shadow API detection, microservice-to-microservice mutual TLS enforcement, and parameter fuzzing defense.
*   **Layers 18-22 (OS & Kernel Execution):** eBPF-based Syscall filtering, memory integrity checking (blocking buffer overflows and ROP chains), container namespace isolation enforcement, and dynamic AppArmor/SELinux profile generation.
*   **Layers 23-26 (AI & Semantic Reasoning):** LLM Prompt Injection blocking, data exfiltration semantic analysis, DGA (Domain Generation Algorithm) decoding, and behavioral clustering of payloads.
*   **Layers 27-30 (Cryptographic & Data State):** Data-in-use secure enclave monitoring, ransomware file-system entropy halting, homomorphic encryption threat analysis, and continuous state-rollback execution verification.

---

## 5. Feature Specification

### 5.1 Detection Features

| Feature | Description | Priority |
|---|---|---|
| Network traffic monitoring | Capture and analyze ingress/egress packets | P0 |
| Authentication event monitoring | Track login attempts, failure rates, source IPs | P0 |
| API behavior monitoring | Request rate, endpoint distribution, error rates | P0 |
| Suricata IDS integration | Signature-based detection for known attack patterns | P0 |
| Isolation Forest anomaly detection | Unsupervised ML for behavioral baseline deviation | P0 |
| Multi-service event correlation | Cross-service timeline for coordinated attack detection | P1 |
| APT chain detection | Sequential attack phase recognition | P2 |
| Threat score real-time update | Continuous risk score per service (0–100) | P0 |

### 5.2 AI Agent Features

| Feature | Description | Priority |
|---|---|---|
| Attack classification | Identify attack type from event features | P0 |
| Confidence scoring | Probability estimate for each classification | P0 |
| Evidence extraction | List of specific behavioral indicators supporting classification | P0 |
| Response recommendation | Propose attack-appropriate actions per service | P0 |
| Risk assessment | Estimate impact severity and blast radius | P0 |
| Natural language explanation | Human-readable summary of threat and rationale | P0 |
| Multi-attack disambiguation | Distinguish concurrent or sequential attack classes | P1 |

### 5.3 Policy Engine Features

| Feature | Description | Priority |
|---|---|---|
| Permission matrix | Defines which actions are permitted per service type | P0 |
| Safety constraint validation | Blocks actions exceeding defined risk thresholds | P0 |
| Human-in-loop gate | Require operator approval for irreversible high-severity actions | P0 |
| Action atomicity | Ensures each action either fully executes or rolls back | P0 |
| Policy versioning | Every policy state is versioned with timestamp and trigger | P0 |
| Dry-run mode | Simulate action effects without executing | P1 |

### 5.4 Firewall Engine Features

| Feature | Description | Priority |
|---|---|---|
| Dynamic rule generation | Generate nftables rules from policy decisions | P0 |
| Per-service rule scope | Rules apply to specific services, not system-wide | P0 |
| Source IP blocking | Block specific attacker IPs | P0 |
| Rate limiting | Throttle connections from suspicious sources | P0 |
| Port restriction | Close exposed ports on targeted services | P0 |
| Rule expiry | Temporary rules auto-expire after configurable TTL | P0 |
| Rule rollback | Restore previous firewall state on threat clearance | P0 |

### 5.5 Isolation Engine Features

| Feature | Description | Priority |
|---|---|---|
| Service network isolation | Move service to quarantine Docker network | P0 |
| Controlled reconnection | Re-attach service to main network after threat clearance | P0 |
| Traffic logging during isolation | Capture all traffic to/from isolated service | P1 |

### 5.6 Credential Engine Features

| Feature | Description | Priority |
|---|---|---|
| Credential revocation | Invalidate active tokens/keys for targeted service | P0 |
| Credential rotation | Generate replacement credential with new version ID | P0 |
| Service re-establishment | Update service config to use new credential | P0 |
| Secret store integration | Store and retrieve credentials from Vault-like service | P0 |
| Rotation audit log | Record old credential ID, new credential ID, timestamp, trigger | P0 |

### 5.7 Recovery Features

| Feature | Description | Priority |
|---|---|---|
| Threat clearance detection | Detect when attack traffic has ceased | P0 |
| Behavioral normalization check | Verify metrics have returned to baseline before rollback | P0 |
| Baseline policy restoration | Revert temporary policies to pre-incident state | P0 |
| Recovery audit entry | Log recovery event with duration and actions reversed | P0 |

### 5.8 SOC Dashboard Features

| Feature | Description | Priority |
|---|---|---|
| Real-time threat feed | WebSocket-pushed event stream | P0 |
| Per-service status indicators | Green/Amber/Red per service with threat score | P0 |
| AI decision log | Time-stamped log of every AI recommendation and policy engine verdict | P0 |
| Incident timeline | Chronological view of attack events and responses | P0 |
| Firewall rule diff view | Before/After view for every rule change | P0 |
| Credential event log | Revocation and rotation events | P0 |
| Security report generation | End-of-incident summary (LLM-generated) | P1 |
| Audit trail viewer | Hash-chained immutable log browser | P1 |

### 5.9 Audit & Compliance Features

| Feature | Description | Priority |
|---|---|---|
| Hash-chained audit log | Every event references SHA-256 hash of previous entry | P0 |
| Tamper detection | Log integrity check on read | P0 |
| Full decision provenance | Every action traceable to triggering event and AI reasoning | P0 |
| Export | JSON and CSV export of incident reports | P1 |

---

## 6. AI/ML Pipeline

### 6.1 Detection Pipeline

```
Raw Events (Suricata alerts, auth logs, API logs)
         │
         ▼
   Event Normalizer
   ─────────────────
   · Deduplicate
   · Timestamp alignment
   · Source IP enrichment
   · Severity tagging
         │
         ▼
  Feature Extraction
  ─────────────────────────────────────────────
  · Login failure count (window: 60s)
  · Unique usernames targeted
  · Requests/minute per source IP
  · Port sweep breadth
  · API endpoint distribution entropy
  · Auth success/failure ratio
         │
         ▼
  ┌──────────────────────────────────┐
  │  Rule-Based Detection Layer      │
  │                                  │
  │  Brute force: >10 failures/60s   │
  │  Port scan: >20 ports/30s        │
  │  API flood: >500 req/min         │
  │  Cred compromise: token reuse    │
  └──────────────┬───────────────────┘
                 │
                 ▼
  ┌──────────────────────────────────┐
  │  ML Anomaly Detection            │
  │                                  │
  │  Isolation Forest                │
  │  · Trained on baseline traffic   │
  │  · Anomaly score per event       │
  │  · Threshold: configurable       │
  └──────────────┬───────────────────┘
                 │
                 ▼
           Threat Score
           (0–100, combined)
```

### 6.2 AI Agent Pipeline

```
Threat Score + Event Context
         │
         ▼
   AI Security Agent (LLM-augmented)
   ────────────────────────────────────
   Input:
     · Normalized event batch
     · Historical context (last 5 min)
     · Service topology
     · Current policy states

   Output (structured JSON):
     · attack_class: "brute_force" | "port_scan" | "api_flood" | "cred_compromise"
     · confidence: 0.0 – 1.0
     · evidence: [list of behavioral indicators]
     · affected_services: [service_ids]
     · recommended_actions: [action_objects]
     · explanation: "natural language rationale"
     · severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
         │
         ▼
   Policy Engine Validation
   ────────────────────────────────────
   · Check action against permission matrix
   · Verify severity threshold for auto-execute
   · If action is irreversible AND severity >= CRITICAL:
       → Hold for human approval
   · Apply safety constraints
         │
         ▼
   Validated Action Set → Execution
```

### 6.3 ML Model Selection Rationale

| Model | Use Case | Rationale |
|---|---|---|
| Isolation Forest | Anomaly detection | Unsupervised; no labeled attack data required; low FP at moderate contamination |
| Random Forest / XGBoost | Attack classification (supervised) | High accuracy on tabular security features; interpretable feature importance |
| LLM (claude-sonnet / local) | Explanation + recommendation | Semantic reasoning; natural language output; NOT used for direct execution |
| Rule engine | Primary detection triggers | Deterministic; zero latency; high reliability for known attack patterns |

**Hybrid rationale:** Pure ML is unreliable in high-stakes autonomous execution. Pure rules miss novel attacks. The hybrid approach uses rules as the primary detection trigger and ML as a confidence booster and novelty detector. The LLM adds semantic reasoning for complex multi-vector scenarios that neither rules nor ML handle well alone.

---

## 7. Tech Stack

### 7.1 Stack Summary

| Layer | Technology | Justification |
|---|---|---|
| Frontend | React + TypeScript | Type safety; component reuse; ecosystem |
| UI Styling | Tailwind CSS | Rapid prototyping; dark mode SOC aesthetics |
| Charts | Recharts | React-native; lightweight |
| Real-time | WebSocket | Sub-second dashboard updates |
| Backend | Python FastAPI | ML ecosystem; async; rapid API dev |
| Database | PostgreSQL | Relational; ACID; complex event queries |
| Cache / Events | Redis | Real-time event queue; rate limiting |
| IDS | Suricata | Industry-standard; rule + anomaly detection |
| Firewall Control | nftables | Modern Linux firewall; programmatic rule management |
| Containerization | Docker + Compose | Isolated cyber lab; reproducible demo |
| ML | scikit-learn | Isolation Forest; Random Forest; XGBoost |
| AI Agent | Python + LLM API | Recommendation and explanation layer |
| Secret Management | Vault-like service | Secure credential store; rotation support |
| Auth | JWT + RBAC | Dashboard access control |
| OS | Ubuntu 24.04 LTS | nftables support; Docker stability |

### 7.2 Backend Project Structure

```
backend/
├── api/                    # FastAPI route definitions
│   ├── events.py           # Incoming event ingestion
│   ├── dashboard.py        # Dashboard data endpoints
│   └── websocket.py        # WebSocket manager
├── agents/                 # AI Security Agent
│   ├── classifier.py       # Attack classification
│   ├── reasoner.py         # LLM-based analysis
│   └── recommender.py      # Response recommendation
├── detection/              # IDS + ML
│   ├── normalizer.py       # Event normalization
│   ├── features.py         # Feature extraction
│   ├── rules.py            # Rule-based detection
│   └── anomaly.py          # Isolation Forest
├── policy/                 # Policy Engine
│   ├── engine.py           # Validation and gating
│   ├── permissions.py      # Permission matrix
│   └── constraints.py      # Safety constraints
├── firewall/               # Firewall Engine
│   ├── generator.py        # nftables rule generation
│   ├── executor.py         # Rule application
│   └── rollback.py         # Rule reversion
├── isolation/              # Isolation Engine
│   ├── docker_ctrl.py      # Docker network management
│   └── quarantine.py       # Service quarantine logic
├── credentials/            # Credential Engine
│   ├── vault.py            # Secret store interface
│   ├── rotator.py          # Rotation logic
│   └── re_establish.py     # Service credential update
├── recovery/               # Recovery Engine
│   ├── monitor.py          # Threat clearance detection
│   └── rollback.py         # Baseline restoration
├── audit/                  # Audit Logging
│   ├── logger.py           # Hash-chained log writer
│   └── verifier.py         # Integrity check
├── models/                 # DB models (SQLAlchemy)
└── database/               # DB connection + migrations
```

### 7.3 Frontend Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ServiceStatusGrid/     # Per-service health cards
│   │   ├── ThreatFeed/            # Real-time event stream
│   │   ├── AIDecisionLog/         # Agent reasoning viewer
│   │   ├── FirewallRuleDiff/      # Before/After rule view
│   │   ├── CredentialEventLog/    # Rotation tracker
│   │   ├── IncidentTimeline/      # Chronological view
│   │   └── AuditTrailViewer/      # Hash-chain browser
│   ├── hooks/
│   │   └── useWebSocket.ts        # Real-time event subscription
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Incidents.tsx
│   │   └── AuditLog.tsx
│   └── types/
│       └── events.ts              # Shared type definitions
```

---

## 8. Module-Level Design

### 8.1 Event Schema

```json
{
  "event_id": "uuid",
  "timestamp": "ISO-8601",
  "source_ip": "10.10.10.X",
  "target_service": "ssh_server | api_server | web_server | database",
  "event_type": "auth_failure | port_sweep | api_request | network_anomaly",
  "raw_data": {},
  "suricata_alert": { "sid": 1001, "msg": "ET SCAN..." },
  "anomaly_score": 0.87,
  "threat_score": 74
}
```

### 8.2 AI Agent Output Schema

```json
{
  "analysis_id": "uuid",
  "trigger_event_ids": ["uuid1", "uuid2"],
  "attack_class": "brute_force",
  "confidence": 0.96,
  "severity": "HIGH",
  "evidence": [
    "37 failed login attempts in 60s",
    "3 distinct usernames targeted",
    "Single source IP: 10.10.10.X",
    "8 attempts/minute sustained"
  ],
  "affected_services": ["ssh_server"],
  "recommended_actions": [
    { "type": "block_ip", "target": "10.10.10.X", "scope": "ssh_server", "ttl": 3600 },
    { "type": "rate_limit", "target": "ssh_server", "threshold": "5/min", "ttl": 1800 },
    { "type": "rotate_credential", "credential_id": "SSH_SERVICE_KEY_V1" }
  ],
  "explanation": "High-confidence SSH brute-force attack from 10.10.10.X. Sustained failed authentication rate exceeds baseline by 40x with multi-username targeting pattern. Credential rotation recommended due to possible credential enumeration intent.",
  "auto_execute_eligible": true
}
```

### 8.3 Policy Engine Decision Schema

```json
{
  "analysis_id": "uuid",
  "actions_validated": [
    { "action": "block_ip", "verdict": "APPROVED", "reason": "within permission matrix" },
    { "action": "rate_limit", "verdict": "APPROVED", "reason": "within permission matrix" },
    { "action": "rotate_credential", "verdict": "APPROVED", "reason": "brute_force class auto-approved" }
  ],
  "actions_blocked": [],
  "human_approval_required": false,
  "execution_timestamp": "ISO-8601"
}
```

### 8.4 Audit Log Entry Schema

```json
{
  "log_id": "uuid",
  "timestamp": "ISO-8601",
  "entry_type": "detection | ai_decision | policy_verdict | action_executed | recovery",
  "content": {},
  "previous_hash": "sha256:...",
  "current_hash": "sha256:..."
}
```

---

## 9. Security Design Decisions

### 9.1 Why the AI Does Not Execute Directly

The core risk of LLM-based autonomous systems is that unconstrained LLM reasoning under ambiguous or adversarial observations has been shown to produce unsafe mitigation actions and false-positive responses. By inserting a deterministic Policy Engine between the AI recommendation and infrastructure control:

- Actions are bounded to a predefined, auditable set
- Hallucinated recommendations are blocked (e.g., LLM proposes deleting a database — policy engine rejects)
- Every execution is traceable to a specific validated action record

### 9.2 Human-in-Loop Threshold

The following action classes require human approval regardless of AI confidence:

| Action | Threshold |
|---|---|
| Full service shutdown | Always |
| Database isolation | Severity >= CRITICAL |
| System-wide IP block | Always |
| Bulk credential revocation | Always |
| Firewall policy reset | Always |

Lower-severity actions (rate limiting, single-IP block, single service isolation) are auto-executable when confidence >= 0.85.

### 9.3 Hash-Chained Audit Log

Every audit log entry computes:

```
current_hash = SHA256(previous_hash + timestamp + content_json)
```

This creates a tamper-evident chain. Any modification to a historical entry invalidates all subsequent hashes, detectable on verification.

### 9.4 Scope Limitations (Scoped Claims)

The prototype demonstrates autonomous defense against the following attack classes:

- SSH brute-force authentication attacks
- Network port scanning
- API request flooding (HTTP flood)
- Credential exposure simulation

It does not claim to defend against: zero-day exploits, firmware attacks, supply chain compromise, or adversarial ML attacks on the detection model.

---

## 10. Demo Environment

### 10.1 Docker Cyber Lab

```yaml
# docker-compose.yml (conceptual)
services:
  web_server:       # nginx
  api_server:       # FastAPI sample app
  ssh_server:       # OpenSSH
  database:         # PostgreSQL
  attacker:         # Kali Linux / custom attack scripts
  monitoring_agent: # Suricata + log forwarder
  aegisai_backend:  # AegisAI core
  aegisai_frontend: # React dashboard

networks:
  protected_network:
  quarantine_network:   # Services moved here on isolation
  management_network:   # AegisAI internal
```

### 10.2 Attack Simulation Scripts

```python
# SSH Brute Force
for i in range(50):
    attempt_ssh_login(target="ssh_server", user=random_user(), password=random_password())
    time.sleep(0.5)

# Port Scan
nmap_scan(target="web_server", range="1-1000")

# API Flooding
for i in range(700):
    requests.get("http://api_server/endpoint")
    time.sleep(0.085)  # ~700 req/min
```

### 10.3 5-Minute Demo Script

**0:00–0:30 — Baseline**
Dashboard shows all services green. Risk score: ~12/100. Introduce the system.

**0:30–1:15 — SSH Brute Force Launch**
Run attack script. Dashboard shows failed login counter rising. Risk score climbs.

**1:15–2:00 — AI Detection**
AI agent fires. Display: attack class, confidence 96%, evidence list, recommended actions.

**2:00–3:00 — Autonomous Defense**
Policy engine approves. Firewall rule applied (show diff). Credential rotation initiated. Attacker simulation fails.

**3:00–3:40 — Credential Rotation**
Show revocation of SSH_SERVICE_KEY_V1, generation of V2, service reconnection.

**3:40–4:20 — Second Attack (API Flood)**
API flooding launched. System detects different attack class. Rate limit applied. DB untouched. Demonstrate resource-level independence.

**4:20–4:45 — Recovery**
Attacks stopped. System detects threat clearance. Temporary policies expire. All services return to green.

**4:45–5:00 — Final Report**
Display incident summary: 2 attacks detected, 2 contained, 1 credential rotated, 5 automated actions, avg response time 1.4s.

---

## 11. Evaluation Metrics

| Metric | Target | Description |
|---|---|---|
| Detection accuracy | >90% | Correctly classified attacks on test set |
| False positive rate | <5% | Legitimate traffic incorrectly flagged |
| Mean time to detect (MTTD) | <10s | Detection latency from attack onset |
| Mean time to respond (MTTR) | <5s | Time from detection to first defensive action |
| Credential rotation time | <30s | Revoke → rotate → re-establish |
| Audit log integrity | 100% | Hash chain verification pass rate |
| Dashboard latency | <500ms | Event to UI display time |

---

## 12. Future Roadmap

### v1.0 (SIH Demo)
- Core 8-stage closed loop
- 4 attack classes
- Per-service firewall + isolation + credential engines
- SOC dashboard with real-time feed
- Hash-chained audit log

### v2.0
- Multi-vector APT chain detection
- Dynamic false-positive threshold adaptation
- Federated deployment across containerized clusters
- MITRE ATT&CK mapping overlay on dashboard
- Formal verification of policy engine rules

### v3.0
- Reinforcement learning-based policy optimization (post-incident learning)
- Integration with SIEM platforms (Splunk, Elastic)
- Zero-trust network architecture integration
- Regulatory compliance reporting (NIS2, DORA)

---

## 13. Ultimate Vision & Complete Feature Coverage

To ensure AegisAI covers every conceivable gap in modern and future cyber defense, the platform's ultimate roadmap includes 26 paradigm-shifting features across multiple security domains:

1.  **eBPF-Based Kernel Tracing:** Zero-day exploit blocking at the Linux syscall level without kernel panics.
2.  **Quantum-Resistant Cryptography Engine:** Preparing data enclaves for post-quantum decryption threats.
3.  **Hardware-Rooted Attestation (TPM/SGX):** Verifying physical node integrity before allowing it to enforce cluster policies.
4.  **Federated Threat Intelligence Swarm:** Multiple isolated AegisAI deployments sharing threat vectors globally and anonymously.
5.  **Dynamic Deception & Honeypot Meshes:** Instantly spinning up fake, vulnerable services (shadow clones) to trap attackers in a sandboxed reality.
6.  **Automated Malware Detonation Sandbox:** Detonating unknown payloads in ephemeral micro-VMs to extract Indicators of Compromise (IOCs).
7.  **Digital Twin Cyber Range:** Simulating both attacks and defenses on a digital twin of the network before applying them to production.
8.  **LLM Prompt Injection & Jailbreak Defense:** Dedicated semantic firewall layers for protecting enterprise AI models hosted behind Aegis.
9.  **Dark Web Active Reconnaissance:** AI agents actively scraping dark web forums for leaked credentials or zero-days related to the organization's stack.
10. **Continuous Autonomous Red Teaming:** Internal AI agents constantly probing the system to find and patch vulnerabilities before attackers do.
11. **Supply Chain Vulnerability Hot-Patching:** Automatically detecting vulnerable open-source dependencies and patching them in memory at runtime.
12. **Cross-Cloud Unified Fabric:** Enforcing policies identically across AWS, Azure, GCP, and On-Premises environments from a single brain.
13. **OT/ICS/SCADA Protocol Inspection:** Deep packet inspection for industrial control systems (power grids, manufacturing plants).
14. **Blockchain-Based Immutable Audit Ledger:** Storing AI decisions on a private, decentralized ledger for absolute legal non-repudiation.
15. **Automated Compliance & Legal Reporting:** Auto-generating GDPR, HIPAA, and SOC2 breach notification reports in real-time.
16. **Biometric Insider Threat Detection:** Analyzing user keystroke dynamics and mouse movements to detect stolen, authenticated sessions.
17. **Infrastructure-as-Code (IaC) Self-Healing:** Redeploying entire compromised VPCs from known-good Terraform state files automatically.
18. **Ransomware Entropy Interception:** Halting processes at the OS level immediately if rapid file-encryption (entropy spiking) is detected.
19. **Autonomous IAM Role Shrinking:** Automatically stripping unused permissions from cloud service accounts (dynamic Least Privilege enforcement).
20. **Satellite & Edge Node Defense:** Lightweight, highly autonomous defensive agents for 5G, IoT, and disconnected edge environments.
21. **Cyber-Kinetic Impact Modeling:** Predicting the physical-world damage (e.g., thermal overload, mechanical failure) of a cyber attack on connected hardware.
22. **Homomorphic Encryption Firewall:** Analyzing traffic and data for threats while it remains mathematically encrypted, preserving absolute privacy.
23. **Social Engineering / Phishing Pre-cognition:** Correlating email/communications anomalies with unusual downstream network traffic.
24. **Memory-Safe Language Rewriting:** AI suggesting and compiling memory-safe (Rust) rewrites for vulnerable C/C++ legacy code dynamically.
25. **Multi-Agent Negotiation:** The defense AI negotiating with or deceiving the attacker's automated AI to waste its computational resources.
26. **Automated Threat Hunting:** Proactively querying the environment's telemetry lakes for signs of Advanced Persistent Threats (APTs) lying dormant in the network.

---

## 14. References

> Key papers and reports informing this design:

1. Rangappa, A.S. (2025). Agentic AI and Cyber Security: Autonomous Threat Hunting, Intrusion Detection, and Adaptive Defense Mechanisms. *Journal of Digital Security and Forensics, 2(1).*
2. Garcia et al. (2024). Comparative benchmarking of agentic AI frameworks (LangChain, AutoGen, CrewAI, MetaGPT, AgentVerse) on CyberSecEval.
3. ScienceDirect (2026). Explainable autonomous cyber defense using adversarial multi-agent reinforcement learning.
4. IBM Security (2024). Cost of a Data Breach Report. Average breach cost: $4.88M; breach lifecycle: 258 days.
5. ISACA Journal (2025). "Automate the routine, escalate the consequential" — design pattern for autonomous IR.
6. Cloud Security Alliance (2026). Agentic AI Autonomy Levels and Control Framework, v1.1.
7. DARPA AIxCC (2024–2025). AI agents demonstrated finding and patching open-source vulnerabilities faster than human teams.
8. Huang et al. (2025). LLM hallucination behavior in autonomous cyber agent deployments.
9. MDPI Journal of Cybersecurity and Privacy (2025). AI-Augmented SOC: LLMs and Agents for Security Automation.
10. ScienceDirect (2025–2026). Hallucination taxonomy in AI-driven cybersecurity systems.

---

*Document maintained by AegisAI development team. Last updated: August 2026.*
