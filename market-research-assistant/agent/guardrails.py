"""
Guardrails module — Ethics, bias reduction, privacy, and safety filters
for the Intelligent Market Research Assistant.
"""

import re
import logging

logger = logging.getLogger(__name__)

# ─── Blocked Content Patterns ─────────────────────────────────────────────────
BLOCKED_INPUT_PATTERNS = [
    r"\b(personal.{0,10}data|SSN|social security|passport number|credit card)\b",
    r"\b(hack|exploit|illegal|fraud|scam|manipulate market)\b",
    r"\b(defame|slander|destroy competitor|ruin)\b",
]

BLOCKED_INDUSTRIES = [
    "weapons", "illegal drugs", "human trafficking", "adult content",
    "gambling", "tobacco targeting minors"
]

# ─── PII Detection Patterns ───────────────────────────────────────────────────
PII_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # email
    r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",                      # phone
    r"\b\d{3}-\d{2}-\d{4}\b",                                   # SSN
]

# ─── Required Input Fields ────────────────────────────────────────────────────
REQUIRED_FIELDS = ["industry", "product", "target_audience", "location"]

MAX_INPUT_LENGTH = 500  # characters per field
MAX_COMPETITORS_LENGTH = 300


class GuardrailViolation(Exception):
    """Raised when a guardrail check fails."""
    pass


def validate_inputs(data: dict) -> dict:
    """
    Validate and sanitize user inputs.
    Returns cleaned data or raises GuardrailViolation.
    """
    cleaned = {}

    # Check required fields
    for field in REQUIRED_FIELDS:
        if not data.get(field, "").strip():
            raise GuardrailViolation(f"Required field missing: '{field}'. Please provide all required information.")

    # Sanitize and validate each field
    for field in ["industry", "product", "target_audience", "location", "competitors"]:
        value = str(data.get(field, "")).strip()

        # Length check
        max_len = MAX_COMPETITORS_LENGTH if field == "competitors" else MAX_INPUT_LENGTH
        if len(value) > max_len:
            raise GuardrailViolation(f"Input too long for field '{field}'. Please keep it under {max_len} characters.")

        # PII detection
        for pattern in PII_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"PII detected in field '{field}' — redacted")
                value = re.sub(pattern, "[REDACTED]", value, flags=re.IGNORECASE)

        # Blocked pattern check
        for pattern in BLOCKED_INPUT_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                raise GuardrailViolation(
                    "Your request contains content that cannot be processed. "
                    "Please ensure your market research request is for a legitimate business purpose."
                )

        # Blocked industry check
        for blocked in BLOCKED_INDUSTRIES:
            if blocked.lower() in value.lower():
                raise GuardrailViolation(
                    f"Market research for this industry type is not supported. "
                    "Please specify a legitimate commercial industry."
                )

        # Basic HTML/script injection prevention
        value = re.sub(r"<[^>]*>", "", value)
        value = re.sub(r"[;&|`$]", "", value)

        cleaned[field] = value

    logger.info("Input validation passed for all fields")
    return cleaned


def validate_question(question: str) -> str:
    """Validate and sanitize a Q&A query."""
    if not question or not question.strip():
        raise GuardrailViolation("Question cannot be empty.")

    if len(question) > 1000:
        raise GuardrailViolation("Question is too long. Please keep it under 1000 characters.")

    # PII removal
    for pattern in PII_PATTERNS:
        question = re.sub(pattern, "[REDACTED]", question, flags=re.IGNORECASE)

    # Blocked patterns
    for pattern in BLOCKED_INPUT_PATTERNS:
        if re.search(pattern, question, re.IGNORECASE):
            raise GuardrailViolation(
                "Your question contains content that cannot be processed. "
                "Please ask a legitimate market research question."
            )

    # Sanitize
    question = re.sub(r"<[^>]*>", "", question)
    return question.strip()


def validate_output(output: str) -> dict:
    """
    Post-process LLM output for safety and quality.
    Returns dict with 'text' and 'warnings'.
    """
    warnings = []

    if not output or len(output.strip()) < 50:
        return {
            "text": "The analysis could not be completed. Please try again.",
            "warnings": ["Insufficient output generated"],
            "passed": False
        }

    # Check for potential hallucinated statistics (very specific numbers without context)
    stat_pattern = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:billion|trillion|million)\b"
    stats_found = re.findall(stat_pattern, output, re.IGNORECASE)
    if len(stats_found) > 8:
        warnings.append("Note: Specific statistics are estimates. Verify with primary sources.")

    # Remove any PII that might have slipped through
    for pattern in PII_PATTERNS:
        output = re.sub(pattern, "[REDACTED]", output, flags=re.IGNORECASE)

    # Add confidence disclaimer if not present
    disclaimer_needed = len(stats_found) > 0
    if disclaimer_needed and "confidence" not in output.lower() and "estimate" not in output.lower():
        output += "\n\n*Data confidence note: Market statistics are estimates based on general knowledge. For investment decisions, validate with primary market research sources.*"

    return {
        "text": output.strip(),
        "warnings": warnings,
        "passed": True
    }


def ethics_summary() -> dict:
    """Return the ethics framework applied to each request."""
    return {
        "data_privacy": "No user data stored beyond current session",
        "bias_reduction": "Multi-perspective prompts applied; diverse audience consideration included",
        "transparency": "Agent reasoning steps available on request",
        "content_safety": "Input and output guardrails active",
        "fairness": "Balanced competitor analysis enforced",
        "ham_tone": "Helpful, Authoritative, Measured tone applied via system prompt"
    }
