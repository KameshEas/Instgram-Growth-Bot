"""Validator for generated variations (agentic report B2: evaluator-optimizer, one bounded retry).

Checks the rules the generator prompt (P01/P02) states, deterministically, and returns human-readable
problems that are fed back to the model for a single retry. No LLM calls here.
"""

import os
import re
from typing import Iterable, List, Optional

ASPECT_RATIOS = {"1:1", "4:5", "9:16", "16:9", "3:2", "2:3"}
TEXT_TYPES = {"reel_script", "caption", "email_subject"}
TRANSFORM_CATEGORIES = {"women_transform", "men_transform", "couples_transform"}

_QUOTED = re.compile(r'"([^"]{3,120})"|“([^”]{3,120})”')
_HEX = re.compile(r"#[0-9a-fA-F]{6}\b")


def validation_enabled() -> bool:
    return os.getenv("GENERATION_VALIDATE", "0").strip().lower() in ("1", "true", "yes", "on")


def required_literals(*sources: Optional[str]) -> List[str]:
    """Quoted phrases and hex colours the creator gave, which must appear verbatim."""
    found: List[str] = []
    for text in sources:
        if not text:
            continue
        for match in _QUOTED.finditer(text):
            phrase = (match.group(1) or match.group(2)).strip()
            if phrase and phrase not in found:
                found.append(phrase)
        for hex_code in _HEX.findall(text):
            if hex_code.upper() not in (f.upper() for f in found):
                found.append(hex_code)
    return found


def validate_variations(variations, requested_count: int, category: str, is_text_content: bool,
                        literals: Iterable[str] = ()) -> List[str]:
    """Return a list of problems ([] means valid)."""
    problems: List[str] = []
    if not isinstance(variations, list) or not variations:
        return ["The response must contain a non-empty \"variations\" list."]
    if requested_count and len(variations) != requested_count:
        problems.append(f"Return exactly {requested_count} variations (you returned {len(variations)}).")

    literals = list(literals)
    for idx, var in enumerate(variations, 1):
        label = f"Variation {idx}"
        if not isinstance(var, dict):
            problems.append(f"{label} must be a JSON object.")
            continue
        if is_text_content:
            for field in ("title", "type", "content", "hook", "cta", "tone"):
                if not str(var.get(field) or "").strip():
                    problems.append(f"{label} is missing \"{field}\".")
            if var.get("type") and var["type"] not in TEXT_TYPES:
                problems.append(f"{label}: \"type\" must be one of {sorted(TEXT_TYPES)}.")
            if category == "email_subjects" and len(str(var.get("content") or "")) > 60:
                problems.append(f"{label}: the subject line must be 50 characters or fewer.")
            body = str(var.get("content") or "")
        else:
            for field in ("title", "style", "prompt", "negative_prompt", "aspect_ratio"):
                if not str(var.get(field) or "").strip():
                    problems.append(f"{label} is missing \"{field}\".")
            if var.get("aspect_ratio") and str(var["aspect_ratio"]).strip() not in ASPECT_RATIOS:
                problems.append(f"{label}: aspect_ratio must be one of {sorted(ASPECT_RATIOS)}.")
            if not isinstance(var.get("keywords"), list) or not var.get("keywords"):
                problems.append(f"{label}: \"keywords\" must be a non-empty list of strings.")
            body = str(var.get("prompt") or "")
            words = len(body.split())
            if body and words < 25:
                problems.append(f"{label}: the prompt is too short ({words} words); aim for 60 to 120 words.")
            if category in TRANSFORM_CATEGORIES and body and "reference" not in body.lower():
                problems.append(f"{label}: transformation prompts must start with \"Using the reference photo,\" "
                                f"and keep the person's face and proportions identical.")
        lower = body.lower()
        for literal in literals:
            if literal.lower() not in lower:
                problems.append(f"{label} must include \"{literal}\" exactly as the creator wrote it.")
    return problems


def feedback_message(problems: List[str]) -> str:
    """Text appended to the request for the single retry."""
    listed = "\n".join(f"- {p}" for p in problems[:12])
    return ("\n\nYour previous answer did not meet these requirements. Fix every item and return the "
            f"complete JSON object again:\n{listed}")
