import hashlib
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.models.schemas import AuditLogEntry

GENESIS_HASH = "0" * 64

class AuditLogger:
    """Tamper-evident, hash-chained SHA-256 immutable audit ledger."""

    def __init__(self):
        self.chain: List[AuditLogEntry] = []
        self._bootstrap_genesis_block()

    def _bootstrap_genesis_block(self):
        now = datetime.utcnow().isoformat()
        content = {
            "system": "AegisAI Autonomous Cyber Defense Agent",
            "event": "GENESIS_LEDGER_INIT",
            "version": "1.0-SIH"
        }
        raw_str = GENESIS_HASH + now + json.dumps(content, sort_keys=True)
        curr_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

        genesis = AuditLogEntry(
            log_id=str(uuid.uuid4()),
            timestamp=now,
            entry_type="detection",
            content=content,
            previous_hash=GENESIS_HASH,
            current_hash=curr_hash
        )
        self.chain.append(genesis)

    def log_event(self, entry_type: str, content: Dict[str, Any]) -> AuditLogEntry:
        prev_hash = self.chain[-1].current_hash if self.chain else GENESIS_HASH
        now = datetime.utcnow().isoformat()
        
        # Compute SHA-256 hash chaining
        serialized_content = json.dumps(content, sort_keys=True, default=str)
        raw_data = prev_hash + now + serialized_content
        curr_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()

        entry = AuditLogEntry(
            log_id=str(uuid.uuid4()),
            timestamp=now,
            entry_type=entry_type,
            content=content,
            previous_hash=prev_hash,
            current_hash=curr_hash
        )
        self.chain.append(entry)
        return entry

    def get_entries(self, limit: int = 100) -> List[AuditLogEntry]:
        return self.chain[-limit:]

    def reset(self):
        self.chain.clear()
        self._bootstrap_genesis_block()
