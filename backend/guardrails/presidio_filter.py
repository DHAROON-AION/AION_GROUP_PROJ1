"""PII detection and masking via Microsoft Presidio."""

import logging
import re
from functools import lru_cache

logger = logging.getLogger(__name__)

_PRESIDIO_AVAILABLE = False

try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine

    _PRESIDIO_AVAILABLE = True
except ImportError:
    logger.info("Presidio not installed; using regex fallback for PII masking")


@lru_cache
def _get_analyzer():
    return AnalyzerEngine()


@lru_cache
def _get_anonymizer():
    return AnonymizerEngine()


# Fallback patterns for common PII when Presidio models are unavailable
_FALLBACK_PATTERNS = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN_REDACTED]"),
    (re.compile(r"\b\d{16}\b"), "[CARD_REDACTED]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[EMAIL_REDACTED]"),
    (re.compile(r"\b\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b"), "[PHONE_REDACTED]"),
    (re.compile(r"\b\d{10,12}\b"), "[ID_REDACTED]"),
]


def mask_pii(text: str) -> tuple[str, list[str]]:
    """
    Detect and mask PII in text.

    Returns masked text and list of detected entity types.
    """
    if not text:
        return text, []

    if _PRESIDIO_AVAILABLE:
        try:
            analyzer = _get_analyzer()
            anonymizer = _get_anonymizer()
            results = analyzer.analyze(text=text, language="en")
            if not results:
                return text, []
            anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
            entities = list({r.entity_type for r in results})
            return anonymized.text, entities
        except Exception as exc:
            logger.warning("Presidio masking failed, using fallback: %s", exc)

    masked = text
    entities: list[str] = []
    for pattern, replacement in _FALLBACK_PATTERNS:
        if pattern.search(masked):
            entities.append(replacement.strip("[]"))
            masked = pattern.sub(replacement, masked)
    return masked, entities
