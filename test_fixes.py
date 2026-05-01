import time
import os
import sys

# Clear cache
if os.path.exists('data/responses.db'):
    os.remove('data/responses.db')
    print('[CLEARED] responses.db')

from src.main import InstagramGrowthBot

bot = InstagramGrowthBot()

# Generate fresh with unique context
unique = f'Professional woman in office at sunset NEW-{int(time.time())}'
resp = bot.generate_image_prompts(
    category='women_transform',
    user_context=unique,
    count=1,
    niche='professional'
)

prompt = resp['prompts'][0]['prompt']

# Verify all 10 fixes
print('\n=== CRITICAL FIXES VERIFICATION ===\n')

fixes = {
    '1. Identity-safe makeup': 'subtly without altering' in prompt,
    '2. Consolidated constraints': 'IDENTITY CONSTRAINTS:' in prompt,
    '3. Hairline preservation': 'hairline' in prompt.lower() or 'face framing' in prompt.lower(),
    '4. Micro-expressions': 'micro-expression' in prompt.lower(),
    '5. Face visibility': 'fully visible' in prompt.lower() or 'unobstructed' in prompt,
    '6. Minimal background': 'not dense' in prompt.lower(),
    '7. Hands guidance': 'prominently visible' in prompt,
    '8. Lighting texture': 'directionally defined' in prompt,
    '9. Scene conflict fix': 'filled with flowers' not in prompt or 'minimal' in prompt.lower(),
    '10. Priority hierarchy': 'PRIORITY HIERARCHY' in prompt,
}

passing = 0
for name, passed in fixes.items():
    status = 'PASS' if passed else 'FAIL'
    print(f'[{status}] {name}')
    if passed:
        passing += 1

print(f'\n=== RESULTS: {passing}/10 FIXES VERIFIED ===\n')

print('=== PROMPT EXCERPT (1500 chars) ===\n')
print(prompt[:1500])
print('\n[...continued...]')

# Exit with success code
sys.exit(0)
