#!/usr/bin/env python3
"""
Test script to verify scene variation implementation for transformation prompts
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import InstagramGrowthBot
import json

def test_scene_variation():
    """Test that transformation prompts generate distinct scenes"""
    print("=" * 70)
    print("SCENE VARIATION TEST - Transformation Prompts")
    print("=" * 70 + "\n")
    
    gen = InstagramGrowthBot()
    
    # Test with women_transform category
    result = gen.generate_image_prompts(
        category='women_transform',
        count=3,
        reference_image_text='Professional Indian woman with brown eyes, oval face, natural skin tone, subtle features, approachable expression'
    )
    
    prompts = result.get('prompts', [])
    print(f"✓ Generated {len(prompts)} prompts\n")
    
    # Analyze each prompt
    for i, p in enumerate(prompts, 1):
        scene = p.get('scene', 'Unknown')
        prompt_text = p.get('prompt', '')
        
        print(f"{'='*70}")
        print(f"PROMPT {i}: {scene}")
        print(f"{'='*70}")
        print(f"Length: {len(prompt_text)} words")
        print(f"\nText Preview (first 400 chars):")
        print(prompt_text[:400])
        print("\n")
    
    # Validation
    print(f"{'='*70}")
    print("VALIDATION CHECKS")
    print(f"{'='*70}")
    
    scenes = [p.get('scene', '') for p in prompts]
    print(f"\n✓ Scenes generated: {scenes}")
    print(f"✓ All unique: {len(scenes) == len(set(scenes))}")
    
    # Check for diversity keywords
    diversity_keywords = {
        'bride': ['bride', 'wedding', 'bridal'],
        'professional': ['professional', 'corporate', 'business', 'office'],
        'casual': ['casual', 'relaxed', 'cafe', 'natural']
    }
    
    print(f"\n✓ Diversity Check:")
    for i, p in enumerate(prompts, 1):
        prompt_text = p.get('prompt', '').lower()
        for scene_type, keywords in diversity_keywords.items():
            if any(kw in prompt_text for kw in keywords):
                print(f"  Prompt {i}: Contains '{scene_type}' keywords ✓")
                break
    
    # Analysis
    print(f"\n{'='*70}")
    print("ANALYSIS")
    print(f"{'='*70}")
    print(result.get('analysis', 'N/A'))
    
    print(f"\n{'='*70}")
    print("TIP")
    print(f"{'='*70}")
    print(result.get('tip', 'N/A'))

if __name__ == '__main__':
    test_scene_variation()
