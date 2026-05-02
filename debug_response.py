#!/usr/bin/env python3
"""
Debug script to see raw response from transformation prompt
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import InstagramGrowthBot
import json

def test_raw_response():
    """Show raw response from transformation prompts"""
    print("=" * 70)
    print("RAW RESPONSE DEBUG - Transformation Prompts")
    print("=" * 70 + "\n")
    
    gen = InstagramGrowthBot()
    
    # Get the prompt that will be sent to Groq
    category = 'women_transform'
    niche_safe = ""
    user_context_safe = ""
    reference_line = "\n\nREFERENCE IMAGE PROVIDED: Professional Indian woman with brown eyes, oval face\nUse this description to anchor facial identity preservation across all variants."
    
    # Build the full prompt from the method
    count = 3
    category_desc = "female portrait transformation (strict facial feature preservation required)"
    
    transformation_directive = ""
    artistic_style_emphasis = ""
    niche_line = ""
    context_line = ""
    
    prompt = f"""You are an expert AI image generation prompt engineer for identity-locked portrait transformations.

Category: {category_desc}{niche_line}{context_line}{reference_line}{transformation_directive}{artistic_style_emphasis}

ABSOLUTE PRIORITY: IDENTITY LOCK (NO EXCEPTIONS)
- IDENTITY MUST BE PIXEL-PERFECT IDENTICAL TO REFERENCE IMAGE
- Face direction/angle/pose/expression: CAN CHANGE per scene
- Everything else about the face: CANNOT CHANGE (not even 1% alteration)

FACIAL FEATURE PRESERVATION (DO NOT ALTER EVEN SLIGHTLY):
✓ PRESERVE EXACTLY: Eye shape, size, spacing, iris color, pupil shape | Nose structure, tip, nostrils, width | Mouth shape, lip fullness, corners | Cheekbone height and prominence | Jawline shape and definition | Face shape (oval/round/square) | Skin tone (exact match, no warming/cooling) | Skin texture (pores, natural blemishes, texture patterns) | Forehead width and height | Chin structure and projection | Face proportions (distance between features) | Unique facial characteristics, birthmarks, asymmetries | Eyebrow shape, thickness, arch, spacing | Hairline position and shape

SCENE VARIATION MANDATE (CRITICAL FOR DIVERSITY):
⚠️ YOU MUST CREATE {count} PROMPTS WITH COMPLETELY DIFFERENT SCENARIOS
- Each prompt MUST use a different transformation scenario from the list below
- Scenario rotation example (for 3 prompts): Prompt 1=Bride, Prompt 2=Professional, Prompt 3=Casual
- If fewer scenarios needed, cycle through: Bride → Professional → Casual → Party → Cultural → Artistic → Outdoor → Minimalist
- ENFORCE DIVERSITY: Each scenario must have distinct pose, body position, environment, and styling
- VALIDATE BEFORE OUTPUT: Confirm each prompt is visually distinct (different scene context)

SPECIAL SCENE ROTATION RULE (if {count}=3):
- Prompt 1: Use Bride/Formal Wedding scenario
- Prompt 2: Use Professional/Corporate scenario  
- Prompt 3: Use Casual/Relaxed scenario

INSTRUCTIONS FOR PROMPT GENERATION:
- Create {count} DISTINCT transformation prompts (each 100-160 words, compressed/dense)
- ENFORCE THE SCENE ROTATION (mandatory scenario assignment per prompt above)
- EACH PROMPT MUST START with explicit facial feature preservation statement
- EACH PROMPT MUST SPECIFY THE SCENE SCENARIO being used
- EACH PROMPT MUST SPECIFY different pose, body position, and face angle than other prompts
- EACH PROMPT MUST SPECIFY different environmental context than other prompts
- EACH PROMPT MUST END with explicit "Negative: [forbidden list]"

Return ONLY valid JSON (no markdown, no text before/after, NO EXPLANATIONS):
{{
  "prompts": [
    {{"prompt": "<100-160 word prompt with identity lock>", "scene": "<transformation type>"}}
  ],
  "analysis": "Brief analysis of approach",
  "tip": "Brief tip"
}}"""

    # Make the Groq call
    cache_key = gen._make_cache_key("generate_image_prompts", category=category)
    result = gen._call_groq_with_fallback(
        command="generate_image_prompts",
        cache_key=cache_key,
        prompt=prompt,
        chat_id=None,
        temperature=0.7,
        max_tokens=2000
    )
    
    print("RAW RESPONSE:")
    print("=" * 70)
    if "response" in result:
        print(result["response"][:1500])
        print("\n... (truncated)")
    else:
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    test_raw_response()
