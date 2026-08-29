import datetime
from typing import Dict, Any, List, Optional
from backend.models.schemas import ServiceId

class IsolationEngine:
    """Manages container network quarantine and controlled forensic re-connection."""

    def __init__(self):
        self.quarantined_services: Dict[ServiceId, Dict[str, Any]] = {}

    def isolate_service(self, service_id: ServiceId, reason: str = "") -> Dict[str, Any]:
        record = {
            "service_id": service_id,
            "status": "QUARANTINED",
            "isolated_at": datetime.datetime.utcnow().isoformat(),
            "reason": reason,
            "network": "quarantine_isolated_net"
        }
        self.quarantined_services[service_id] = record
        return record

    def reconnect_service(self, service_id: ServiceId) -> Optional[Dict[str, Any]]:
        record = self.quarantined_services.pop(service_id, None)
        if record:
            record["status"] = "RECONNECTED"
            record["reconnected_at"] = datetime.datetime.utcnow().isoformat()
            record["network"] = "protected_network"
        return record

    def is_isolated(self, service_id: ServiceId) -> bool:
        return service_id in self.quarantined_services

    def get_quarantined(self) -> List[Dict[str, Any]]:
        return list(self.quarantined_services.values())

    def reset(self):
        self.quarantined_services.clear()
