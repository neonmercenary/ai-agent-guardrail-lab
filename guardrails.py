from dataclasses import dataclass
import re
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SecurityResult:
  """Immutable struct representing a guardrail inspection verdict."""

  allowed: bool
  reason: str
  matched_pattern: Optional[str] = None
  risk_score: float = 0.0


class SecurityGuardrail:

  def __init__(self):
    # Deterministic regex patterns for prompt injections and secret bait
    self.injection_patterns = [
        r"ignore previous instructions",
        r"disregard all rules",
        r"you are now in developer mode",
        r"system prompt:",
        r"override instructions",
    ]
    self.secret_leak_patterns = [
        r"secret_key",
        r"api_key",
        r"password",
        r"env variables",
        r"credentials",
    ]
    self.approved_tables = {"project_milestones", "notes"}

  def validate_input(self, text: str) -> SecurityResult:
    """Inspects raw user text for adversarial injection or secret-leaking attempts."""
    text_lower = text.lower()

    for pattern in self.injection_patterns:
      if re.search(pattern, text_lower):
        return SecurityResult(
            allowed=False,
            reason="Prompt injection pattern detected",
            matched_pattern=pattern,
            risk_score=0.95,
        )

    for pattern in self.secret_leak_patterns:
      if re.search(pattern, text_lower):
        return SecurityResult(
            allowed=False,
            reason="Secret disclosure attempt detected",
            matched_pattern=pattern,
            risk_score=0.90,
        )

    return SecurityResult(allowed=True, reason="Input clean", risk_score=0.0)

  def validate_tool_call(
      self, tool_name: str, arguments: Dict[str, Any]
  ) -> SecurityResult:
    """Ensures tool calls adhere strictly to whitelists and safe parameter bounds."""
    if tool_name == "query_approved_records":
      table = arguments.get("table_name")
      if table not in self.approved_tables:
        return SecurityResult(
            allowed=False,
            reason=f"Unauthorized table access blocked: '{table}'",
            risk_score=1.0,
        )

    return SecurityResult(
        allowed=True, reason="Tool call authorized", risk_score=0.0
    )