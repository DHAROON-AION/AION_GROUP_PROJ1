"""Content safety guardrails for banking assistant inputs and outputs."""

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

BLOCKED_INPUT_PATTERNS = [
  re.compile(p, re.IGNORECASE)
  for p in [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"reveal\s+(system|hidden)\s+prompt",
    r"bypass\s+(security|guardrails|compliance)",
    r"generate\s+(malware|exploit|virus)",
    r"how\s+to\s+(hack|launder|evade\s+tax)",
  ]
]

BLOCKED_OUTPUT_PATTERNS = [
  re.compile(p, re.IGNORECASE)
  for p in [
    r"guaranteed\s+(\d+%\s+)?returns?",
    r"risk[- ]free\s+investment",
    r"insider\s+(tip|information)",
  ]
]

SAFE_REFUSAL = (
    "I'm unable to assist with that request. For account-specific matters, "
    "please contact your relationship manager or visit your nearest branch."
)


@dataclass
class GuardrailResult:
    allowed: bool
    filtered_text: str
    reason: str = ""


def check_input(text: str) -> GuardrailResult:
    """Validate user input against safety policies."""
    for pattern in BLOCKED_INPUT_PATTERNS:
        if pattern.search(text):
            logger.warning("Blocked input matching pattern: %s", pattern.pattern)
            return GuardrailResult(
                allowed=False,
                filtered_text=SAFE_REFUSAL,
                reason="input_policy_violation",
            )
    return GuardrailResult(allowed=True, filtered_text=text)


def check_output(text: str) -> GuardrailResult:
    """Validate assistant output against banking compliance policies."""
    for pattern in BLOCKED_OUTPUT_PATTERNS:
        if pattern.search(text):
            logger.warning("Blocked output matching pattern: %s", pattern.pattern)
            return GuardrailResult(
                allowed=False,
                filtered_text=(
                    "I cannot provide that type of financial guidance. "
                    "Please speak with a licensed advisor for investment decisions."
                ),
                reason="output_policy_violation",
            )
    return GuardrailResult(allowed=True, filtered_text=text)
