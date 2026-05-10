#!/usr/bin/env python3
"""
Professional Secrets Validator - Quality Assurance Tool

Tracks and validates that all 6 professional secrets are present in generated
prompts, ensuring consistent quality across all transformation categories.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

# ============================================================================
# PROFESSIONAL SECRETS KEYWORDS
# ============================================================================

PROFESSIONAL_SECRETS_KEYWORDS = {
    "cinematic_lighting": {
        "description": "Advanced lighting techniques for cinematic quality",
        "keywords": [
            "volumetric", "three-point", "global illumination", "backlighting",
            "rim lighting", "side lighting", "color-graded lighting", "golden hour",
            "cinematic lighting", "dramatic lighting", "atmospheric lighting"
        ]
    },
    "realistic_skin_textures": {
        "description": "Photorealistic skin rendering with character",
        "keywords": [
            "pores", "micro-texture", "subsurface scattering", "imperfections",
            "skin texture", "natural appearance", "realistic skin", "complexion",
            "skin tones", "texture", "natural skin"
        ]
    },
    "emotional_expression": {
        "description": "Capturing genuine emotion and storytelling",
        "keywords": [
            "authentic", "emotional", "genuine", "narrative", "storytelling",
            "connection", "chemistry", "expression", "emotion", "sentiment",
            "soulful", "sincere", "tender", "vulnerable", "affection"
        ]
    },
    "color_grading": {
        "description": "Professional color grading for mood and impact",
        "keywords": [
            "color grading", "color palette", "color harmony", "warm", "cool",
            "saturation", "contrast", "color treatment", "color tone", "hue",
            "atmospheric", "moody", "graded"
        ]
    },
    "professional_camera_language": {
        "description": "Professional camera and lens techniques",
        "keywords": [
            "focal length", "aperture", "depth of field", "perspective",
            "composition", "85mm", "135mm", "compression", "framing",
            "portrait lens", "camera", "photography", "editorial"
        ]
    },
    "storytelling_atmosphere": {
        "description": "Creating narrative and mood in imagery",
        "keywords": [
            "narrative", "atmosphere", "environmental context", "scenario",
            "mood", "story", "setting", "backdrop", "environment",
            "storytelling", "cinematic", "compelling"
        ]
    }
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
    for secret_name, result in secrets_detected.items():
        if not result.found:
            recommendations.append(
                f"Missing '{secret_name}': Consider adding keywords like "
                f"{', '.join(PROFESSIONAL_SECRETS_KEYWORDS[secret_name]['keywords'][:3])}"
            )
    
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
