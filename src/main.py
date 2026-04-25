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
    
    def image_generation_prompts(self, category: str, custom_prompt: str = None) -> dict:
        """Get image generation prompts from library or use custom prompt"""
        try:
            # Import the prompt library
            from src.prompts.templates import get_category_prompts, list_categories
            
            # Normalize category name
            category = category.lower().replace(" ", "_").replace("-", "_")
            
            # Get all categories
            all_categories = list_categories()
            
            # Check if category exists
            if category not in all_categories:
                return {
                    "status": "error",
                    "error": f"Category '{category}' not found",
                    "available_categories": all_categories
                }
            
            # If custom prompt provided, enhance it for the category
            if custom_prompt and custom_prompt.strip():
                logger.info(f"[OK] Processing custom prompt for category: {category}")
                
                # For design_posters, enhance with design specifications
                if category == "design_posters":
                    enhancement_prompt = f"""Create a professional poster design prompt from this concept. Be CRISP and CONCISE:

Concept: {custom_prompt}

Generate prompt with ONLY essential details:
- Resolution: 1920x1080
- Style: [specify style]
- Key colors: [3-4 colors only]
- Main elements: [key visual elements]
- Typography: [font style and placement]
- Composition: [layout approach]
- Quality: 8K professional

Return ONLY the prompt, max 300 words."""
                    
                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": enhancement_prompt}],
                            temperature=0.7,
                            max_tokens=350  # Shorter max_tokens for conciseness
                        )
                        enhanced_prompt = response.choices[0].message.content.strip()
                        logger.info(f"[OK] Enhanced custom prompt for design_posters")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "enhanced": True,
                            "count": 1,
                            "prompts": [enhanced_prompt],
                            "note": "Enhanced poster design prompt ready for DALL-E 3, Midjourney, Stable Diffusion",
                            "available_categories": all_categories
                        }
                    except Exception as e:
                        logger.warning(f"Failed to enhance prompt, returning original: {e}")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "count": 1,
                            "prompts": [custom_prompt.strip()],
                            "note": "Custom prompt ready for DALL-E 3, Midjourney, Stable Diffusion",
                            "available_categories": all_categories
                        }
                
                # For reel_scripts, enhance with production specifications
                elif category == "reel_scripts":
                    enhancement_prompt = f"""Create a professional reel script from this concept. Be CRISP and CONCISE:

Concept: {custom_prompt}

Generate script with ONLY essential details:
- Duration: [15s/30s/45s]
- Scene breakdown: [3-4 key scenes]
- Transitions: [transition style]
- Audio: [music genre/pacing]
- Text overlays: [key text elements]
- Camera movement: [primary camera technique]
- Call-to-action: [main CTA]
- Format: Vertical (9:16)

Return ONLY the script, max 250 words."""
                    
                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": enhancement_prompt}],
                            temperature=0.7,
                            max_tokens=300  # Shorter for conciseness
                        )
                        enhanced_prompt = response.choices[0].message.content.strip()
                        logger.info(f"[OK] Enhanced custom prompt for reel_scripts")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "enhanced": True,
                            "count": 1,
                            "prompts": [enhanced_prompt],
                            "note": "Enhanced reel script ready for video production",
                            "available_categories": all_categories
                        }
                    except Exception as e:
                        logger.warning(f"Failed to enhance prompt, returning original: {e}")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "count": 1,
                            "prompts": [custom_prompt.strip()],
                            "note": "Custom reel script ready",
                            "available_categories": all_categories
                        }
                
                # For transform categories, enhance with pose and context specifications
                elif category in ["women_transform", "men_transform", "couples_transform"]:
                    transform_type = {
                        "women_transform": "woman",
                        "men_transform": "man",
                        "couples_transform": "couple"
                    }[category]
                    
                    enhancement_prompt = f"""Create a detailed transformation prompt for portrait image generation. Be CRISP and CONCISE:

Concept: {custom_prompt}

Generate prompt with ONLY essential details:
- Specific pose: [body position and angle]
- Hand placement: [hands position]
- Head angle: [head position and gaze]
- Expression: [facial expression]
- Outfit: [clothing description]
- Lighting: [light type and direction]
- Background: [background setting]
- Camera: [framing and angle]
- Quality: 8K professional

IMPORTANT: The pose should be transformable (different from original) while face can be referenced.

Return ONLY the prompt, max 250 words."""
                    
                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": enhancement_prompt}],
                            temperature=0.7,
                            max_tokens=300  # Shorter for conciseness
                        )
                        enhanced_prompt = response.choices[0].message.content.strip()
                        logger.info(f"[OK] Enhanced custom prompt for {category}")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "enhanced": True,
                            "count": 1,
                            "prompts": [enhanced_prompt],
                            "note": f"Enhanced transformation prompt for {transform_type} - use with face reference for pose transformation",
                            "available_categories": all_categories
                        }
                    except Exception as e:
                        logger.warning(f"Failed to enhance prompt, returning original: {e}")
                        return {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "count": 1,
                            "prompts": [custom_prompt.strip()],
                            "note": f"Custom {transform_type} transformation prompt ready",
                            "available_categories": all_categories
                        }
                
                # For other categories, return custom prompt as-is
                else:
                    logger.info(f"[OK] Using custom prompt for category: {category}")
                    return {
                        "status": "success",
                        "category": category,
                        "custom": True,
                        "count": 1,
                        "prompts": [custom_prompt.strip()],
                        "note": "Custom prompt ready for DALL-E 3, Midjourney, Stable Diffusion, or other image generators",
                        "available_categories": all_categories
                    }
            
            # Get prompts for the category from library
            prompts = get_category_prompts(category)
            
            if not prompts:
                return {
                    "status": "error",
                    "error": f"No prompts found for category '{category}'"
                }
            
            # Return 3 random prompts from category
            import random
            selected = random.sample(prompts, min(3, len(prompts)))
            
            logger.info(f"[OK] Generated {len(selected)} prompts for category: {category}")
            
            return {
                "status": "success",
                "category": category,
                "count": len(selected),
                "prompts": selected,
                "note": "Use these prompts with DALL-E 3, Midjourney, Stable Diffusion, or other image generators",
                "available_categories": all_categories
            }
        except Exception as e:
            logger.error(f"Image generation prompts error: {e}")
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
