#!/usr/bin/env python3
"""
Instagram Growth Bot - Minimal Implementation
Uses Groq API + pure Python (requests, no async frameworks)
Includes metrics tracking and error resilience
"""

import os
import json
import logging
import time
from pathlib import Path
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=str(env_path))

# Configure logging with file output
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import metrics tracking
try:
    from src.metrics import metrics, health_check
    METRICS_ENABLED = True
except ImportError:
    METRICS_ENABLED = False
    logger.debug("Metrics module not available")

# Initialize Groq client
def init_groq():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("[ERROR] GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)

# Utility function for robust JSON parsing
def parse_json_response(text: str) -> dict:
    """Parse JSON from response, handling markdown code blocks and incomplete JSON"""
    text = text.strip()
    
    logger.debug(f"[DEBUG] Parsing response (length={len(text)})...")
    
    try:
        # Try direct parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try extracting from markdown code block with ```json
    if "```json" in text:
        try:
            start_marker = "```json"
            end_marker = "```"
            start = text.find(start_marker)
            if start != -1:
                start += len(start_marker)
                # Find the LAST occurrence of closing ``` to get complete JSON
                end = text.rfind(end_marker)
                if end > start:
                    json_str = text[start:end].strip()
                    if json_str:
                        logger.debug(f"[DEBUG] Found json block, length={len(json_str)}")
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            # Try to fix incomplete JSON by adding closing braces
                            logger.debug(f"[DEBUG] JSON incomplete, trying to fix...")
                            json_str = json_str.rstrip()
                            # Count opening and closing braces
                            open_count = json_str.count('{')
                            close_count = json_str.count('}')
                            if open_count > close_count:
                                json_str += '}' * (open_count - close_count)
                                logger.debug(f"[DEBUG] Added {open_count - close_count} closing braces")
                                try:
                                    return json.loads(json_str)
                                except json.JSONDecodeError:
                                    pass
        except Exception as e:
            logger.debug(f"[DEBUG] Failed to parse markdown json block: {e}")
    
    # Try extracting from generic markdown code block with ```
    if "```" in text:
        try:
            start_marker = "```"
            end_marker = "```"
            start = text.find(start_marker)
            if start != -1:
                start += len(start_marker)
                # Skip any language specifier (e.g., "python", "json")
                newline_pos = text.find("\n", start)
                if newline_pos != -1:
                    start = newline_pos + 1
                
                # Find the LAST occurrence of closing ``` to get complete JSON
                end = text.rfind(end_marker)
                if end > start:
                    json_str = text[start:end].strip()
                    if json_str:
                        logger.debug(f"[DEBUG] Found generic block, length={len(json_str)}")
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            # Try to fix incomplete JSON
                            json_str = json_str.rstrip()
                            open_count = json_str.count('{')
                            close_count = json_str.count('}')
                            if open_count > close_count:
                                json_str += '}' * (open_count - close_count)
                                try:
                                    return json.loads(json_str)
                                except json.JSONDecodeError:
                                    pass
        except Exception as e:
            logger.debug(f"[DEBUG] Failed to parse generic markdown block: {e}")
    
    # Try to find and parse any JSON object in the text
    try:
        # Look for {  ... } pattern
        start = text.find("{")
        if start != -1:
            # Try to find matching closing brace from the end
            end = text.rfind("}")
            if end > start:
                json_str = text[start:end+1]
                logger.debug(f"[DEBUG] Found raw JSON, length={len(json_str)}")
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to fix incomplete JSON
                    open_count = json_str.count('{')
                    close_count = json_str.count('}')
                    if open_count > close_count:
                        json_str += '}' * (open_count - close_count)
                        try:
                            return json.loads(json_str)
                        except:
                            pass
    except Exception as e:
        logger.debug(f"[DEBUG] Failed to parse raw JSON: {e}")
    
    # Log failed parsing for debugging
    preview = text[:500] if len(text) > 500 else text
    logger.warning(f"[WARN] JSON parsing failed. Response (first 500 chars): {preview}")
    
    # Return empty error dict if all parsing fails
    return {}

# AI Agent implementations
class InstagramGrowthBot:
    def __init__(self):
        self.client = init_groq()
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        logger.info("[OK] Bot initialized with Groq API")
        
    def generate_content(self, topic: str, style: str = "engaging") -> dict:
        """Generate viral-optimized Instagram content"""
        prompt = f"""Create 3 viral-optimized Instagram captions for a {style} post about "{topic}".
        
Include:
- Hook (first line)
- Main message
- Call-to-action
- 3-5 relevant hashtags
- Virality score (0-100)

Format as JSON with keys: captions (list), virality_score (int), hashtags (list)"""
        
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            duration = time.time() - start_time
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=True,
                    prompt_length=len(prompt)
                )
            
            result = parse_json_response(response.choices[0].message.content)
            if result:
                logger.info(f"[OK] Generated {len(result.get('captions', []))} captions")
                if METRICS_ENABLED:
                    metrics.record_content_generation(
                        topic=topic,
                        captions_count=len(result.get('captions', [])),
                        virality_score=result.get('virality_score', 0)
                    )
                    health_check.record_success()
            return result or {"error": "Failed to parse content generation"}
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Content generation error: {e}")
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=False
                )
                metrics.record_error("ContentGenerationError", str(e), "ContentGenerator")
                health_check.record_error()
            return {"error": "Failed to generate content"}
    
    def analyze_trends(self, niche: str) -> dict:
        """Analyze trending topics in a niche"""
        prompt = f"""Analyze current trending topics for a {niche} Instagram account.
        
Provide:
- Top 5 trending hashtags
- Estimated viral potential (0-100) for each
- Content ideas based on trends
- Best posting times
- Competitor strategies to watch

Format as JSON."""
        
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
            )
            
            duration = time.time() - start_time
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=True,
                    prompt_length=len(prompt)
                )
            
            result = parse_json_response(response.choices[0].message.content)
            if result:
                logger.info(f"[OK] Analyzed trends for {niche}")
                if METRICS_ENABLED:
                    health_check.record_success()
            return result or {"error": "Failed to analyze trends"}
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Trend analysis error: {e}")
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=False
                )
                metrics.record_error("TrendAnalysisError", str(e), "TrendAnalyzer")
                health_check.record_error()
            return {"error": "Failed to analyze trends"}
    
    def engagement_strategy(self, account_size: str) -> dict:
        """Generate engagement strategy based on account size"""
        prompt = f"""Create a safe, organic engagement strategy for a {account_size} Instagram account.
        
Include:
- Daily engagement targets (follows, likes, comments)
- Comment templates (5 variations)
- DM outreach strategy
- Hashtag strategy
- Timing recommendations
- Anti-bot precautions

Format as JSON."""
        
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            duration = time.time() - start_time
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=True,
                    prompt_length=len(prompt)
                )
            
            result = parse_json_response(response.choices[0].message.content)
            if result:
                logger.info(f"[OK] Generated engagement strategy for {account_size} account")
                if METRICS_ENABLED:
                    health_check.record_success()
            return result or {"error": "Failed to generate strategy"}
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Engagement strategy error: {e}")
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=False
                )
                metrics.record_error("EngagementStrategyError", str(e), "EngagementStrategist")
                health_check.record_error()
            return {"error": "Failed to generate strategy"}
    
    def image_generation_prompts(self, category: str, custom_prompt: str = None, level: str = None) -> dict:
        """Get image generation prompts from library or enhance a custom prompt.
        
        Args:
            category: Prompt category name.
            custom_prompt: Optional user-supplied concept to enhance via Groq.
            level: Difficulty filter — 'beginner', 'professional', or 'expert'.
        """
        try:
            from src.prompts.templates import (
                get_category_prompts, get_prompts_by_level,
                list_categories, get_category_meta, DIFFICULTY_EMOJI
            )
            import random

            category = category.lower().replace(" ", "_").replace("-", "_")
            all_categories = list_categories()

            if category not in all_categories:
                return {
                    "status": "error",
                    "error": f"Category '{category}' not found",
                    "available_categories": all_categories
                }

            meta = get_category_meta(category)

            # ── CUSTOM PROMPT PATH ───────────────────────────────────────────
            if custom_prompt and custom_prompt.strip():
                logger.info(f"[OK] Enhancing custom prompt — category={category}, level={level or 'auto'}")

                # Build category-specific enhancement instructions
                ENHANCE_CONFIGS = {
                    "design_posters": {
                        "task": "professional poster / social-media graphic design prompt",
                        "fields": "Resolution · Style · Colour palette (3-4 colours) · Main visual elements · Typography · Composition · File format",
                        "max_tokens": 350,
                    },
                    "ui_ux_design": {
                        "task": "detailed UI/UX design specification prompt",
                        "fields": "Platform (iOS/Android/Web) · Screen name · Key components · Colour system · Typography · Grid/spacing · Interactions · Accessibility note",
                        "max_tokens": 380,
                    },
                    "brand_identity": {
                        "task": "brand identity design prompt",
                        "fields": "Brand name & industry · Logo style · Colour palette (3-5 colours + hex) · Typography pairing · Tone of voice · Key deliverables · Format",
                        "max_tokens": 350,
                    },
                    "illustration_art": {
                        "task": "digital illustration / concept art prompt",
                        "fields": "Subject & scene · Art style · Colour palette · Lighting · Mood · Detail level · Canvas size · Tools/medium",
                        "max_tokens": 320,
                    },
                    "animation_motion": {
                        "task": "animation / motion graphics production prompt",
                        "fields": "Duration · Frame rate · Style · Key scenes (3-4) · Transitions · Audio · Text overlays · Export format",
                        "max_tokens": 320,
                    },
                    "photography_styles": {
                        "task": "photography / fine-art image prompt",
                        "fields": "Subject · Style (noir/surreal/editorial etc.) · Lighting setup · Colour grade · Lens & focal length · Mood · Resolution",
                        "max_tokens": 300,
                    },
                    "print_design": {
                        "task": "print design prompt",
                        "fields": "Format & size (with bleed) · Colour mode (CMYK/RGB) · Typography · Key visuals · Finish (gloss/matte/foil) · DPI · Print-ready notes",
                        "max_tokens": 320,
                    },
                    "product_3d": {
                        "task": "3D product visualisation / render prompt",
                        "fields": "Product type · Materials & shaders · Lighting rig · Background/environment · Camera angle · Render engine · Output resolution",
                        "max_tokens": 320,
                    },
                    "reel_scripts": {
                        "task": "Instagram Reel / short-form video script",
                        "fields": "Duration · Scene breakdown (3-4 scenes) · Transitions · Audio · Text overlays · Camera movement · Call-to-action · Format (9:16)",
                        "max_tokens": 300,
                    },
                    "women_transform": {
                        "task": "woman portrait transformation image prompt",
                        "fields": "Facial feature preservation (face shape, eye shape & colour, nose, lips, skin tone, complexion — must match reference) · Pose & body angle · Hand placement · Head angle & gaze · Expression · Outfit · Lighting · Background · Camera framing · Quality",
                        "max_tokens": 320,
                    },
                    "men_transform": {
                        "task": "man portrait transformation image prompt",
                        "fields": "Facial feature preservation (face shape, jawline, eye shape & colour, nose, lips, skin tone, beard/facial hair — must match reference) · Pose & body angle · Hand placement · Head angle & gaze · Expression · Outfit · Lighting · Background · Camera framing · Quality",
                        "max_tokens": 320,
                    },
                    "couples_transform": {
                        "task": "couples portrait transformation image prompt",
                        "fields": "Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colours, noses, lips, skin tones, complexions — must match reference images) · Couple connection pose · Face positions · Hand/arm placement · Expressions · Outfits · Lighting · Background · Camera framing · Quality",
                        "max_tokens": 340,
                    },
                }

                config = ENHANCE_CONFIGS.get(category)
                level_instruction = ""
                if level == "beginner":
                    level_instruction = "Keep it simple — suitable for beginners using Canva, basic Photoshop, or free AI tools."
                elif level == "professional":
                    level_instruction = "Write at professional industry standard. Include tool-specific terminology."
                elif level == "expert":
                    level_instruction = "Write at expert/advanced level with technical precision, niche techniques, and production-ready specs."

                if config:
                    # Build mandatory facial preservation clause for transform categories
                    transform_categories = {"women_transform", "men_transform", "couples_transform"}
                    if category in transform_categories:
                        if category == "couples_transform":
                            facial_rule = """

CRITICAL FOR 100% FACIAL PRESERVATION:
1. Start prompt with: "EXACT FACE MATCH + IDENTITY PRESERVATION"
2. Specify facial features TWICE in the prompt
3. End with: "— USE FACE_ID FROM REFERENCE IMAGE. PRESERVE every facial detail: both subjects' unique face shapes, eye shapes & colors, nose structure, lips, skin tones, complexions, jawlines, facial characteristics. Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact."
4. Add: "- Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable"
"""
                        elif category == "men_transform":
                            facial_rule = """

CRITICAL FOR 100% FACIAL PRESERVATION:
1. Start prompt with: "EXACT FACE MATCH + IDENTITY PRESERVATION"
2. Specify facial features TWICE in the prompt
3. End with: "— USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose structure, lips, skin tone, beard/facial hair, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact."
4. Add: "- Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable"
"""
                        else:  # women_transform
                            facial_rule = """

CRITICAL FOR 100% FACIAL PRESERVATION:
1. Start prompt with: "EXACT FACE MATCH + IDENTITY PRESERVATION"
2. Specify facial features TWICE in the prompt
3. End with: "— USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose structure, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact."
4. Add: "- Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable"
"""
                    else:
                        facial_rule = ""

                    enhancement_prompt = f"""Create a {config['task']} from this concept. Be CRISP and CONCISE.
{level_instruction}

Concept: {custom_prompt}

Include ONLY these essential details:
{config['fields']}

IMPORTANT: Return ONLY the prompt/spec itself — no explanations. Max 250 words.{facial_rule}"""

                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": enhancement_prompt}],
                            temperature=0.7,
                            max_tokens=config["max_tokens"],
                        )
                        enhanced = response.choices[0].message.content.strip()
                        logger.info(f"[OK] Enhanced custom prompt for {category}")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "enhanced": True,
                            "level": level or "professional",
                            "count": 1,
                            "prompts": [enhanced],
                            "meta": meta,
                            "available_categories": all_categories,
                        }
                    except Exception as e:
                        logger.warning(f"Enhancement failed, returning original: {e}")

                # Fallback: return as-is
                return {
                    "status": "success",
                    "category": category,
                    "custom": True,
                    "enhanced": False,
                    "level": level or "",
                    "count": 1,
                    "prompts": [custom_prompt.strip()],
                    "meta": meta,
                    "available_categories": all_categories,
                }

            # ── LIBRARY PATH ─────────────────────────────────────────────────
            if level and level in ("beginner", "professional", "expert"):
                prompt_strings = get_prompts_by_level(category, level)
            else:
                # Mix all levels — pick one from each if possible
                beg = get_prompts_by_level(category, "beginner")
                pro = get_prompts_by_level(category, "professional")
                exp = get_prompts_by_level(category, "expert")
                # Fall back to legacy plain-string list
                if not beg and not pro and not exp:
                    raw = get_category_prompts(category)
                    prompt_strings = [p if isinstance(p, str) else p["prompt"] for p in raw]
                else:
                    pool = []
                    if beg:
                        pool.append(random.choice(beg))
                    if pro:
                        pool.append(random.choice(pro))
                    if exp:
                        pool.append(random.choice(exp))
                    prompt_strings = pool

            if not prompt_strings:
                return {"status": "error", "error": f"No prompts found for '{category}'"}

            selected = random.sample(prompt_strings, min(3, len(prompt_strings)))
            logger.info(f"[OK] Serving {len(selected)} library prompts — category={category}, level={level or 'mixed'}")

            return {
                "status": "success",
                "category": category,
                "custom": False,
                "level": level or "mixed",
                "count": len(selected),
                "prompts": selected,
                "meta": meta,
                "available_categories": all_categories,
            }

        except Exception as e:
            logger.error(f"image_generation_prompts error: {e}")
            return {"status": "error", "error": str(e)}

    def search_prompts(self, keyword: str) -> dict:
        """Search all prompt categories for a keyword."""
        try:
            from src.prompts.templates import search_prompts as _search
            results = _search(keyword)
            return {"status": "success", "keyword": keyword, "count": len(results), "results": results[:10]}
        except Exception as e:
            return {"status": "error", "error": str(e)}


    
    def monetization_ideas(self, niche: str, follower_count: int) -> dict:
        """Suggest monetization strategies"""
        prompt = f"""Suggest monetization strategies for a {niche} Instagram account with {follower_count} followers.
        
Include:
- 6 Revenue streams (sponsored posts, affiliates, digital products, etc.)
- Realistic revenue projections
- Implementation timeline
- Partner types to target
- Pricing recommendations
- Success metrics

Format as JSON."""
        
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            duration = time.time() - start_time
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=True,
                    prompt_length=len(prompt)
                )
            
            result = parse_json_response(response.choices[0].message.content)
            if result:
                logger.info(f"[OK] Generated monetization ideas for {follower_count}+ followers")
                if METRICS_ENABLED:
                    health_check.record_success()
            return result or {"error": "Failed to generate ideas"}
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Monetization ideas error: {e}")
            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model,
                    duration=duration,
                    success=False
                )
                metrics.record_error("MonetizationError", str(e), "MonetizationAdvisor")
                health_check.record_error()
            return {"error": "Failed to generate ideas"}

def main():
    """Main bot function"""
    logger.info("="*60)
    logger.info("[BOT] Instagram Growth Bot Started")
    logger.info("="*60)
    
    # Initialize bot
    bot = InstagramGrowthBot()
    
    # Example usage
    print("\n" + "="*60)
    print("[DEMO] Content Generation")
    print("="*60)
    content = bot.generate_content(topic="fitness transformation", style="motivational")
    print(json.dumps(content, indent=2))
    
    print("\n" + "="*60)
    print("[DEMO] Trend Analysis")
    print("="*60)
    trends = bot.analyze_trends(niche="fitness")
    print(json.dumps(trends, indent=2))
    
    print("\n" + "="*60)
    print("[DEMO] Engagement Strategy")
    print("="*60)
    strategy = bot.engagement_strategy(account_size="micro (5K-100K)")
    print(json.dumps(strategy, indent=2))
    
    print("\n" + "="*60)
    print("[DEMO] Monetization Ideas")
    print("="*60)
    monetization = bot.monetization_ideas(niche="fitness", follower_count=50000)
    print(json.dumps(monetization, indent=2))
    
    # Finalize metrics
    if METRICS_ENABLED:
        metrics.finalize_session()
        metrics.print_summary()
    
    logger.info("[OK] Bot demo completed successfully!")

if __name__ == "__main__":
    main()
