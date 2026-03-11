# ============================================================
# utils/validator.py
# Input validation before the pipeline starts.
# Rejects empty, too-short, or nonsense topics early.
# ============================================================

import re
from utils.logger import get_logger

log = get_logger(__name__)

MIN_WORDS   = 2
MAX_CHARS   = 300


class InvalidTopicError(ValueError):
    """Raised when the research topic fails validation."""
    pass


def validate_topic(topic: str) -> str:
    """
    Cleans and validates a research topic.

    Returns the cleaned topic string.
    Raises InvalidTopicError with a human-readable message if invalid.
    """
    if not topic or not topic.strip():
        raise InvalidTopicError("Topic cannot be empty.")

    cleaned = topic.strip()

    # Too long
    if len(cleaned) > MAX_CHARS:
        raise InvalidTopicError(
            f"Topic is too long ({len(cleaned)} chars). Max {MAX_CHARS}."
        )

    # Too short / not enough words
    word_count = len(cleaned.split())
    if word_count < MIN_WORDS:
        raise InvalidTopicError(
            f"Topic must be at least {MIN_WORDS} words. Got: '{cleaned}'"
        )

    # Only special characters / numbers
    if not re.search(r"[a-zA-Z]", cleaned):
        raise InvalidTopicError("Topic must contain actual words.")

    log.info(f"Topic validated: '{cleaned}'")
    return cleaned