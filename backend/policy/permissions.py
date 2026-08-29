from typing import Dict, Set
from backend.models.schemas import ServiceId, ActionType

class PermissionMatrix:
    """
    Defines which defensive action categories are permitted for each protected service.
    Guarantees that an AI cannot propose an inappropriate or unpermitted action for a specific service tier.
    """

    PERMITTED_ACTIONS: Dict[ServiceId, Set[ActionType]] = {
        "ssh_server": {
            "block_ip",
            "rate_limit",
            "rotate_credential",
            "port_restrict",
            "isolate_service"
        },
        "api_server": {
            "block_ip",
            "rate_limit",
            "rotate_credential",
            "isolate_service",
            "custom_rule"
        },
        "web_server": {
            "block_ip",
            "rate_limit",
            "port_restrict",
            "isolate_service",
            "custom_rule"
        },
        "database": {
            "block_ip",
            "rotate_credential",
            "isolate_service"
            # Note: rate_limit and port_restrict are restricted on DB to avoid cluster sync partitions
        }
    }

    @classmethod
    def is_action_permitted(cls, service_id: ServiceId, action_type: ActionType) -> bool:
        allowed = cls.PERMITTED_ACTIONS.get(service_id, set())
        return action_type in allowed
