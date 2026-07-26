"""Sanitize user input to prevent prompt injection attacks."""

import re
from typing import Optional


class PromptSanitizer:
    """Sanitize user prompts to prevent injection attacks."""

    # Characters and patterns that indicate potential injection attempts
    INJECTION_PATTERNS = [
        r"ignore.*instructions?",
        r"system.*prompt",
        r"you are.*now",
        r"forget.*previous",
        r"disregard.*previous",
        r"<system>",
        r"<instruction>",
        r"\[SYSTEM\]",
    ]

    # Maximum prompt length to prevent abuse
    MAX_PROMPT_LENGTH = 1000

    # Allowed character ranges (alphanumeric + safe punctuation)
    ALLOWED_PATTERN = r"^[a-zA-Z0-9\s\-.,!?'\"()&:;/—]+$"

    @staticmethod
    def sanitize(prompt: Optional[str]) -> tuple[str, list[str]]:
        """
        Sanitize a user prompt and return (cleaned_prompt, warnings).

        Args:
            prompt: Raw user input

        Returns:
            Tuple of (sanitized_prompt, list_of_warnings)
        """
        if not prompt:
            return "", []

        warnings = []
        cleaned = str(prompt).strip()

        # Check length
        if len(cleaned) > PromptSanitizer.MAX_PROMPT_LENGTH:
            warnings.append(f"Prompt truncated from {len(cleaned)} to {PromptSanitizer.MAX_PROMPT_LENGTH} chars")
            cleaned = cleaned[:PromptSanitizer.MAX_PROMPT_LENGTH]

        # Check for injection patterns (case-insensitive)
        for pattern in PromptSanitizer.INJECTION_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                warnings.append(f"Suspicious pattern detected and removed")
                # Remove the problematic part
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Remove potentially dangerous characters
        # Allow: alphanumeric, spaces, common punctuation, emoji (limited)
        if not re.match(PromptSanitizer.ALLOWED_PATTERN, cleaned):
            # Remove disallowed characters
            cleaned = re.sub(r"[^a-zA-Z0-9\s\-.,!?'\"()&:;/—\U0001F300-\U0001F9FF]", "", cleaned)
            if cleaned != prompt:
                warnings.append("Removed disallowed characters")

        # Clean up whitespace
        cleaned = " ".join(cleaned.split())

        # Ensure minimum length for useful prompts
        if len(cleaned) < 5:
            warnings.append("Prompt too short (minimum 5 characters)")

        return cleaned, warnings

    @staticmethod
    def is_safe(prompt: Optional[str]) -> bool:
        """Check if a prompt is safe to process."""
        if not prompt:
            return True

        cleaned, warnings = PromptSanitizer.sanitize(prompt)
        # Safe if no warnings and has content after sanitization
        return len(warnings) == 0 and len(cleaned) >= 5
