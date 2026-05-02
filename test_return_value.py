#!/usr/bin/env python3
"""
Debug test to see what generate_image_prompts returns
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import InstagramGrowthBot
import json

def test_return_value():
    """Show what generate_image_prompts returns"""
    print("=" * 70)
    print("Testing generate_image_prompts return value")
    print("=" * 70 + "\n")
    
    gen = InstagramGrowthBot()
    
    # Call generate_image_prompts
    result = gen.generate_image_prompts(
        category='women_transform',
        count=3,
        reference_image_text='Professional Indian woman with brown eyes, oval face, natural skin tone'
    )
    
    print("Full return value:")
    print(json.dumps(result, indent=2)[:2000])
    print("\n...")
    print(f"\nPrompts count: {len(result.get('prompts', []))}")
    print(f"Keys in result: {list(result.keys())}")
    
if __name__ == '__main__':
    test_return_value()
