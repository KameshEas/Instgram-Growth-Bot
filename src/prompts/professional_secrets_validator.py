#!/usr/bin/env python3
"""
Professional Secrets Validator - Quality Assurance Tool

Tracks and validates that all 6 professional secrets are present in generated
prompts, ensuring consistent quality across all transformation categories.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from src.prompts.professional_structure import PROFESSIONAL_SECRETS_KEYWORDS  # M3 FIX: Import from single source of truth

# ============================================================================
# PROFESSIONAL SECRETS KEYWORDS
# ============================================================================
# M3 FIX: Imported from professional_structure.py to ensure consistency
# and eliminate keyword overlap issues across the codebase


# ============================================================================
# COMPONENT GUIDANCE (M7 FIX: All 12 Components)
# ============================================================================
# M7 FIX: Specific guidance for all 12 components when they're missing or weak
COMPONENT_GUIDANCE = {
    "subject": "Describe who is in the image (person, character, or group). Use: woman, man, couple, professional, model",
    "face_details": "Add facial characteristics and texture details. Use: skin texture, facial features, cheekbones, complexity, realistic appearance",
    "hair": "Describe hair styling, color, and texture. Use: hairstyle, hair color, hair texture, braided, flowing, styled",
    "expression": "Specify emotional expression and facial emotion. Use: smile, genuine expression, emotion, eye contact, authentic emotion",
    "clothing": "Describe what the subject is wearing. Use: outfit, dress, clothing, jacket, blazer, attire, wardrobe, styled",
    "pose": "Describe body positioning and posture. Use: pose, standing, seated, posture, positioned, gesture, stance",
    "environment": "Add background setting and context. Use: background, environment, setting, location, backdrop, scenery, landscape",
    "lighting": "Specify lighting techniques and quality. Use: three-point lighting, soft light, dramatic lighting, golden hour, cinematic",
    "mood": "Convey the overall atmosphere and feeling. Use: mood, atmosphere, energy, peaceful, vibrant, dramatic, intimate, joyful",
    "camera_style": "Add camera technique and composition. Use: 85mm, aperture, depth of field, composition, framing, perspective",
    "color_palette": "Define color grading and tone. Use: color grading, warm tones, cool tones, saturation, color treatment, graded",
    "quality_keywords": "Specify resolution and quality level. Use: 8k, high definition, masterpiece, sharp, detailed, professional"
}


@dataclass
class SecretDetectionResult:
    """Result of secret detection in a prompt."""
    secret: str
    found: bool
    keywords_matched: List[str]
    confidence: float  # 0.0 to 1.0


@dataclass
class PromptQualityReport:
    """Quality report for a generated prompt."""
    category: str
    prompt: str
    total_length: int
    secrets_detected: Dict[str, SecretDetectionResult]
    all_secrets_present: bool
    completeness_score: float  # 0.0 to 100.0
    recommendations: List[str]


# ============================================================================
# DETECTION FUNCTIONS
# ============================================================================

def detect_secret_in_prompt(
    prompt: str,
    secret_name: str,
    keywords: List[str]
) -> SecretDetectionResult:
    """
    Detect if a professional secret is present in a prompt.
    
    Args:
        prompt: The generated prompt text
        secret_name: Name of the secret (e.g., 'cinematic_lighting')
        keywords: Keywords to search for
        
    Returns:
        SecretDetectionResult with detected keywords and confidence
    """
    prompt_lower = prompt.lower()
    matched_keywords = [kw for kw in keywords if kw.lower() in prompt_lower]
    
    # Calculate confidence based on keyword density
    # C5: Fix confidence math - maintain 0.0-1.0 scale without incorrect 1.5x multiplier
    if not matched_keywords:
        confidence = 0.0
    else:
        keyword_density = len(matched_keywords) / len(keywords)
        confidence = keyword_density  # Keep 0.0-1.0 range, remove incorrect 1.5x multiplier
    
    return SecretDetectionResult(
        secret=secret_name,
        found=len(matched_keywords) > 0,
        keywords_matched=matched_keywords,
        confidence=confidence
    )


def check_component_presence(
    prompt: str,
    component: str
) -> Tuple[bool, str]:
    """
    M7 FIX: Check if a component is present in the prompt and provide guidance.
    
    Args:
        prompt: The generated prompt
        component: Component name to check (e.g., 'face_details')
        
    Returns:
        Tuple of (is_present, guidance) where guidance is specific to the component
    """
    prompt_lower = prompt.lower()
    
    # Component-specific signal keywords to detect presence
    component_signals = {
        "subject": ["person", "woman", "man", "couple", "professional", "model", "character"],
        "face_details": ["face", "skin", "complexion", "cheekbone", "facial", "texture"],
        "hair": ["hair", "hairstyle", "braid", "curl", "wave", "strand", "styled"],
        "expression": ["smile", "expression", "emotion", "gaze", "authentic", "genuine"],
        "clothing": ["dress", "outfit", "clothes", "jacket", "shirt", "attire", "wardrobe"],
        "pose": ["pose", "posing", "standing", "seated", "positioned", "stance"],
        "environment": ["background", "setting", "environment", "location", "backdrop", "scene"],
        "lighting": ["lighting", "light", "illumination", "shadow", "dramatic", "golden"],
        "mood": ["mood", "atmosphere", "energy", "peaceful", "vibrant", "intimate"],
        "camera_style": ["camera", "lens", "aperture", "composition", "framing", "perspective"],
        "color_palette": ["color", "grading", "tone", "saturation", "warm", "cool"],
        "quality_keywords": ["8k", "4k", "high", "detailed", "masterpiece", "sharp"]
    }
    
    signals = component_signals.get(component, [])
    is_present = any(signal in prompt_lower for signal in signals)
    guidance = COMPONENT_GUIDANCE.get(component, f"Enhance the {component} component")
    
    return is_present, guidance


def validate_prompt_quality(
    prompt: str,
    category: str
) -> PromptQualityReport:
    """
    Comprehensive quality validation for a generated prompt.
    
    Args:
        prompt: The generated prompt
        category: Category of the prompt (e.g., 'couples_transform')
        
    Returns:
        PromptQualityReport with detailed analysis
    """
    # Detect all professional secrets
    secrets_detected = {}
    for secret_name, secret_data in PROFESSIONAL_SECRETS_KEYWORDS.items():
        result = detect_secret_in_prompt(
            prompt=prompt,
            secret_name=secret_name,
            keywords=secret_data["keywords"]
        )
        secrets_detected[secret_name] = result
    
    # Calculate metrics
    all_secrets_present = all(result.found for result in secrets_detected.values())
    secrets_found_count = sum(1 for result in secrets_detected.values() if result.found)
    completeness_score = (secrets_found_count / len(PROFESSIONAL_SECRETS_KEYWORDS)) * 100
    
    # Generate recommendations
    recommendations = []
    
    # M7 FIX: Add secret recommendations (existing)
    for secret_name, result in secrets_detected.items():
        if not result.found:
            recommendations.append(
                f"Missing '{secret_name}': Consider adding keywords like "
                f"{', '.join(PROFESSIONAL_SECRETS_KEYWORDS[secret_name]['keywords'][:3])}"
            )
    
    # M7 FIX: Add component recommendations for all 12 components
    all_components = [
        "subject", "face_details", "hair", "expression", "clothing", "pose",
        "environment", "lighting", "mood", "camera_style", "color_palette", "quality_keywords"
    ]
    
    for component in all_components:
        is_present, guidance = check_component_presence(prompt, component)
        if not is_present:
            recommendations.append(f"{component}: {guidance}")
    
    return PromptQualityReport(
        category=category,
        prompt=prompt,
        total_length=len(prompt),
        secrets_detected=secrets_detected,
        all_secrets_present=all_secrets_present,
        completeness_score=completeness_score,
        recommendations=recommendations
    )


def generate_quality_report(report: PromptQualityReport) -> str:
    """
    Generate a formatted quality report string.
    
    Args:
        report: PromptQualityReport to format
        
    Returns:
        Formatted report string
    """
    lines = [
        "\n" + "="*80,
        f"📊 PROFESSIONAL SECRETS QUALITY REPORT",
        "="*80,
        f"\nCategory: {report.category}",
        f"Prompt Length: {report.total_length} characters",
        f"\n{'SECRET NAME':<35} {'STATUS':<10} {'KEYWORDS':<20}",
        "-"*80,
    ]
    
    for secret_name, result in report.secrets_detected.items():
        status = "✅ FOUND" if result.found else "❌ MISSING"
        keywords_str = f"({len(result.keywords_matched)})" if result.keywords_matched else "(0)"
        lines.append(f"{secret_name:<35} {status:<10} {keywords_str:<20}")
        if result.keywords_matched:
            lines.append(f"  Keywords: {', '.join(result.keywords_matched[:3])}")
    
    lines.extend([
        "\n" + "-"*80,
        f"Overall Completeness Score: {report.completeness_score:.1f}%",
        f"All Secrets Present: {'✅ YES' if report.all_secrets_present else '❌ NO'}",
    ])
    
    if report.recommendations:
        lines.extend([
            "\n📋 Recommendations:",
        ])
        for rec in report.recommendations:
            lines.append(f"  • {rec}")
    
    lines.append("=" * 80 + "\n")
    
    return "\n".join(lines)


# ============================================================================
# BATCH VALIDATION
# ============================================================================

def validate_category_prompts(
    category: str,
    prompts: List[str]
) -> Tuple[List[PromptQualityReport], Dict[str, any]]:
    """
    Validate multiple prompts for a category.
    
    Args:
        category: Category name
        prompts: List of prompts to validate
        
    Returns:
        Tuple of (list of reports, summary statistics)
    """
    reports = [validate_prompt_quality(prompt, category) for prompt in prompts]
    
    # Calculate summary statistics
    avg_completeness = sum(r.completeness_score for r in reports) / len(reports)
    all_have_secrets = all(r.all_secrets_present for r in reports)
    avg_length = sum(r.total_length for r in reports) / len(reports)
    
    summary = {
        "category": category,
        "prompt_count": len(reports),
        "average_completeness": avg_completeness,
        "all_complete": all_have_secrets,
        "average_length": avg_length,
    }
    
    return reports, summary


if __name__ == "__main__":
    # Example usage
    print("\n" + "="*80)
    print("Professional Secrets Validator - Module Test")
    print("="*80)
    
    # Test prompt
    test_prompt = """
    Using reference images, transform the couple into a romantic intimate moment,
    both with natural skin texture and appearance, hair matching reference with
    natural styling, genuine expressions showing deep connection, wearing elegant
    scenario-appropriate outfits, positioned naturally showing couple intimacy,
    in a beautiful romantic scenario, with warm intimate lighting and golden hour
    glow, cinematic atmospheric lighting flattering both, capturing authentic
    couple emotion and connection, professional couple portrait composition with
    85mm focal length creating romantic compression, warm intimate color grading
    and natural tones reflecting emotional storytelling atmosphere, high definition,
    masterpiece couple photography, award-winning quality, cinematic excellence
    capturing their love story.
    """
    
    # Validate
    report = validate_prompt_quality(test_prompt, "couples_transform")
    print(generate_quality_report(report))
    
    print("✅ Validator module loaded successfully")
    print("   Use: from professional_secrets_validator import validate_prompt_quality")
