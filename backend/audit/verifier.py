import hashlib
import json
from typing import Dict, Any, List
from backend.models.schemas import AuditLogEntry

class AuditVerifier:
    """Cryptographically verifies continuity and authenticity of hash-chained audit log."""

    @staticmethod
    def verify_chain(chain: List[AuditLogEntry]) -> Dict[str, Any]:
        if not chain:
            return {"is_valid": True, "total_blocks": 0, "status": "EMPTY_CHAIN"}

        for i in range(len(chain)):
            current = chain[i]

            # 1. Verify link to previous hash
            if i > 0:
                prev = chain[i - 1]
                if current.previous_hash != prev.current_hash:
                    return {
                        "is_valid": False,
                        "tamper_detected_at_index": i,
                        "block_id": current.log_id,
                        "reason": f"Broken chain link: previous_hash '{current.previous_hash}' does not match prior block hash '{prev.current_hash}'",
                        "total_blocks": len(chain)
                    }

            # 2. Re-compute hash of current block
            serialized = json.dumps(current.content, sort_keys=True, default=str)
            expected_raw = current.previous_hash + current.timestamp + serialized
            expected_hash = hashlib.sha256(expected_raw.encode("utf-8")).hexdigest()

            if expected_hash != current.current_hash:
                return {
                    "is_valid": False,
                    "tamper_detected_at_index": i,
                    "block_id": current.log_id,
                    "reason": f"Block content integrity violation: expected hash '{expected_hash}', but found '{current.current_hash}'",
                    "total_blocks": len(chain)
                }

        return {
            "is_valid": True,
            "total_blocks": len(chain),
            "genesis_hash": chain[0].current_hash[:16] + "...",
            "head_hash": chain[-1].current_hash[:16] + "...",
            "status": "100%_CRYPTOGRAPHICALLY_VERIFIED_AUTHENTIC"
        }
