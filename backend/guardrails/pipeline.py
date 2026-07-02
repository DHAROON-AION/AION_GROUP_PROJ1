"""Guardrail pipeline — orchestrates PII masking and content safety."""

import logging

from backend.guardrails.content_filter import check_input, check_output
from backend.guardrails.presidio_filter import mask_pii

logger = logging.getLogger(__name__)


def process_input(text: str) -> tuple[str, dict]:
    """
    Run full input guardrail pipeline.

    Returns sanitized text and metadata about applied filters.
    """
    meta: dict = {"pii_entities": [], "blocked": False, "block_reason": ""}

    guard = check_input(text)
    if not guard.allowed:
        meta["blocked"] = True
        meta["block_reason"] = guard.reason
        return guard.filtered_text, meta

    masked, entities = mask_pii(text)
    meta["pii_entities"] = entities
    return masked, meta


def process_output(text: str) -> tuple[str, dict]:
    """Run full output guardrail pipeline."""
    meta: dict = {"pii_entities": [], "blocked": False, "block_reason": ""}

    guard = check_output(text)
    if not guard.allowed:
        meta["blocked"] = True
        meta["block_reason"] = guard.reason
        return guard.filtered_text, meta

    masked, entities = mask_pii(text)
    meta["pii_entities"] = entities
    return masked, meta
