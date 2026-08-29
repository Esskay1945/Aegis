import uuid
from datetime import datetime
from typing import Dict, List, Optional
from backend.models.schemas import CredentialRecord, ServiceId

class CredentialEngine:
    """Manages secret revocation, zero-downtime key rotation, and version tracking."""

    def __init__(self):
        self.credentials: Dict[str, CredentialRecord] = {}
        self.rotation_history: List[CredentialRecord] = []
        self._bootstrap_initial_credentials()

    def _bootstrap_initial_credentials(self):
        services: List[ServiceId] = ["ssh_server", "api_server", "web_server", "database"]
        now = datetime.utcnow().isoformat()
        for svc in services:
            key_id = f"{svc.upper()}_KEY_V1"
            rec = CredentialRecord(
                credential_id=key_id,
                service_id=svc,
                version="V1",
                status="ACTIVE",
                created_at=now,
                trigger="INITIAL_PROVISIONING"
            )
            self.credentials[svc] = rec
            self.rotation_history.append(rec)

    def rotate_credential(self, service_id: ServiceId, trigger_reason: str = "") -> CredentialRecord:
        current = self.credentials.get(service_id)
        current_version_num = 1
        if current:
            try:
                current_version_num = int(current.version.replace("V", ""))
            except Exception:
                current_version_num = 1
            current.status = "REVOKED"
            current.revoked_at = datetime.utcnow().isoformat()

        next_version = f"V{current_version_num + 1}"
        new_key_id = f"{service_id.upper()}_KEY_{next_version}"

        new_rec = CredentialRecord(
            credential_id=new_key_id,
            service_id=service_id,
            version=next_version,
            status="ACTIVE",
            created_at=datetime.utcnow().isoformat(),
            trigger=trigger_reason or "AUTONOMOUS_DEFENSE_TRIGGER"
        )
        if current:
            current.new_version_id = new_key_id

        self.credentials[service_id] = new_rec
        self.rotation_history.append(new_rec)
        return new_rec

    def get_current_credential(self, service_id: ServiceId) -> Optional[CredentialRecord]:
        return self.credentials.get(service_id)

    def get_rotation_history(self) -> List[CredentialRecord]:
        return self.rotation_history

    def reset(self):
        self.credentials.clear()
        self.rotation_history.clear()
        self._bootstrap_initial_credentials()
