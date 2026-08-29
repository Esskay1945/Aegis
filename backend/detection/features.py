from collections import defaultdict
from typing import Dict, List, Any
import time

class FeatureExtractor:
    """Extracts behavioral and temporal security features across sliding windows."""

    def __init__(self, window_seconds: int = 60):
        self.window_seconds = window_seconds
        # In-memory sliding window buffers
        self.auth_failures: Dict[str, List[float]] = defaultdict(list) # ip -> timestamps
        self.auth_usernames: Dict[str, List[str]] = defaultdict(list) # ip -> list of target usernames
        self.requests_per_ip: Dict[str, List[float]] = defaultdict(list) # ip -> timestamps
        self.ports_scanned: Dict[str, set] = defaultdict(set) # ip -> set of ports
        self.endpoint_hits: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int)) # ip -> endpoint -> count
        self.auth_successes: Dict[str, List[float]] = defaultdict(list) # ip -> timestamps

    def _prune_old(self, current_time: float):
        cutoff = current_time - self.window_seconds
        for ip in list(self.auth_failures.keys()):
            self.auth_failures[ip] = [t for t in self.auth_failures[ip] if t > cutoff]
        for ip in list(self.requests_per_ip.keys()):
            self.requests_per_ip[ip] = [t for t in self.requests_per_ip[ip] if t > cutoff]
        for ip in list(self.auth_successes.keys()):
            self.auth_successes[ip] = [t for t in self.auth_successes[ip] if t > cutoff]

    def record_event(self, source_ip: str, event_type: str, raw_data: Dict[str, Any]):
        now = time.time()
        self._prune_old(now)

        if event_type == "auth_failure":
            self.auth_failures[source_ip].append(now)
            user = raw_data.get("username") or raw_data.get("user")
            if user:
                self.auth_usernames[source_ip].append(user)
        elif event_type == "auth_success":
            self.auth_successes[source_ip].append(now)
        elif event_type == "api_request" or event_type == "http_request":
            self.requests_per_ip[source_ip].append(now)
            endpoint = raw_data.get("endpoint", "/")
            self.endpoint_hits[source_ip][endpoint] += 1
        elif event_type == "port_probe" or event_type == "port_sweep":
            port = raw_data.get("port")
            if port:
                self.ports_scanned[source_ip].add(port)

    def extract_features(self, source_ip: str) -> Dict[str, float]:
        now = time.time()
        self._prune_old(now)

        fail_count = len(self.auth_failures[source_ip])
        success_count = len(self.auth_successes[source_ip])
        req_count = len(self.requests_per_ip[source_ip])
        unique_users = len(set(self.auth_usernames[source_ip]))
        ports_count = len(self.ports_scanned[source_ip])
        
        # Calculate ratio safely
        total_auth = fail_count + success_count
        fail_ratio = (fail_count / total_auth) if total_auth > 0 else 0.0

        # Endpoint entropy proxy (diversity)
        endpoint_count = len(self.endpoint_hits[source_ip])

        return {
            "login_failures_60s": float(fail_count),
            "unique_usernames_targeted": float(unique_users),
            "requests_per_minute": float(req_count),
            "ports_scanned_30s": float(ports_count),
            "endpoint_diversity": float(endpoint_count),
            "auth_failure_ratio": float(fail_ratio)
        }

    def get_feature_vector(self, source_ip: str) -> List[float]:
        feats = self.extract_features(source_ip)
        return [
            feats["login_failures_60s"],
            feats["unique_usernames_targeted"],
            feats["requests_per_minute"],
            feats["ports_scanned_30s"],
            feats["endpoint_diversity"],
            feats["auth_failure_ratio"]
        ]

    def reset_ip(self, source_ip: str):
        self.auth_failures.pop(source_ip, None)
        self.auth_usernames.pop(source_ip, None)
        self.requests_per_ip.pop(source_ip, None)
        self.ports_scanned.pop(source_ip, None)
        self.endpoint_hits.pop(source_ip, None)
        self.auth_successes.pop(source_ip, None)

    def reset_all(self):
        self.auth_failures.clear()
        self.auth_usernames.clear()
        self.requests_per_ip.clear()
        self.ports_scanned.clear()
        self.endpoint_hits.clear()
        self.auth_successes.clear()
