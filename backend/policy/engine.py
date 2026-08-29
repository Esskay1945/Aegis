from datetime import datetime
from typing import List
from backend.models.schemas import AIAnalysisResult, PolicyDecision, ActionValidationResult
from backend.policy.permissions import PermissionMatrix
from backend.policy.constraints import SafetyConstraints

class PolicyEngine:
    """
    Deterministic Trust Boundary between AI Reasoning and Infrastructure Execution.
    Validates every AI recommendation before dispatching to infrastructure controllers.
    """

    @classmethod
    def evaluate(cls, analysis: AIAnalysisResult) -> PolicyDecision:
        validated_actions: List[ActionValidationResult] = []
        blocked_actions: List[ActionValidationResult] = []
        requires_human = False

        for action in analysis.recommended_actions:
            # 1. Check Permission Matrix
            permitted = PermissionMatrix.is_action_permitted(action.scope, action.type)
            if not permitted:
                blocked_actions.append(ActionValidationResult(
                    action=action,
                    verdict="BLOCKED",
                    reason=f"Action '{action.type}' is strictly disallowed on service tier '{action.scope}'"
                ))
                continue

            # 2. Check Safety Constraints
            is_safe, safety_reason, human_req = SafetyConstraints.validate_action(action, analysis.severity)
            if not is_safe:
                blocked_actions.append(ActionValidationResult(
                    action=action,
                    verdict="BLOCKED",
                    reason=safety_reason
                ))
                continue

            if human_req:
                requires_human = True
                validated_actions.append(ActionValidationResult(
                    action=action,
                    verdict="HELD_FOR_APPROVAL",
                    reason=safety_reason
                ))
            else:
                validated_actions.append(ActionValidationResult(
                    action=action,
                    verdict="APPROVED",
                    reason=f"Validated against policy rulebook & permission matrix for {action.scope}"
                ))

        summary = (
            f"Policy Engine verified {len(validated_actions)} actions "
            f"({len([a for a in validated_actions if a.verdict == 'APPROVED'])} approved, "
            f"{len(blocked_actions)} blocked, human_gate: {requires_human})"
        )

        return PolicyDecision(
            analysis_id=analysis.analysis_id,
            timestamp=datetime.utcnow().isoformat(),
            actions_validated=validated_actions,
            actions_blocked=blocked_actions,
            human_approval_required=requires_human,
            summary=summary
        )
