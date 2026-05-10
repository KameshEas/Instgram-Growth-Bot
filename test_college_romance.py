#!/usr/bin/env python3
"""
Test: Custom Couple Scenario - "A Hidden College Romance"

This demonstrates how the professional structure transforms a simple
requirement into a complete optimized prompt with all 12 components
and 6 professional secrets embedded.
"""

from src.prompts.professional_structure import (
    build_professional_prompt,
    get_category_info,
    build_simple_prompt,
    PROFESSIONAL_SECRETS,
)

print("\n" + "="*80)
print("🎓 CUSTOM COUPLE SCENARIO - HIDDEN COLLEGE ROMANCE")
print("="*80)

# Get category info
print("\n📋 CATEGORY INFO - couples_transform:")
category_info = get_category_info("couples_transform")
print(f"   Components: {len(category_info['components'])} (must be 12)")
print(f"   Components: {category_info['components']}")

# Generate default prompt
print("\n" + "-"*80)
print("DEFAULT PROMPT (Using all first options):")
print("-"*80)
default_prompt = build_simple_prompt("couples_transform")
print(f"\n{default_prompt}\n")
print(f"Length: {len(default_prompt)} characters")

# Generate custom prompt for college romance
print("\n" + "-"*80)
print("CUSTOM PROMPT - 'A Hidden College Romance'")
print("-"*80)

# Create custom components for college romance theme
custom_components = {
    "subject": "Using reference images, transform the couple into a hidden college romance moment",
    "face_details": "both with natural skin texture and appearance showing youthful warmth",
    "hair": "hair styled naturally as in reference images with that college-day freshness",
    "expression": "with natural genuine expressions showing secret connection and college crush moment, tender shy smiles revealing their hidden romance",
    "clothing": "wearing casual college-appropriate outfits with authentic casual styling",
    "pose": "positioned naturally together in a secluded college campus spot showing intimate connection without drawing attention",
    "environment": "in a beautiful hidden romance scenario with soft campus ambiance and intimate atmosphere",
    "lighting": "with warm intimate lighting suggesting evening campus setting, golden hour campus light creating romantic mood",
    "mood": "capturing authentic hidden romance moment showing genuine connection and college chemistry",
    "camera_style": "professional couple portrait composition with 85mm focal length creating romantic compression",
    "color_palette": "with warm intimate color grading and natural tones reflecting college nostalgia",
    "quality_keywords": "high definition, sharp detail, authentic couple photography, masterpiece quality",
}

custom_prompt = build_professional_prompt(
    category="couples_transform",
    components=custom_components,
    include_quality=True
)

print(f"\n{custom_prompt}\n")
print(f"Length: {len(custom_prompt)} characters")

# Analyze professional secrets
print("\n" + "-"*80)
print("✅ PROFESSIONAL SECRETS ANALYSIS")
print("-"*80)

secrets_found = {
    "Cinematic Lighting": "golden hour campus light creating romantic mood" in custom_prompt,
    "Realistic Skin Textures": "natural skin texture and appearance" in custom_prompt,
    "Emotional Expression": "secret connection and college crush" in custom_prompt,
    "Color Grading": "warm intimate color grading" in custom_prompt,
    "Professional Camera Language": "85mm focal length creating romantic compression" in custom_prompt,
    "Storytelling Atmosphere": "hidden romance scenario with soft campus ambiance" in custom_prompt,
}

for secret, present in secrets_found.items():
    status = "✓" if present else "✗"
    print(f"  {status} {secret}")

all_present = all(secrets_found.values())
print(f"\n  Overall: {'✅ All 6 secrets present' if all_present else '❌ Missing some secrets'}")

# Show component breakdown
print("\n" + "-"*80)
print("📊 12-COMPONENT BREAKDOWN")
print("-"*80)

components_list = [
    "Subject", "Face Details", "Hair", "Expression",
    "Clothing", "Pose", "Environment", "Lighting",
    "Mood", "Camera Style", "Color Palette", "Quality Keywords"
]

for i, comp in enumerate(components_list, 1):
    print(f"  {i:2d}. {comp}")

print(f"\n  ✅ Total: {len(components_list)}/12 components")

# Scenario analysis
print("\n" + "-"*80)
print("🎯 SCENARIO ANALYSIS")
print("-"*80)

scenario_elements = {
    "Relationship Type": "College sweethearts with hidden romance",
    "Setting": "Secluded college campus spot",
    "Time of Day": "Evening/golden hour",
    "Emotional Tone": "Tender, shy, intimate, genuine",
    "Connection Level": "Secret/hidden from others",
    "Physical Proximity": "Close, intimate, showing connection",
    "Clothing Appropriateness": "Casual college-appropriate",
    "Lighting Type": "Warm, golden hour campus light",
    "Camera Approach": "85mm focal length (romantic compression)",
    "Color Grade": "Warm intimate tones with nostalgia",
}

for element, description in scenario_elements.items():
    print(f"  • {element}: {description}")

# Comparison with default
print("\n" + "-"*80)
print("📈 CUSTOMIZATION IMPACT")
print("-"*80)

print(f"\n  Default prompt length: {len(default_prompt)} chars")
print(f"  Custom prompt length: {len(custom_prompt)} chars")
print(f"  Difference: +{len(custom_prompt) - len(default_prompt)} chars (+{round(((len(custom_prompt) - len(default_prompt)) / len(default_prompt)) * 100, 1)}%)")

print("\n  Benefits of customization:")
print("  ✓ Specific college setting (vs generic)")
print("  ✓ Hidden romance emotion (vs generic couple)")
print("  ✓ Campus ambiance (vs generic environment)")
print("  ✓ Evening lighting specification (vs generic warm)")
print("  ✓ Youthful appearance emphasis (vs generic natural)")
print("  ✓ Casual college attire (vs generic outfit)")

# Usage instructions
print("\n" + "="*80)
print("📌 HOW TO USE THIS PROMPT")
print("="*80)

print("""
Option 1 - Mobile App:
  1. Open Generate screen
  2. Select 'couples_transform' category
  3. Enable Advanced Mode
  4. Paste this custom prompt in context field:
     "A hidden college romance between two students on campus at evening"
  5. Add reference image of couple
  6. Generate

Option 2 - Telegram Bot:
  1. Send reference image of couple
  2. Send: /generate couples_transform "A hidden college romance"
  3. Bot generates optimized prompt

Option 3 - Direct API:
  1. POST to /api/generate_image_prompts
  2. Include: category="couples_transform"
  3. Include: custom_prompt="A hidden college romance"
  4. Include: reference_image_url (URL or file)
  5. Receive 3 variations optimized for your scenario

Expected Output:
  - 3 prompt variations (all with college romance theme)
  - Each 550-600 characters
  - All 12 components covered
  - All 6 professional secrets embedded
  - Better AI generation due to specific scenario
""")

print("="*80 + "\n")
