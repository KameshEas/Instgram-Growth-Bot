#!/usr/bin/env python
"""Test script to verify prompt generation differs on each call"""
import sys
sys.path.insert(0, '.')
from src.main import InstagramGrowthBot

bot = InstagramGrowthBot()

print('=' * 80)
print('TEST: Verify fresh prompts (no caching for custom input)')
print('=' * 80)

# Test 1: Generate custom prompts
print('\n--- GENERATION 1 ---')
result1 = bot.image_generation_prompts(
    category='couples_transform',
    custom_prompt='Couples romantic intimacy in kitchen',
    chat_id=123
)

if result1 and 'prompts' in result1:
    print('[OK] Got {} prompts'.format(len(result1['prompts'])))
    for i, p in enumerate(result1['prompts'], 1):
        if isinstance(p, dict):
            text = p.get('prompt', '')[:100]
        else:
            text = str(p)[:100]
        print('  Prompt {}: {}...'.format(i, text))
else:
    print('[ERROR] Error: {}'.format(result1))
    sys.exit(1)

# Test 2: Generate again
print('\n--- GENERATION 2 (same custom prompt) ---')
result2 = bot.image_generation_prompts(
    category='couples_transform',
    custom_prompt='Couples romantic intimacy in kitchen',
    chat_id=123
)

if result2 and 'prompts' in result2:
    print('[OK] Got {} prompts'.format(len(result2['prompts'])))
    for i, p in enumerate(result2['prompts'], 1):
        if isinstance(p, dict):
            text = p.get('prompt', '')[:100]
        else:
            text = str(p)[:100]
        print('  Prompt {}: {}...'.format(i, text))
else:
    print('[ERROR] Error: {}'.format(result2))
    sys.exit(1)

# Compare
print('\n' + '=' * 80)
print('COMPARISON')
print('=' * 80)

r1_prompts = []
for p in result1.get('prompts', []):
    if isinstance(p, dict):
        r1_prompts.append(p.get('prompt', ''))
    else:
        r1_prompts.append(str(p))

r2_prompts = []
for p in result2.get('prompts', []):
    if isinstance(p, dict):
        r2_prompts.append(p.get('prompt', ''))
    else:
        r2_prompts.append(str(p))

# Check if they're different
all_same = all(p1 == p2 for p1, p2 in zip(r1_prompts, r2_prompts))

if all_same:
    print('[FAIL] SAME PROMPTS - Caching is still active!')
    print('\nFirst 200 chars of Prompt 1 (both generations):')
    print('Gen 1: {}'.format(r1_prompts[0][:200]))
    print('Gen 2: {}'.format(r2_prompts[0][:200]))
else:
    print('[PASS] DIFFERENT PROMPTS - Caching is disabled!')
    print('\nFirst 200 chars of Prompt 1 (both generations):')
    print('Gen 1: {}'.format(r1_prompts[0][:200]))
    print('Gen 2: {}'.format(r2_prompts[0][:200]))

# Check if Bride scenario is present
if any('Bride' in p or 'bride' in p for p in r1_prompts):
    print('\n[WARN] Bride scenario still found in prompts')
else:
    print('\n[PASS] Bride scenario NOT found - using user requirement only!')

print('\n')

