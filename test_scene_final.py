#!/usr/bin/env python3
"""
Final scene variation test with unique parameters to avoid cache
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import InstagramGrowthBot
import json
from datetime import datetime

def test_with_unique_context():
    """Test scene variation with unique context to bypass cache"""
    print("=" * 70)
    print("FINAL SCENE VARIATION TEST")
    print("=" * 70 + "\n")
    
    gen = InstagramGrowthBot()
    
    # Use unique context to bypass cache (includes timestamp)
    unique_context = f"transformation_test_{datetime.now().timestamp()}"
    
    # Call generate_image_prompts with unique niche
    result = gen.generate_image_prompts(
        category='women_transform',
        niche=unique_context,
        count=3,
        reference_image_text='Professional Indian woman with brown eyes, oval face, natural skin tone, subtle smile'
    )
    
    print(f"Cache status: {result.get('_from_cache', False)}")
    print(f"Has error: {'error' in result}\n")
    
    if 'prompts' in result:
        prompts = result['prompts']
        print(f"✓ Generated {len(prompts)} prompts\n")
        
        for i, p in enumerate(prompts, 1):
            scene = p.get('scene', 'Unknown')
            prompt_text = p.get('prompt', '')
            print(f"{'=' * 70}")
            print(f"PROMPT {i}: {scene}")
            print(f"{'=' * 70}")
            print(f"Length: {len(prompt_text)} words")
            print(f"\nText Preview:")
            print(prompt_text[:300] + "...\n")
        
        # Validation
        print(f"{'=' * 70}")
        print("VALIDATION")
        print(f"{'=' * 70}\n")
        
        scenes = [p.get('scene', '') for p in prompts]
        print(f"Scenes: {scenes}")
        print(f"✓ All unique: {len(scenes) == len(set(scenes))}")
        
        print(f"\n✓ Analysis:\n{result.get('analysis', 'N/A')}")
        print(f"\n✓ Tip:\n{result.get('tip', 'N/A')}")
    else:
        print(f"ERROR: {result.get('error', 'Unknown error')}")
        print(f"\nFull result: {json.dumps(result, indent=2)[:500]}")

if __name__ == '__main__':
    test_with_unique_context()
