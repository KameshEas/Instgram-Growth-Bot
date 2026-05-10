#!/usr/bin/env python3
"""
Instagram Growth Bot - Minimal Implementation
Uses Groq API + pure Python (requests, no async frameworks)
Includes metrics tracking and error resilience
"""

import os
import json
import hashlib
import logging
import sys
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

# Ensure stdout/stderr use UTF-8 on Windows consoles to avoid UnicodeEncodeError
try:
    if sys.stdout and (sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr and (sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

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

# Import prompt logging / response cache (SQLite-backed)
try:
    import src.database.prompt_log as _plog
    PROMPT_LOG_ENABLED = True
except Exception:
    PROMPT_LOG_ENABLED = False
    logger.debug("Prompt log module not available")

# Initialize Groq client
def init_groq():
    """L1 FIX: Descriptive error messages for initialization failures."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "[ERROR L1] GROQ_API_KEY not found in .env file. "
            "Ensure .env exists in project root with GROQ_API_KEY=<your-api-key>. "
            "Get API key from: https://console.groq.com"
        )
    return Groq(api_key=api_key)

# Utility function for robust JSON parsing
def parse_json_response(text: str) -> dict:
    """Parse JSON from response, handling markdown code blocks, incomplete JSON, and embedded JSON
    
    L1 FIX: Descriptive error messages with context about parsing failure
    """
    text = text.strip()
    
    if not text:
        logger.warning("[WARN] JSON parsing failed: empty response text received (expected JSON object or array)")
        return {"error": "Empty response - no content to parse"}
    
    logger.debug(f"[DEBUG] Parsing response (length={len(text)}, first 200 chars: {text[:200]})...")
    
    try:
        # Try direct parsing first
        result = json.loads(text)
        if isinstance(result, dict):
            logger.debug("[DEBUG] Successfully parsed as direct JSON")
            return result
    except json.JSONDecodeError as e:
        logger.debug(f"[DEBUG] Direct JSON parse failed at position {e.pos}: {e.msg}")
        pass
    
    # Try extracting from markdown code block with ```json
    if "```json" in text:
        try:
            start_marker = "```json"
            end_marker = "```"
            start = text.find(start_marker)
            if start != -1:
                start += len(start_marker)
                end = text.rfind(end_marker)
                if end > start:
                    json_str = text[start:end].strip()
                    if json_str:
                        logger.debug(f"[DEBUG] Found ```json block, length={len(json_str)}")
                        try:
                            result = json.loads(json_str)
                            if isinstance(result, dict):
                                return result
                        except json.JSONDecodeError as e:
                            logger.debug(f"[DEBUG] ```json block failed to parse: {e}")
                            # Try to fix incomplete JSON
                            json_str = json_str.rstrip().rstrip(",")
                            open_count = json_str.count('{') + json_str.count('[')
                            close_count = json_str.count('}') + json_str.count(']')
                            if open_count > close_count:
                                json_str += '}' * (json_str.count('{') - json_str.count('}'))
                                logger.debug(f"[DEBUG] Attempting to fix missing braces...")
                                try:
                                    result = json.loads(json_str)
                                    if isinstance(result, dict):
                                        return result
                                except:
                                    pass
        except Exception as e:
            logger.debug(f"[DEBUG] Failed to parse ```json block: {e}")
    
    # Try extracting from generic markdown code block with ```
    if "```" in text and "```json" not in text:
        try:
            start_marker = "```"
            end_marker = "```"
            start = text.find(start_marker)
            if start != -1:
                start += len(start_marker)
                newline_pos = text.find("\n", start)
                if newline_pos != -1:
                    start = newline_pos + 1
                
                end = text.rfind(end_marker)
                if end > start:
                    json_str = text[start:end].strip()
                    if json_str:
                        logger.debug(f"[DEBUG] Found generic ``` block, length={len(json_str)}")
                        try:
                            result = json.loads(json_str)
                            if isinstance(result, dict):
                                return result
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            logger.debug(f"[DEBUG] Failed to parse generic ``` block: {e}")
    
    # Try to find and parse JSON (objects or arrays)
    try:
        # Find both opening characters to determine which to parse
        obj_start = text.find("{")
        arr_start = text.find("[")
        
        # Determine which JSON structure to parse
        start = None
        is_array = False
        
        if obj_start != -1 and arr_start != -1:
            # Both present, use whichever comes first
            if arr_start < obj_start:
                start = arr_start
                is_array = True
            else:
                start = obj_start
                is_array = False
        elif arr_start != -1:
            # Only array
            start = arr_start
            is_array = True
        elif obj_start != -1:
            # Only object
            start = obj_start
            is_array = False
        
        if start != -1:
            if is_array:
                end = text.rfind("]")
                if end > start:
                    json_str = text[start:end+1]
                    logger.debug(f"[DEBUG] Found JSON array, length={len(json_str)}")
                    try:
                        result = json.loads(json_str)
                        if isinstance(result, list) and result:
                            return {"prompts": result}  # Wrap array in dict
                    except json.JSONDecodeError:
                        pass
            else:
                end = text.rfind("}")
                if end > start:
                    json_str = text[start:end+1]
                    logger.debug(f"[DEBUG] Found raw JSON object, length={len(json_str)}")
                    try:
                        result = json.loads(json_str)
                        if isinstance(result, dict) and result:
                            return result
                    except json.JSONDecodeError as e:
                        logger.debug(f"[DEBUG] Raw JSON parse failed: {e}")
                        # Try to fix incomplete JSON
                        json_str_fixed = json_str.rstrip().rstrip(",")
                        open_braces = json_str_fixed.count('{')
                        close_braces = json_str_fixed.count('}')
                        if open_braces > close_braces:
                            json_str_fixed += '}' * (open_braces - close_braces)
                            logger.debug(f"[DEBUG] Attempting fix: added {open_braces - close_braces} closing braces")
                            try:
                                result = json.loads(json_str_fixed)
                                if isinstance(result, dict) and result:
                                    return result
                            except:
                                pass
    except Exception as e:
        logger.debug(f"[DEBUG] Failed to parse JSON: {e}")
    
    # Log failed parsing for debugging
    preview = text[:300] if len(text) > 300 else text
    logger.warning(
        f"[WARN L1] JSON parsing failed after attempting: direct parse, ```json blocks, generic code blocks, raw extraction. "
        f"Response length: {len(text)} chars, starts with: {preview}..."
    )
    
    # Return empty dict with error indicator
    return {"error": "Failed to parse JSON response (no valid JSON found after attempts at multiple extraction methods)"}

# AI Agent implementations
class InstagramGrowthBot:
    def __init__(self):
        self.client = init_groq()
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        if PROMPT_LOG_ENABLED:
            _plog.init_prompt_log_db()
            _plog.purge_expired_cache()
        logger.info("[OK] Bot initialized with Groq API")

    # ── Private helpers ──────────────────────────────────────────────────────

    def _make_cache_key(self, command: str, **context) -> str:
        """Build a deterministic SHA-256 cache key from command + semantic context."""
        parts = [command]
        for field in ("niche", "account_stage", "region", "action", "topic"):
            parts.append(str(context.get(field, "")).lower().strip())
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()

    def _call_groq_with_fallback(
        self,
        command: str,
        cache_key: str,
        prompt: str,
        chat_id: int = None,
        temperature: float = 0.7,
        max_tokens: int = None,
        ttl_hours: int = None,
    ) -> dict:
        """Centralised Groq call with DB logging and tiered fallback cache.

        Flow:
        1. Check fresh cache → return immediately on hit (unless ttl_hours=None).
        2. Call Groq → on success log + cache + return result.
        3. On failure → log error → serve stale cache with _stale flag.
        4. Nothing cached → return error dict.
        """
        # Step 1 — fresh cache check (SKIP if ttl_hours=None, meaning no caching for this request)
        if PROMPT_LOG_ENABLED and ttl_hours is not None:  # Only use cache if caching is enabled (ttl_hours set)
            cached = _plog.get_cached_response(cache_key)
            if cached:
                logger.info("[CACHE] Fresh hit for %s", command)
                return {**cached, "_from_cache": True, "_stale": False}

        call_kwargs: dict = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        if max_tokens:
            call_kwargs["max_tokens"] = max_tokens

        start = time.time()
        try:
            response = self.client.chat.completions.create(**call_kwargs)
            duration = time.time() - start
            latency_ms = int(duration * 1000)

            if METRICS_ENABLED:
                metrics.record_api_call(
                    model=self.model, duration=duration,
                    success=True, prompt_length=len(prompt),
                )

            result = parse_json_response(response.choices[0].message.content)

            if result:
                if METRICS_ENABLED:
                    health_check.record_success()
                if PROMPT_LOG_ENABLED:
                    _plog.log_prompt_response(
                        command=command, prompt_hash=cache_key,
                        prompt_text=prompt, response_json=json.dumps(result),
                        success=1, latency_ms=latency_ms, model=self.model,
                        chat_id=chat_id,
                    )
                    _plog.upsert_cache(
                        cache_key=cache_key, command=command,
                        response_json=json.dumps(result), ttl_hours=ttl_hours,
                    )
                return result

            # Parse failure — log what we got
            raw_response = response.choices[0].message.content[:500]  # First 500 chars
            logger.error(
                f"[ERROR L1] {command}: JSON parse failed after {latency_ms}ms latency. "
                f"Expected JSON object/array but received invalid format. "
                f"Response preview: {raw_response}..."
            )
            
            # Parse failure — try stale cache as fallback (only if caching enabled)
            if PROMPT_LOG_ENABLED and ttl_hours is not None:  # Only fall back to stale cache if this request uses caching
                _plog.log_prompt_response(
                    command=command, prompt_hash=cache_key, prompt_text=prompt,
                    response_json=None, success=0, error_msg="JSON parse failed after all parsing attempts",
                    latency_ms=latency_ms, model=self.model, chat_id=chat_id,
                )
                stale = _plog.get_cached_response(cache_key, ignore_ttl=True)
                if stale:
                    logger.warning("[CACHE] Stale fallback for %s (parse failure after %dms)", command, latency_ms)
                    return {**stale, "_from_cache": True, "_stale": True}
            return {"error": f"Failed to parse {command} response (JSON invalid - tried 4 extraction methods)"}

        except Exception as exc:
            duration = time.time() - start
            latency_ms = int(duration * 1000)
            logger.error(
                f"[ERROR L1] {command} execution failed after {latency_ms}ms: "
                f"{type(exc).__name__}: {str(exc)}. Model: {self.model}"
            )
            if METRICS_ENABLED:
                metrics.record_api_call(model=self.model, duration=duration, success=False)
                metrics.record_error(f"{command}Error", f"{type(exc).__name__}: {str(exc)}", command)
                health_check.record_error()
            if PROMPT_LOG_ENABLED:
                _plog.log_prompt_response(
                    command=command, prompt_hash=cache_key, prompt_text=prompt,
                    response_json=None, success=0, error_msg=f"{type(exc).__name__}: {str(exc)}",
                    latency_ms=latency_ms, model=self.model, chat_id=chat_id,
                )
                # Only use stale cache if caching is enabled (ttl_hours set)
                if ttl_hours is not None:
                    stale = _plog.get_cached_response(cache_key, ignore_ttl=True)
                    if stale:
                        logger.warning(
                            f"[CACHE] Stale fallback for {command} (AI unavailable after {latency_ms}ms): {type(exc).__name__}"
                        )
                        return {**stale, "_from_cache": True, "_stale": True}
            return {"error": f"Failed to execute {command} (Groq API error - {type(exc).__name__})"}
        
    def generate_content(
        self,
        topic: str,
        style: str = "engaging",
        niche: str = "",
        follower_count: int = None,
        region: str = "",
        language: str = "English",
        account_stage: str = "",
        chat_id: int = None,
    ) -> dict:
        """Generate viral-optimized Instagram content using full account context."""
        ctx_lines = []
        if niche:
            ctx_lines.append(f"- Niche: {niche}")
        if follower_count:
            ctx_lines.append(f"- Followers: {follower_count:,}")
        if account_stage:
            ctx_lines.append(f"- Account stage: {account_stage}")
        if region:
            ctx_lines.append(f"- Target region: {region}")
        if language and language.lower() != "english":
            ctx_lines.append(f"- Content language: {language}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "- No account profile provided"

        prompt = f"""You are an expert Instagram content strategist.

Account context:
{context_block}

Topic: "{topic}"
Style: {style}

Generate the optimal set of Instagram captions for this account. Decide the best number based on the topic and account stage. For each caption include a compelling hook, main message, and strong call-to-action.

Return JSON with:
- captions: list of caption objects, each with: hook (opening line ≤15 words), body (main message), cta (call-to-action), format_type (Reel/Carousel/Static/Story)
- hashtags: list of relevant hashtags tailored to this niche and region (you decide the right quantity and mix)
- virality_score: estimated score 0-100 with brief reasoning
- posting_tip: one actionable tip specific to this content and account stage"""

        cache_key = self._make_cache_key(
            "generate_content", niche=niche, account_stage=account_stage,
            region=region, topic=topic,
        )
        result = self._call_groq_with_fallback(
            command="generate_content", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.7,
        )
        if result and "error" not in result and METRICS_ENABLED:
            metrics.record_content_generation(
                topic=topic,
                captions_count=len(result.get("captions", [])),
                virality_score=result.get("virality_score", 0),
            )
            logger.info("[OK] Generated %d captions", len(result.get("captions", [])))
        return result
    
    def analyze_trends(
        self,
        niche: str,
        region: str = "",
        scraped_trends: list = None,
        chat_id: int = None,
    ) -> dict:
        """Analyze trending topics using real scraped data where available."""
        if scraped_trends:
            scraped_block = (
                f"Live scraped trends (Reddit / GitHub / HN):\n"
                f"{json.dumps(scraped_trends[:30], indent=2)}\n"
                f"Analyse these real-world trends for relevance to the {niche} niche."
            )
        else:
            scraped_block = (
                f"No live scrape data available. Use your knowledge of current {niche} trends "
                f"and the broader social-media landscape."
            )

        region_note = f" Target audience region: {region}." if region else ""

        prompt = f"""You are an Instagram growth strategist specialising in trend analysis.{region_note}

Niche: {niche}

{scraped_block}

Provide a comprehensive trend analysis. Let the data and niche guide how many hashtags and ideas to surface — do not limit yourself to a fixed count.

Return JSON with:
- trending_hashtags: list of objects with hashtag, relevance_to_niche (0-100), why_it_works
- content_ideas: list of specific, actionable content ideas based on the trends
- posting_schedule: recommended times for {region or 'the target'} audience (include timezone reasoning)
- competitor_insights: strategies to watch or adopt
- trend_summary: 2-sentence overview of the current trend landscape"""

        cache_key = self._make_cache_key("analyze_trends", niche=niche, region=region)
        return self._call_groq_with_fallback(
            command="analyze_trends", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.6, ttl_hours=6,
        )
    
    def engagement_strategy(
        self,
        account_size: str,
        niche: str = "",
        follower_count: int = None,
        region: str = "",
        content_mix: dict = None,
        chat_id: int = None,
    ) -> dict:
        """Generate a personalised safe organic engagement strategy."""
        ctx_lines = [f"- Account size tier: {account_size}"]
        if niche:
            ctx_lines.append(f"- Niche: {niche}")
        if follower_count:
            ctx_lines.append(f"- Current followers: {follower_count:,}")
        if region:
            ctx_lines.append(f"- Region: {region}")
        if content_mix:
            ctx_lines.append(f"- Content mix: {json.dumps(content_mix)}")
        context_block = "\n".join(ctx_lines)

        prompt = f"""You are an Instagram growth coach specialising in safe, organic engagement.

Account context:
{context_block}

Create a personalised engagement strategy for this account. Base all recommendations on the specific niche, region, and account stage — do not use generic one-size-fits-all numbers.

Return JSON with:
- daily_engagement_plan: specific daily actions tailored to this niche and stage (the AI determines right volume/frequency)
- comment_templates: niche-specific comment templates the creator can personalise
- dm_strategy: DM outreach approach appropriate for this account size and niche
- hashtag_approach: how to find and use hashtags for this specific niche
- timing_recommendations: best posting times for this niche and region audience
- anti_spam_guidelines: how to stay safe while growing organically
- growth_projection: realistic projection based on consistent execution of this strategy"""

        cache_key = self._make_cache_key(
            "engagement_strategy", niche=niche, account_stage=account_size, region=region,
        )
        result = self._call_groq_with_fallback(
            command="engagement_strategy", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.7, ttl_hours=48,
        )
        if result and "error" not in result:
            logger.info("[OK] Generated engagement strategy for %s account", account_size)
        return result
    
    def image_generation_prompts(self, category: str = "general_photography", 
                                  custom_prompt: str = None, level: str = None, 
                                  niche: str = "", chat_id: int = None, 
                                  reference_image_text: str = None,
                                  temperature: float = None,
                                  guidance: float = None,
                                  count: int = None) -> dict:
        """Enhance custom prompt or generate AI-only prompts.
        
        Architecture: Pure AI-generated prompts (no static library).
        All prompt generation uses Groq AI — no library fallback.
        
        Args:
            category: Content category (used for context only)
            custom_prompt: Optional user-supplied concept to enhance via AI
            level: Difficulty level (context for AI)
            niche: Optional niche/brand context
            chat_id: Optional chat ID for logging
            reference_image_text: Optional description of reference image for design_gifts
        
        Returns:
            Dict with generated prompts via AI
        """
        try:
            from src.prompts.templates import list_categories, get_category_meta
            
            category = category.lower().replace(" ", "_").replace("-", "_")
            all_categories = list_categories()
            
            if category not in all_categories:
                category = "general_photography"
            
            meta = get_category_meta(category)
            
            # If custom prompt provided, enhance it via AI
            if custom_prompt and custom_prompt.strip():
                logger.info(f"[AI] Enhancing custom prompt — category={category}")
                
                # For transformations and design_gifts, generate multiple variations
                # Transformations: 3 variants to show different scenes/styles with same identity
                # Design_gifts with reference: 3-4 outfit variations
                # Others: single prompt
                if category in {"women_transform", "men_transform", "couples_transform"}:
                    prompt_count = 3  # Multiple transformation variants to show variation while preserving identity
                elif category == "design_gifts" and reference_image_text:
                    prompt_count = 3  # Multiple outfit variations
                else:
                    prompt_count = 1
                
                return self.generate_image_prompts(
                    category=category,
                    niche="",  # Not a niche context - custom_prompt is the transformation directive
                    count= prompt_count if count is None else count,
                    user_context=custom_prompt,  # Pass custom_prompt as the actual user requirement
                    chat_id=chat_id,
                    reference_image_text=reference_image_text
                )
            
            # Otherwise, generate via AI
            return self.generate_image_prompts(
                    category=category,
                    niche=niche,
                    count= count or 3,
                    user_context="",
                    chat_id=chat_id,
                    reference_image_text=reference_image_text,
                    temperature=temperature,
                )
        
        except Exception as e:
            logger.error(f"image_generation_prompts error: {e}")
            return {"status": "error", "error": str(e)}

    def generate_image_prompts(
        self,
        category: str = "general_photography",
        niche: str = "",
        count: int = 3,
        user_context: str = "",
        chat_id: int = None,
        reference_image_text: str = None,
        temperature: float = None,
        guidance: float = None,
    ) -> dict:
        """Generate AI-crafted, niche-tailored image generation prompts for a given category.
        
                                            temperature=temperature if temperature is not None else 0.8,
            reference_image_text: Optional description of reference image for categories like design_gifts
                                 (e.g., "couple photo for personalized gift design")
        """
        CATEGORY_DESC = {
            "general_photography":  "lifestyle, street, travel, and editorial photography",
            "women_professional":   "professional/corporate female portrait photography",
            "women_transform":      "female portrait transformation with reference-based identity preservation and scenario-specific generation",
            "men_professional":     "professional/corporate male portrait photography",
            "men_transform":        "male portrait transformation with reference-based identity preservation and scenario-specific generation",
            "couples_transform":    "couples portrait transformation with relationship-context awareness and dual-identity preservation through reference foundation",
            "design_posters":       "social media poster and graphic design",
            "design_gifts":         "personalized gift design and custom merchandise",
            "ui_ux_design":         "UI/UX screen and interface design",
            "brand_identity":       "brand identity and logo design",
            "illustration_art":     "digital illustration and concept art",
            "animation_motion":     "animation and motion graphics",
            "photography_styles":   "fine-art and editorial photography styles",
            "print_design":         "print collateral and marketing design",
            "product_3d":           "3D product visualisation and rendering",
            "reel_scripts":         "Instagram Reel short-form video scripts",
        }

        transform_categories = {"women_transform", "men_transform", "couples_transform"}
        category_desc = CATEGORY_DESC.get(category, category.replace("_", " "))
        
        # Sanitize niche and user_context to prevent quote/JSON breaking
        niche_safe = (niche or "").replace('"', "'").replace("\n", " ").strip()[:100]
        user_context_safe = (user_context or "").replace('"', "'").replace("\n", " ").strip()[:200]
        
        niche_line = f"\nNiche/brand: {niche_safe}" if niche_safe else ""
        context_line = f"\nUser requirement: {user_context_safe}" if user_context_safe else ""
        
        # Build reference image context for transformations
        reference_line = ""
        if category in transform_categories and reference_image_text:
            reference_line = f"\n\nREFERENCE IMAGE PROVIDED: {reference_image_text}\nUse this description to anchor facial identity preservation across all variants."

        # Use specialized prompt template for transformation tasks
        if category in transform_categories:
            # For transformation with CUSTOM prompt, use a simplified template that respects user's requirement
            if user_context_safe and user_context_safe.strip():
                # CUSTOM TRANSFORMATION: User-driven requirement only (no hardcoded scenarios)
                prompt = f"""You are an expert AI image generation prompt engineer for identity-locked portrait transformations.

Category: {category_desc}{niche_line}{context_line}

USER'S TRANSFORMATION REQUIREMENT: {user_context_safe}

ABSOLUTE PRIORITY: IDENTITY LOCK (NO EXCEPTIONS)
- IDENTITY MUST BE PIXEL-PERFECT IDENTICAL TO REFERENCE IMAGE
- Face direction/angle/pose/expression: CAN CHANGE to fit the user's requirement
- Everything else about the face: CANNOT CHANGE (not even 1% alteration)

FACIAL FEATURE PRESERVATION (DO NOT ALTER EVEN SLIGHTLY):
Preserve identically: Eye shape, size, spacing, iris color, pupil shape | Nose structure, tip, nostrils, width | Mouth shape, lip fullness, corners | Cheekbone height and prominence | Jawline shape and definition | Face shape | Skin tone (exact match) | Skin texture | Forehead, chin structure | Face proportions | Unique facial characteristics, birthmarks, asymmetries | Eyebrow shape, thickness, arch, spacing | Hairline position and shape

Forbidden: Any beautification, skin smoothing, feature alteration, plastic surgery effects, artificial perfection, identity change

SCENE TRANSFORMATION (WHAT CAN CHANGE):
- Hair direction, style, color (completely new) | Makeup type (new, not from reference) | Clothing/costume (scene-appropriate) | Face angle and pose (optimize for requirement) | Expression | Lighting (preserve skin texture while enhancing mood) | Background

TECHNICAL REQUIREMENTS:
Composition: Medium close-up (waist-up), 50mm portrait lens style, eye-level or slight angle
Face Clarity: Sharpest element, fully visible, most detailed
Hands: Anatomically correct, properly detailed if visible
Lighting: Soft, preserving skin texture (no over-smoothing)
Background: Minimal, blurred, supporting
Skin Texture: Natural with visible pores, no artificial smoothing
Realism: Strict photorealism

NEGATION INSTRUCTIONS:
Negative: "avoid beautification, avoid face smoothing, avoid skin enhancement, avoid retouching, avoid feature alteration, avoid plastic surgery effects, avoid artificial perfection, avoid Photoshop effects, avoid feature reshaping, avoid identity change"

INSTRUCTION:
- Create {count} DISTINCT transformation prompts (each 100-160 words), each showing a DIFFERENT creative interpretation of the user's requirement
- Each prompt MUST preserve facial identity absolutely while varying pose, clothing, environment, lighting, and mood to match different aspects of the requirement
- Ensure each prompt is visually distinct in its interpretation of the requirement
- DO NOT add template scenarios (Bride/Professional/Casual) — use ONLY the user's requirement to drive the generation
- Each prompt MUST start with facial feature preservation statement
- Each prompt MUST END with explicit negation instructions

Return ONLY valid JSON (no markdown, no text before/after):
{{
  "prompts": [
    {{"prompt": "<100-160 word prompt preserving identity, using user requirement, with negatives>", "interpretation": "<brief 2-3 word description of this prompt's creative angle>"}}
  ],
  "tip": "Identity preservation + user requirement focus technique used"
}}"""
                return self._call_groq_with_fallback(
                    command="generate_image_prompts",
                    cache_key=self._make_cache_key(
                        "generate_image_prompts",
                        niche=niche,
                        action=category,
                        topic=user_context_safe[:50],
                    ),
                    prompt=prompt,
                    chat_id=chat_id,
                    temperature=temperature if temperature is not None else 0.8,
                    ttl_hours=None,  # NO CACHE for custom prompts
                )
            
            # For transformation with custom prompt, use it to define the scene
            # Otherwise use category-based approach
            transformation_directive = ""
            artistic_style_emphasis = ""
            
            prompt = f"""You are an expert AI image generation prompt engineer for identity-locked portrait transformations.

Category: {category_desc}{niche_line}{context_line}{reference_line}{transformation_directive}{artistic_style_emphasis}

ABSOLUTE PRIORITY: IDENTITY LOCK (NO EXCEPTIONS)
- IDENTITY MUST BE PIXEL-PERFECT IDENTICAL TO REFERENCE IMAGE
- Face direction/angle/pose/expression: CAN CHANGE per scene
- Everything else about the face: CANNOT CHANGE (not even 1% alteration)

FACIAL FEATURE PRESERVATION (DO NOT ALTER EVEN SLIGHTLY):
✓ PRESERVE EXACTLY: Eye shape, size, spacing, iris color, pupil shape | Nose structure, tip, nostrils, width | Mouth shape, lip fullness, corners | Cheekbone height and prominence | Jawline shape and definition | Face shape (oval/round/square) | Skin tone (exact match, no warming/cooling) | Skin texture (pores, natural blemishes, texture patterns) | Forehead width and height | Chin structure and projection | Face proportions (distance between features) | Unique facial characteristics, birthmarks, asymmetries | Eyebrow shape, thickness, arch, spacing | Hairline position and shape

✗ ABSOLUTELY FORBIDDEN: Any skin smoothing or artificial enhancement | Any beautification or retouching | Any feature adjustment (bigger eyes, smaller nose, fuller lips, etc.) | Any facial structure alteration | Any skin tone warming, cooling, or lightening | Any feature reshaping or refinement | Any asymmetry correction | Filters, effects, or stylization that change facial appearance | Any micro-alterations that change identity perception

SCENE TRANSFORMATION (WHAT CAN CHANGE):
- Hair direction, style, color (completely new - NOT from reference) | Makeup type and intensity (NEW - NOT from reference) | Clothing/costume (completely new scene-appropriate attire) | Face direction, angle, pose (optimize for scene) | Expression, micro-expressions (appropriate to scene action) | Lighting intensity and direction (preserve skin texture while enhancing mood) | Background elements (soft, blurred, non-distracting)

ACCESSORY & STYLING HARMONY (CRITICAL COORDINATION RULES):
⭐ JEWELRY & ACCESSORIES MUST COORDINATE WITH OUTFIT:
- Earrings: Metal tone and style must complement outfit colors (gold accessories with warm tones, silver with cool tones, rose gold versatile)
- Jewelry color: Match primary outfit color palette (if wearing purple, use complementary metal; if wearing jewel tones, use gold)
- Necklace (if any): Length and material must suit outfit neckline and formality level
- Bindi (if applicable): Color MUST harmonize with outfit color scheme — warm outfit = warm/red tones, cool outfit = blue/purple tones, neutral outfit = gold/jewel tones
- Bindi placement: Must be centered, appropriate to face structure, visible and color-coordinated
- Bracelets: Metal and style must match jewelry/accessories theme (matching earrings tone and formality)
- Overall coherence: All accessories work together as unified styling set, never mismatched metals or clashing colors
- Style consistency: Formal outfit = refined/elegant accessories; casual outfit = simple/approachable accessories; traditional = culturally appropriate styling

TECHNICAL REQUIREMENTS:
Composition: Medium close-up (waist-up), 50mm portrait lens style, eye-level or slight angle
Face Clarity: Sharpest element, fully visible, unobstructed, most detailed
Hands: Anatomically correct, naturally positioned, properly detailed (if visible)
Lighting: Directional but soft, preserving skin texture detail (avoid over-smoothing)
Background: Minimal, blurred, supporting (never competing with face)
Depth: Shallow depth of field isolating face
Skin Texture: Natural with visible pores, no artificial smoothing
Realism: Strict photorealism, no cartoon/stylization

NEGATION INSTRUCTIONS (Critical for AI models):
- Negative: "avoid beautification, avoid face smoothing, avoid skin enhancement, avoid retouching, avoid feature alteration, avoid plastic surgery effects, avoid artificial perfection, avoid Photoshop effects, avoid feature reshaping, avoid identity change, avoid mismatched accessories"

4-LAYER STRUCTURE FOR EACH PROMPT:
Layer 1 (Identity Lock): "Preserve [specific facial feature list] identically from reference image. Do not alter facial structure in any way."
Layer 2 (Composition): "[Scene-specific camera angle], 50mm portrait aesthetic, face sharp and detailed, shallow depth of field"
Layer 3 (Transformation): "[Scene-specific costume/styling/action] with accessories coordinated to outfit colors and style"
Layer 4 (Prohibitions): "Negative prompt: avoid beautification, avoid smoothing, avoid retouching, avoid feature alteration"

SCENE VARIATION MANDATE (CRITICAL FOR DIVERSITY):
⚠️ YOU MUST CREATE {count} PROMPTS WITH COMPLETELY DIFFERENT SCENARIOS
- Each prompt MUST use a different transformation scenario from the list below
- Scenario rotation example (for 3 prompts): Prompt 1=Bride, Prompt 2=Professional, Prompt 3=Casual
- If fewer scenarios needed, cycle through: Bride → Professional → Casual → Party → Cultural → Artistic → Outdoor → Minimalist
- ENFORCE DIVERSITY: Each scenario must have distinct pose, body position, environment, and styling
- VALIDATE BEFORE OUTPUT: Confirm each prompt is visually distinct (different scene context)

SCENE-SPECIFIC TRANSFORMATION SCENARIOS (CHOOSE DIFFERENT ONE FOR EACH PROMPT):

1️⃣ BRIDE/FORMAL WEDDING:
   - Setting: Luxurious wedding venue (bridal suite, garden, hall, decorated space)
   - Pose: Standing confident with deliberate positioning (hand on hip, hand on dress, crossed arms, or elegant hand placement)
   - Body Position: Upright, poised, formal stance showing confidence and elegance
   - Face Angle: Direct to camera with gentle head tilt, or profile/3-quarter angle looking thoughtful
   - Makeup: Full bridal makeup (enhanced eyes, defined brows, lip color, luminous skin)
   - Attire: Wedding dress/bridal wear, embellished/elegant (saree, lehenga, gown, traditional bridal, etc.)
   - Jewelry: Statement bridal jewelry (earrings, necklace, bangles, coordinated with outfit)
   - Hair: Bridal hairstyle (updo, half-up, braided, or with bridal accessories like flowers/tiara)
   - Expression: Radiant, joyful, confident, gentle, romantic
   - Lighting: Warm flattering light, romantic golden hour feel, soft directional light
   - Background: Decorated, elegant, complementary to bridal theme (venue details softly blurred)

2️⃣ PROFESSIONAL/CORPORATE:
   - Setting: Professional environment (office interior, glass background, corporate space, studio)
   - Pose: Power pose or confident seated (leaning on desk, hand on chest, arms crossed confidently, or seated at desk)
   - Body Position: Upright, commanding, formal professional posture
   - Face Angle: Direct eye contact with camera (confident direct gaze) or slight angle showing approachability
   - Makeup: Professional polished makeup (minimal but refined, matte finish, professional colors)
   - Attire: Business formal wear (blazer, suit, professional dress, business casual), well-tailored
   - Jewelry: Minimal professional jewelry (simple earrings, professional watch/bracelet, understated)
   - Hair: Professional neat styling (bun, sleek waves, professional cut, salon-finished)
   - Expression: Confident, professional, commanding, approachable yet authoritative
   - Lighting: Corporate studio lighting (bright, neutral, even, professional headshot aesthetic)
   - Background: Corporate/office elements softly blurred, professional backdrop

3️⃣ CASUAL/RELAXED:
   - Setting: Casual environment (cafe, park bench, relaxed indoor space, casual cafe ambiance)
   - Pose: Relaxed comfortable positioning (leaning against wall, casual seated, relaxed standing, natural arm placement)
   - Body Position: Relaxed, at-ease posture, comfortable and approachable
   - Face Angle: Natural over-shoulder look, slight head tilt, soft angle showing approachability
   - Makeup: Natural minimal makeup (enhanced but fresh-faced, natural tones, effortless look)
   - Attire: Casual comfortable clothing (jeans, casual dress, sweater, relaxed fit, approachable style)
   - Jewelry: Simple casual accessories (minimal earrings, simple bracelet, casual watch if any)
   - Hair: Natural styled hair (loose waves, casual bun, natural texture, undone elegance)
   - Expression: Warm, friendly, genuine smile, relaxed, approachable, natural
   - Lighting: Soft natural or cafe lighting, warm tones, soft shadows, intimate feel
   - Background: Casual setting elements (cafe interior, park, relaxed background slightly blurred)

4️⃣ PARTY/GLAMOROUS EVENT:
   - Setting: Upscale party/event venue (cocktail party, gala, nightclub, celebration space, elegant event)
   - Pose: Dynamic energetic positioning (standing with attitude, hand gesture, confident stance, engaging pose)
   - Body Position: Confident, expressive, dynamic posture showing energy and presence
   - Face Angle: Engaging angle (slightly turned with eye contact over shoulder, or frontal with direct gaze)
   - Makeup: Glamorous bold makeup (dramatic eyes, defined lips, luminous glow, statement makeup)
   - Attire: Evening formal wear (cocktail dress, designer dress, saree, formal gown, glamorous outfit)
   - Jewelry: Statement jewelry (chandelier earrings, bold necklace, multiple bracelets, coordinated ensemble)
   - Hair: Glamorous styling (loose curls, voluminous waves, elegant updo, salon-quality shine)
   - Expression: Confident, radiant, engaging, fun, social, glowing
   - Lighting: Warm flattering light, evening/event lighting with subtle glow, mood lighting
   - Background: Event venue elements (elegant decor, venue details, sophisticated background)

5️⃣ CULTURAL/TRADITIONAL:
   - Setting: Cultural/traditional setting (temple, cultural space, traditional backdrop, culturally appropriate environment)
   - Pose: Respectful traditional positioning (standing gracefully, culturally appropriate gesture, traditional pose elements)
   - Body Position: Graceful, dignified, respectful posture honoring cultural context
   - Face Angle: Direct frontal or slight profile angle, serene and composed expression angle
   - Makeup: Traditional makeup (cultural-appropriate colors, traditional cosmetics, authentic styling)
   - Attire: Traditional cultural dress (authentic regional clothing, cultural attire, traditional styling)
   - Jewelry: Traditional jewelry (cultural-appropriate metals and designs, authentic cultural jewelry, coordinated)
   - Hair: Traditional styling (cultural-appropriate hairstyle, traditional accessories, authentic styling)
   - Expression: Serene, dignified, respectful, culturally-aligned, graceful
   - Lighting: Warm respectful lighting, honoring cultural aesthetics, soft authentic feel
   - Background: Culturally appropriate background (traditional elements, respectful cultural setting)

6️⃣ ARTISTIC/CREATIVE:
   - Setting: Artistic environment (artist studio, creative space, artistic backdrop, gallery-like setting)
   - Pose: Creative expressive positioning (artistic gesture, unique angle, unconventional but flattering pose)
   - Body Position: Expressive, creative posture, artistic and unique positioning
   - Face Angle: Unconventional flattering angle (profile, dramatic angle, artistic angle that showcases creativity)
   - Makeup: Creative artistic makeup (subtle artistic elements, creative colors or techniques, artist-inspired)
   - Attire: Artistic/creative clothing (bohemian wear, artistic style, creative fashion, expressive clothing)
   - Jewelry: Artistic accessories (bohemian jewelry, artistic pieces, creative jewelry, curated collection)
   - Hair: Creative styling (artistic arrangement, textured, unique but flattering, creative hair direction)
   - Expression: Creative, thoughtful, artistic, inspired, unique
   - Lighting: Artistic lighting (dramatic, mood lighting, studio lights creating artistic effect)
   - Background: Artistic elements (studio details, creative backdrop, artistic environment)

7️⃣ OUTDOOR/ADVENTURE:
   - Setting: Outdoor natural setting (garden, nature, outdoor landscape, park, natural backdrop)
   - Pose: Active comfortable outdoor positioning (standing naturally in landscape, active engaged pose, adventure-ready)
   - Body Position: Relaxed active posture, at-ease in natural environment, engaged with setting
   - Face Angle: Natural angle with setting (looking toward landscape, engaged with environment, natural outdoor angle)
   - Makeup: Natural outdoor makeup (fresh-faced, sun-kissed, natural look appropriate for outdoors)
   - Attire: Casual outdoor wear (outdoor clothing, adventure-appropriate, casual sporty or relaxed casual)
   - Jewelry: Minimal nature-friendly accessories (simple jewelry, adventure-appropriate, minimal metal)
   - Hair: Natural outdoor styling (loose, windswept, natural texture, outdoor-appropriate)
   - Expression: Fresh, energized, connection to nature, genuine, outdoor-friendly
   - Lighting: Natural sunlight (golden hour, soft natural light, outdoor natural lighting)
   - Background: Natural outdoor scenery (landscape elements, nature, outdoor environment)

8️⃣ MINIMALIST/MODERN CONTEMPORARY:
   - Setting: Modern minimalist space (clean background, contemporary setting, modern studio, sleek space)
   - Pose: Clean modern positioning (simple elegant stance, contemporary pose, minimal but striking)
   - Body Position: Refined, minimalist posture, clean lines, contemporary elegance
   - Face Angle: Direct contemporary angle (frontal or slight angle, modern portrait aesthetic)
   - Makeup: Minimalist refined makeup (clean lines, modern tones, refined simplicity)
   - Attire: Modern contemporary clothing (minimalist fashion, contemporary outfit, clean lines, modern aesthetic)
   - Jewelry: Minimal modern jewelry (geometric, minimalist pieces, contemporary jewelry, or no jewelry)
   - Hair: Clean modern styling (sleek, minimalist, contemporary cut, modern aesthetic)
   - Expression: Composed, modern, confident, refined, contemporary
   - Lighting: Clean modern lighting (studio light, bright contemporary, clean shadows)
   - Background: Minimalist backdrop (plain or subtle, contemporary, clean modern space)

POSE DIVERSITY ENFORCEMENT:
✓ MANDATORY: Each of {count} prompts MUST have:
  - DIFFERENT body position type (standing vs seated vs leaning vs dynamic)
  - DIFFERENT face angle (frontal vs profile vs 3/4 angle vs over-shoulder)
  - DIFFERENT hand/arm positioning (hands down vs hands active vs hands placed vs arm gesture)
  - DIFFERENT environmental context (indoor vs outdoor, venue type, background style)
  - DIFFERENT pose intent (confident vs relaxed vs energetic vs composed vs graceful)
  - DIFFERENT body language (formal vs casual vs creative vs active vs traditional)

SPECIAL SCENE ROTATION RULE (if {count}=3):
- Prompt 1: Use Bride/Formal Wedding scenario
- Prompt 2: Use Professional/Corporate scenario  
- Prompt 3: Use Casual/Relaxed scenario

SPECIAL SCENE ROTATION RULE (if {count}=6):
- Prompt 1: Bride/Formal Wedding
- Prompt 2: Professional/Corporate
- Prompt 3: Casual/Relaxed
- Prompt 4: Party/Glamorous Event
- Prompt 5: Cultural/Traditional
- Prompt 6: Artistic/Creative

INSTRUCTIONS FOR PROMPT GENERATION:
- Create {count} DISTINCT transformation prompts (each 100-160 words, compressed/dense)
- ENFORCE THE SCENE ROTATION (mandatory scenario assignment per prompt above)
- EACH PROMPT MUST START with explicit facial feature preservation statement
- EACH PROMPT MUST SPECIFY THE SCENE SCENARIO being used (e.g., "Bride Scenario: wedding formal attire")
- EACH PROMPT MUST INCLUDE accessory-outfit coordination specifics
- EACH PROMPT MUST SPECIFY different pose, body position, and face angle than other prompts
- EACH PROMPT MUST SPECIFY different environmental context than other prompts
- EACH PROMPT MUST END with explicit "Negative: [forbidden list]"
- Use direct language, minimize explanation, maximize clarity
- Repeat identity anchors 2-3 times in different forms for redundancy
- Order: Facial Preservation (most emphasized) → Composition → Scene → Negatives
- Test prompts work on DALL-E 3, Midjourney, Stable Diffusion
- CRITICAL VALIDATION: Before returning JSON, verify each prompt uses a different scenario and has distinct pose/position/environment

SPECIAL INSTRUCTION FOR REFERENCE-BASED TRANSFORMATIONS:
- Every transformation shares the EXACT SAME FACE (facial features immutable)
- Face angle/pose/expression: OPTIMIZE per scene (never locked, varies by scenario)
- Body position/clothing/environment/styling: COMPLETELY NEW AND UNIQUE per scene
- The person must be recognizable across all transformations by facial features alone
- But the scenes, poses, environments, and styling must be VISUALLY DISTINCT and different

Return ONLY valid JSON (no markdown, no text before/after):
{{
  "prompts": [
    {{"prompt": "<compressed 100-160 word prompt with identity lock, accessory-outfit coordination, and negatives>", "scene": "<transformation type>"}}
  ],
  "analysis": "Facial preservation strategy, identity anchors, and accessory coordination approach used",
  "tip": "Identity lock + accessory harmony technique: [specific method for preserving face and coordinating styling]"
}}"""
        elif category == "design_gifts":
            # Specialized template for gift design with optional reference image support
            if reference_image_text:
                # Reference-based personalized gift design (e.g., couple in design)
                prompt = f"""You are an expert AI design prompt engineer specializing in personalized gift designs using reference images.

Category: {category_desc}{niche_line}{context_line}

REFERENCE IMAGE USAGE:
- PRESERVE (identical to reference): Facial features, appearance, physical characteristics, identity
- VARY/CHANGE (different for each prompt): Costumes, styling, clothing, hairstyle, makeup, accessories, jewelry
- MAINTAIN RECOGNIZABILITY: People must remain clearly identifiable but in different outfit/styling contexts

Gift Design with Reference Requirements:
- Create {count} distinct, creative gift design concepts incorporating the reference image
- Each prompt should be optimized for DALL-E 3, Midjourney, or Stable Diffusion
- Designs should be printable on merchandise (mugs, t-shirts, posters, art prints, etc.)
- Preserve facial identity while varying costumes/styling creatively for each design variation
- CRITICAL: DO NOT use the same costume/clothing across prompts — each design needs DIFFERENT outfits and styles

For each design prompt, include:
1. CONCEPT: Design theme and emotional appeal with reference integration
2. VISUAL STYLE: Specific artistic direction (watercolor, digital illustration, modern vector, etc.)
3. COMPOSITION: How reference people integrate with design elements
4. COLOR SCHEME: Specific colors or palettes suited for the gift and reference
5. TEXT/TYPOGRAPHY: Personalized text, calligraphy, or messaging integrated elegantly
6. COSTUME/STYLING: UNIQUE outfit and styling appropriate to the design concept (NOT from reference, DIFFERENT in each prompt)
7. DECORATIVE ELEMENTS: Supporting design elements that complement reference and costume
8. CONTEXT: Where/how this design would be used (mug, t-shirt, poster, canvas print, etc.)

Instructions:
- Create {count} DISTINCT personalized gift design prompts (each ~140-200 words)
- Emphasize reference facial identity preservation with VARIED costumes and creative styling
- **COSTUME DIFFERENTIATION (MANDATORY)**: Prompt 1 costume style MUST be completely different from Prompt 2, which MUST be different from Prompt 3, etc.
  * Example: If Prompt 1 uses formal/elegant attire → Prompt 2 must use casual/relaxed clothing → Prompt 3 must use traditional/cultural or themed clothing
  * NEVER repeat similar outfit styles, color schemes, or clothing types across different prompts
  * Each design gets its own distinct costume identity
- Facial features, appearance, and identity MUST remain consistent and recognizable across all prompts
- Each must be production-ready for print on demand with high resolution
- Vary design themes, scenes, outfits, text placements, and decorative approaches creatively
- Ensure reference people remain clearly identifiable in all prompts despite outfit changes
- Choose outfit styles that naturally fit each design's unique theme and context

Return ONLY valid JSON (no markdown, no extra text):
{{
  "prompts": [
    {{"prompt": "<design prompt with reference integration and UNIQUE creative OUTFIT for each, 140-200 words>", "scene": "<design theme>"}}
  ],
  "tip": "<actionable tip for personalized gift designs with consistent identity but varied creative styling>"
}}"""
            else:
                # Standard text-based gift design (no reference image)
                prompt = f"""You are an expert AI design prompt engineer specializing in personalized gift designs and merchandise.

Category: {category_desc}{niche_line}{context_line}

Gift Design Requirements:
- Create {count} distinct, creative gift design concepts
- Each prompt should be optimized for DALL-E 3, Midjourney, or Stable Diffusion
- Designs should be printable on merchandise (mugs, t-shirts, posters, etc.)
- Include specific style guidance (modern, vintage, minimalist, ornate, etc.)
- Consider personalization elements that make the gift unique and meaningful

For each design prompt, include:
1. CONCEPT: What the design represents and its emotional appeal
2. VISUAL STYLE: Specific artistic direction (e.g., watercolor, digital illustration, 3D render)
3. COMPOSITION: Layout, focal point, use of space
4. COLOR SCHEME: Specific colors or palettes suited for the gift
5. DETAILS: Specific elements, patterns, typography, or decorative features
6. CONTEXT: Where/how this design would be used (mug, shirt, poster, etc.)
7. PERSONALIZATION: How it could be customized for the recipient

Instructions:
- Create {count} DISTINCT gift design prompts (each ~100-150 words)
- Each must be production-ready for print on demand
- Include quality indicators (high resolution, professional finish)
- Consider both aesthetic appeal and printability
- Vary designs across prompts to offer different style options

Return ONLY valid JSON (no markdown, no extra text):
{{
  "prompts": [
    {{"prompt": "<design prompt optimized for image generation>", "scene": "<gift type/style>"}}
  ],
  "tip": "<actionable tip for best gift design results>"
}}"""
        else:
            # Standard template for non-transformation, non-gift categories
            prompt = f"""You are an expert AI image generation prompt engineer creating CONCISE, ready-to-use prompts.

Category: {category_desc}{niche_line}{context_line}

Instructions:
- Create {count} distinct, complementary prompts (each ~100-150 words max)
- Each must work directly in DALL-E 3, Midjourney, or Stable Diffusion
- NO generic filler — be specific about scene, mood, lighting, style
- Vary settings/angles across prompts

IMPORTANT: Keep prompts CONCISE and focused on visual elements.

Return ONLY valid JSON (no markdown, no extra text):
{{
  "prompts": [
    {{"prompt": "<full ready-to-use prompt, 100-150 words>", "scene": "<3-5 word scene label>"}}
  ],
  "tip": "<one actionable tip for best results>"
}}"""

        cache_key = self._make_cache_key(
            "generate_image_prompts",
            niche=niche,
            action=category,
            topic=user_context_safe[:50] if user_context_safe else str(count),  # Include custom prompt content to prevent cache collision
        )
        # NO CACHE for custom prompts — user wants fresh generation each time
        cache_ttl = None if user_context_safe else 24  # Custom prompts: no cache; standard: 24h cache
        return self._call_groq_with_fallback(
            command="generate_image_prompts",
            cache_key=cache_key,
            prompt=prompt,
            chat_id=chat_id,
            temperature=temperature if temperature is not None else 0.8,
            ttl_hours=cache_ttl,
        )

    def enhance_prompts_with_professional_structure(
        self,
        prompts_response: dict,
        category: str,
        apply_professional_secrets: bool = True
    ) -> dict:
        """
        Enhance AI-generated prompts with professional structure validation and quality improvements.
        
        This method integrates the professional 12-component framework to:
        1. Validate that prompts include all essential components
        2. Inject professional secrets (cinematic lighting, emotional expression, etc.)
        3. Calculate quality scores
        4. Provide enhancement recommendations
        
        M4 FIX: Uses caching to avoid reprocessing the same prompts multiple times
        
        Args:
            prompts_response: The JSON response from generate_image_prompts containing "prompts" array
            category: Category of prompts (e.g., 'portrait_transformation', 'design_gifts')
            apply_professional_secrets: Whether to inject professional secrets into prompts
            
        Returns:
            Enhanced response with professional structure metadata and quality improvements
        """
        # M4 FIX: Initialize cache for enhancement results if not already present
        if not hasattr(self, '_enhancement_cache'):
            self._enhancement_cache = {}
        
        # C2: Improve error handling - don't silently fail
        try:
            from src.prompts.professional_prompt_enhancer import ProfessionalPromptEnhancer
            enhancer_available = True
        except ImportError as e:
            logger.error(f"[ERROR C2] Professional prompt enhancer import failed: {e}")
            logger.warning("[WARN] Prompts will not be enhanced with professional structure. Quality scores unavailable.")
            enhancer_available = False
        
        if not isinstance(prompts_response, dict) or "prompts" not in prompts_response:
            return prompts_response
        
        prompts_list = prompts_response.get("prompts", [])
        
        # If enhancer is not available, add metadata flag and return with warning
        if not enhancer_available:
            logger.warning(f"[WARN C2] Processing {len(prompts_list)} prompts WITHOUT professional enhancement")
            for prompt_item in prompts_list:
                if isinstance(prompt_item, dict):
                    prompt_item["professional_enhancement_status"] = "failed_import"
                    prompt_item["quality_score"] = None
                    prompt_item["enhancement_note"] = "Professional enhancer unavailable - quality score missing"
            return prompts_response
        
        enhancer = ProfessionalPromptEnhancer()
        enhanced_prompts = []
        quality_scores = []
        
        # L6 FIX: Track comprehensive batch statistics
        batch_stats = {
            "total_prompts": len(prompts_list),
            "cache_hits": 0,
            "cache_misses": 0,
            "processing_times_ms": [],
            "skipped_prompts": 0,
            "secrets_found_counts": {secret: 0 for secret in ["cinematic_lighting", "realistic_skin_textures", "emotional_expression", "color_grading", "professional_camera_language", "storytelling_atmosphere"]}
        }
        
        for prompt_item in prompts_list:
            if not isinstance(prompt_item, dict) or "prompt" not in prompt_item:
                enhanced_prompts.append(prompt_item)
                batch_stats["skipped_prompts"] += 1
                continue
            
            original_prompt = prompt_item["prompt"]
            
            # M4 FIX: Check cache before enhancing
            cache_key = hashlib.sha256(f"{category}:{original_prompt}".encode()).hexdigest()
            prompt_start_time = time.time()
            
            if cache_key in self._enhancement_cache:
                # Use cached enhancement result
                enhancement_result = self._enhancement_cache[cache_key]
                batch_stats["cache_hits"] += 1
                logger.debug(f"[CACHE] Cache hit for prompt (category={category}, cache_size={len(self._enhancement_cache)})")
            else:
                # Enhance with professional structure
                enhancement_result = enhancer.enhance_prompt_with_structure(
                    original_prompt,
                    category,
                    professional_secrets=None  # L3 FIX: Renamed from professional_secrets_to_embed
                )
                batch_stats["cache_misses"] += 1
                
                # M4 FIX: Store in cache (limit cache size to 1000 entries to prevent memory bloat)
                if len(self._enhancement_cache) >= 1000:
                    # Remove oldest entry (FIFO)
                    oldest_key = next(iter(self._enhancement_cache))
                    del self._enhancement_cache[oldest_key]
                
                self._enhancement_cache[cache_key] = enhancement_result
            
            # L6 FIX: Track processing time per prompt
            prompt_processing_time = int((time.time() - prompt_start_time) * 1000)
            batch_stats["processing_times_ms"].append(prompt_processing_time)
            
            # L6 FIX: Track which secrets were found
            for secret, found in enhancement_result["professional_secrets_found"].items():
                if found:
                    batch_stats["secrets_found_counts"][secret] += 1
            
            # Create enhanced prompt item
            enhanced_item = {
                **prompt_item,
                "professional_structure": {
                    "components_found": enhancement_result["component_analysis"],
                    "professional_secrets_found": enhancement_result["professional_secrets_found"],
                    "quality_score": enhancement_result["quality_score"],
                    "completeness_notes": enhancement_result["enhancement_suggestions"].get("notes", [])
                }
            }
            
            # Apply professional secrets if requested
            if apply_professional_secrets and enhancement_result["enhancement_suggestions"].get("enhanced_prompt"):
                enhanced_item["prompt_enhanced"] = enhancement_result["enhancement_suggestions"]["enhanced_prompt"]
            
            enhanced_prompts.append(enhanced_item)
            quality_scores.append(enhancement_result["quality_score"])
        
        # Calculate average quality score and comprehensive batch statistics
        avg_quality_score = (sum(quality_scores) / len(quality_scores)) if quality_scores else 0
        cache_hit_rate = (batch_stats["cache_hits"] / batch_stats["total_prompts"] * 100) if batch_stats["total_prompts"] > 0 else 0
        avg_processing_time = (sum(batch_stats["processing_times_ms"]) / len(batch_stats["processing_times_ms"])) if batch_stats["processing_times_ms"] else 0
        
        # Log comprehensive batch statistics
        logger.info(
            f\"[BATCH STATS L6] Processed {batch_stats['total_prompts']} prompts in category '{category}': \"\n                f\"cache_hit_rate={cache_hit_rate:.1f}% ({batch_stats['cache_hits']}/{batch_stats['total_prompts']}), \"\n                f\"avg_quality_score={avg_quality_score:.1f}, \"\n                f\"avg_processing_time={avg_processing_time:.0f}ms\"\n        )
        
        # Return enhanced response with L6 comprehensive batch statistics
        return {
            **prompts_response,
            "prompts": enhanced_prompts,
            "professional_structure_metadata": {
                "category": category,
                "average_quality_score": round(avg_quality_score, 1),
                "enhanced": True,
                "enhancement_date": datetime.now().isoformat(),
                "professional_secrets_applied": apply_professional_secrets,
                # L6 FIX: Comprehensive batch statistics
                "batch_statistics": {
                    "total_prompts_processed": batch_stats["total_prompts"],
                    "skipped_prompts": batch_stats["skipped_prompts"],
                    "cache_hits": batch_stats["cache_hits"],
                    "cache_misses": batch_stats["cache_misses"],
                    "cache_hit_rate_percent": round(cache_hit_rate, 1),
                    "average_processing_time_ms": round(avg_processing_time, 1),
                    "min_processing_time_ms": min(batch_stats["processing_times_ms"]) if batch_stats["processing_times_ms"] else 0,
                    "max_processing_time_ms": max(batch_stats["processing_times_ms"]) if batch_stats["processing_times_ms"] else 0,
                    "secrets_distribution": batch_stats["secrets_found_counts"]
                }
            }
        }

    def generate_design_brief(
        self,
        category: str = "design_posters",
        user_input: str = "",
        niche: str = "",
        brand_context: dict = None,
        chat_id: int = None,
    ) -> dict:
        """Generate comprehensive design briefs from user input — 3 creative variations."""
        from src.prompts.templates import DESIGN_BRIEF_SYSTEM_PROMPT
        
        if brand_context is None:
            brand_context = {}

        niche_line = f"\nBrand/Niche: {niche}" if niche else ""
        brand_line = f"\nBrand context: {brand_context}" if brand_context else ""

        # Build combined prompt (system instructions + user request)
        prompt = f"""{DESIGN_BRIEF_SYSTEM_PROMPT}

---

Design Category: {category.replace("_", " ").title()}

User's Design Concept:
{user_input}{niche_line}{brand_line}

Create 3 distinct, professional design brief variations that incorporate ALL of the user's content and messaging.

Each variation should be a complete, ready-to-brief design brief that a designer can execute immediately."""

        cache_key = self._make_cache_key(
            "generate_design_brief",
            category=category,
            niche=niche,
        )
        
        # NO CACHE for custom design briefs — user wants fresh generation each time
        cache_ttl = None if user_input and user_input.strip() else 24
        result = self._call_groq_with_fallback(
            command="generate_design_brief",
            cache_key=cache_key,
            prompt=prompt,
            chat_id=chat_id,
            temperature=0.85,
            ttl_hours=cache_ttl,
        )

        # Parse and structure response
        if result and isinstance(result, dict):
            if "error" in result:
                return result
            
            # Extract briefs from response
            briefs = result.get("briefs", [])
            if briefs:
                return {
                    "status": "success",
                    "brief": result,
                    "sections": [b.get("title", f"Brief {i+1}") for i, b in enumerate(briefs)],
                    "total_sections": len(briefs),
                }
        
        return result

    def generate_gift_design_concepts(
        self,
        product_type: str,
        concept_idea: str,
        personalization: dict = None,
        chat_id: int = None,
        niche: str = "",
    ) -> dict:
        """Generate 3 gift design concepts with briefs + AI image generation prompts."""
        from src.prompts.templates import GIFT_DESIGN_SYSTEM_PROMPT, get_gift_product_meta

        if personalization is None:
            personalization = {}

        product_meta = get_gift_product_meta(product_type)
        
        # Build personalization context
        brand_colors_str = ""
        if personalization.get("brand_colors"):
            brand_colors_str = f"\nBrand colors: {', '.join(personalization['brand_colors'])}"
        
        tone_str = ""
        if personalization.get("tone"):
            tone = personalization["tone"]
            tone_desc = personalization.get("tone_description", "")
            tone_str = f"\nDesign tone: {tone.title()} ({tone_desc})" if tone_desc else f"\nDesign tone: {tone.title()}"
        
        occasion_str = f"\nOccasion: {personalization.get('occasion', '').title()}" if personalization.get("occasion") else ""
        recipient_str = f"\nRecipient type: {personalization.get('recipient_type', '').title()}" if personalization.get("recipient_type") else ""

        # Build combined prompt
        prompt = f"""{GIFT_DESIGN_SYSTEM_PROMPT}

---

PRODUCT: {product_type.replace("_", " ").title()}
Specifications:
- Printable Area: {product_meta.get("printable_area")}
- Constraints: {product_meta.get("constraints")}

USER'S CONCEPT: {concept_idea}{brand_colors_str}{tone_str}{occasion_str}{recipient_str}

Create 3 DISTINCT, production-ready gift design concepts that incorporate ALL of the user's messaging and preferences.
Each concept should include a design brief and 2 image generation prompts (DALL-E 3 + Midjourney optimized).
All prompts must be ready to paste directly into image generation tools."""

        cache_key = self._make_cache_key(
            "generate_gift_design",
            product_type=product_type,
            tone=personalization.get("tone", ""),
            occasion=personalization.get("occasion", ""),
            niche=niche,
        )

        # NO CACHE for custom gift designs — user wants fresh generation each time
        cache_ttl = None if concept_idea and concept_idea.strip() else 24
        result = self._call_groq_with_fallback(
            command="generate_gift_design_concepts",
            cache_key=cache_key,
            prompt=prompt,
            chat_id=chat_id,
            temperature=0.85,
            ttl_hours=cache_ttl,
        )

        # Parse and structure response
        if result and isinstance(result, dict):
            if "error" in result:
                return result

            concepts = result.get("concepts", [])
            if concepts:
                return {
                    "status": "success",
                    "concepts": concepts,
                    "concept_count": len(concepts),
                    "product_type": product_type,
                    "design_tip": "Each concept includes a design brief and two image generation prompts ready for DALL-E 3 or Midjourney.",
                }

        return result

    def monetization_ideas(
        self,
        niche: str,
        follower_count: int,
        engagement_rate: float = None,
        content_type: str = "",
        region: str = "",
        chat_id: int = None,
    ) -> dict:
        """Suggest the most suitable monetization strategies for this specific account."""
        ctx_lines = [f"- Niche: {niche}", f"- Followers: {follower_count:,}"]
        if engagement_rate:
            ctx_lines.append(f"- Estimated engagement rate: {engagement_rate:.1%}")
        if content_type:
            ctx_lines.append(f"- Primary content type: {content_type}")
        if region:
            ctx_lines.append(f"- Market region: {region}")
        context_block = "\n".join(ctx_lines)

        prompt = f"""You are an Instagram monetization strategist.

Account context:
{context_block}

Suggest the most suitable monetization strategies for this specific account. Identify which revenue streams genuinely fit this niche and audience size — do not default to a fixed list. All revenue projections should reflect realistic ranges for this specific niche and market, not arbitrary numbers.

Include:
- Recommended revenue streams (only those that genuinely fit this niche and size)
- Realistic revenue projections per stream (range based on niche market rates)
- Implementation priority and timeline
- Partner types and platforms best suited to this niche
- Pricing recommendations for this market
- Success metrics relevant to this niche

Format as JSON."""

        cache_key = self._make_cache_key(
            "monetization_ideas", niche=niche, account_stage="", region=region,
        )
        result = self._call_groq_with_fallback(
            command="monetization_ideas", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.7, ttl_hours=24,
        )
        if result and "error" not in result:
            logger.info("[OK] Generated monetization ideas for %s+ followers", follower_count)
        return result

    # ─────────────────────────────────────────────────────────────────────
    #  Phase 4 — new AI methods (all inject user-profile context)
    # ─────────────────────────────────────────────────────────────────────

    def _profile_ctx(self, niche: str = "", audience_size: str = "", goals: list = None) -> str:
        """Build a short profile-context string to inject into every system prompt."""
        parts = []
        if niche:
            parts.append(f"niche: {niche}")
        if audience_size:
            parts.append(f"audience size: {audience_size}")
        if goals:
            parts.append(f"goals: {', '.join(goals)}")
        return f" The user's Instagram profile — {'; '.join(parts)}." if parts else ""

    def caption_generator(self, post_description: str, niche: str = "",
                          audience_size: str = "", chat_id: int = None) -> dict:
        """Generate a viral Instagram caption with CTA and hashtags."""
        ctx = self._profile_ctx(niche=niche, audience_size=audience_size)
        prompt = f"""You are an expert Instagram copywriter.{ctx}

Write a viral Instagram caption for this post:
\"{post_description}\"

Return JSON with exactly these keys:
- caption: the full caption text (hook + story + CTA, max 2200 chars)
- hook: the opening line (max 15 words, no emoji)
- cta: call-to-action sentence
- hashtags: list of 10 targeted hashtags (no # prefix)
- estimated_reach: low/medium/high"""

        cache_key = self._make_cache_key(
            "caption_generator", niche=niche, action=post_description[:40],
        )
        return self._call_groq_with_fallback(
            command="caption_generator", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.8,
        )

    def hashtag_pack(self, topic: str, niche: str = "", chat_id: int = None) -> dict:
        """Return hashtags in 3 tiers for a given topic."""
        ctx = self._profile_ctx(niche=niche)
        prompt = f"""You are an Instagram hashtag strategist.{ctx}

Generate a hashtag pack for the topic: \"{topic}\"

Return JSON with exactly these keys:
- broad: list of high-reach hashtags (1M+ posts, no # prefix)
- niche: list of mid-range hashtags (100K–1M posts, no # prefix)
- micro: list of micro/specific hashtags (<100K posts, no # prefix)
- tip: one-sentence usage tip"""

        cache_key = self._make_cache_key("hashtag_pack", niche=niche, topic=topic)
        return self._call_groq_with_fallback(
            command="hashtag_pack", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.6,
        )

    def bio_optimizer(self, current_bio: str, niche: str = "", goals: list = None,
                      chat_id: int = None) -> dict:
        """Rewrite an Instagram bio: hook + value prop + CTA."""
        ctx = self._profile_ctx(niche=niche, goals=goals or [])
        prompt = f"""You are an Instagram profile expert.{ctx}

Rewrite this Instagram bio to maximise follows and profile visits:
\"{current_bio}\"

Return JSON with exactly these keys:
- rewritten_bio: the new bio text (max 150 chars)
- hook: opening line that grabs attention
- value_prop: what the audience gets from following
- cta: call-to-action (e.g. "DM for collabs ↓")
- keywords: list of 5 SEO keywords included in the bio
- char_count: character count of rewritten_bio"""

        cache_key = self._make_cache_key("bio_optimizer", niche=niche, action=current_bio[:40])
        return self._call_groq_with_fallback(
            command="bio_optimizer", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.7, ttl_hours=48,
        )

    def content_calendar(self, niche: str = "", audience_size: str = "",
                         chat_id: int = None) -> dict:
        """Generate a 7-post weekly content calendar."""
        ctx = self._profile_ctx(niche=niche, audience_size=audience_size)
        prompt = f"""You are an Instagram content strategist.{ctx}

Create a 7-post weekly content calendar for an Instagram account.

Return JSON with exactly these keys:
- week_theme: an overarching theme for the week (max 10 words)
- posts: list of 7 objects, one per day, each with:
    - day: Monday/Tuesday/…/Sunday
    - format: Reel | Carousel | Story | Static Post
    - topic: specific post topic (max 10 words)
    - caption_angle: hook or emotional angle (max 15 words)
    - hashtag_theme: 1-word hashtag cluster to use
    - best_time: posting time e.g. "7:00 PM"
- pro_tip: one actionable insight for the week"""

        cache_key = self._make_cache_key("content_calendar", niche=niche)
        return self._call_groq_with_fallback(
            command="content_calendar", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.75,
        )

    def posting_schedule(self, niche: str = "", audience_size: str = "",
                         chat_id: int = None) -> dict:
        """Return best posting times and a weekly schedule."""
        ctx = self._profile_ctx(niche=niche, audience_size=audience_size)
        prompt = f"""You are an Instagram growth expert.{ctx}

Recommend the optimal posting schedule.

Return JSON with exactly these keys:
- best_times: list of objects each with time (e.g. "8:00 AM IST"), day_type (weekday/weekend), reason (max 15 words)
- weekly_schedule: object mapping Monday–Sunday to a recommended format (Reel/Carousel/Story/Rest)
- frequency: recommended posts per week (integer)
- timezone_note: note about audience timezone assumptions
- pro_tip: one sentence on timing strategy"""

        cache_key = self._make_cache_key("posting_schedule", niche=niche)
        return self._call_groq_with_fallback(
            command="posting_schedule", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.6, ttl_hours=48,
        )

    def story_ideas(self, topic: str, niche: str = "", chat_id: int = None) -> dict:
        """Generate interactive Instagram Story ideas."""
        ctx = self._profile_ctx(niche=niche)
        prompt = f"""You are an Instagram Stories expert.{ctx}

Generate interactive Instagram Story ideas for the topic: \"{topic}\"

Return JSON with exactly these keys:
- stories: list of objects each with:
    - type: Poll | Quiz | Countdown | Slider | Question Box | This or That
    - title: Story slide title (max 8 words)
    - prompt: the interactive question or text shown to viewers (max 20 words)
    - engagement_tip: one line on why this drives engagement
- hook_tip: one tip for the first Story slide to maximise retention"""

        cache_key = self._make_cache_key("story_ideas", niche=niche, topic=topic)
        return self._call_groq_with_fallback(
            command="story_ideas", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.8,
        )

    def profile_audit(self, niche: str = "", audience_size: str = "",
                      goals: list = None, chat_id: int = None) -> dict:
        """Return an Instagram profile improvement checklist."""
        ctx = self._profile_ctx(niche=niche, audience_size=audience_size, goals=goals or [])
        prompt = f"""You are an Instagram growth auditor.{ctx}

Perform an advisory profile audit and provide actionable recommendations.

Return JSON with exactly these keys:
- score: estimated profile health score 0–100 (integer) based on typical accounts in this niche
- checklist: list of objects each with:
    - area: Bio | Highlights | Feed Aesthetic | Posting Frequency | Hashtag Strategy | Engagement
    - status: Good | Needs Work | Critical
    - finding: what to look for (max 20 words)
    - action: specific improvement step (max 20 words)
- quick_wins: list of 3 things to do this week for fastest growth
- note: disclaimer that this is advisory without seeing the actual account"""

        cache_key = self._make_cache_key("profile_audit", niche=niche)
        return self._call_groq_with_fallback(
            command="profile_audit", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.65, ttl_hours=48,
        )

    def chat_response(self, user_message: str, profile: dict = None) -> str:
        """Return a conversational Instagram growth answer for free-text messages.

        Injects the user's saved profile as system context so every response
        is personalised without the user having to re-state their niche each time.
        """
        profile = profile or {}
        niche = profile.get("niche", "")
        audience_size = profile.get("audience_size", "")
        goals = profile.get("goals", [])
        chat_id = profile.get("chat_id")
        ctx = self._profile_ctx(niche=niche, audience_size=audience_size, goals=goals)

        system = (
            "You are an expert Instagram growth coach. Give concise, actionable advice. "
            "Use plain text — no markdown headers, no bullet stars. Keep replies under 300 words."
            + ctx
        )
        start = time.time()
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=400,
            )
            duration = time.time() - start
            latency_ms = int(duration * 1000)
            if METRICS_ENABLED:
                metrics.record_api_call(model=self.model, duration=duration, success=True, prompt_length=len(user_message))
                health_check.record_success()
            answer = resp.choices[0].message.content.strip()
            if PROMPT_LOG_ENABLED:
                _plog.log_prompt_response(
                    command="chat_response",
                    prompt_hash=self._make_cache_key("chat_response", action=user_message[:50]),
                    prompt_text=user_message,
                    response_json=json.dumps({"reply": answer}),
                    success=1, latency_ms=latency_ms, model=self.model, chat_id=chat_id,
                )
            return answer
        except Exception as e:
            logger.error(f"chat_response error: {e}")
            if METRICS_ENABLED:
                metrics.record_api_call(model=self.model, duration=time.time()-start, success=False)
                health_check.record_error()
            if PROMPT_LOG_ENABLED:
                _plog.log_prompt_response(
                    command="chat_response",
                    prompt_hash=self._make_cache_key("chat_response", action=user_message[:50]),
                    prompt_text=user_message, response_json=None,
                    success=0, error_msg=str(e),
                    latency_ms=int((time.time() - start) * 1000),
                    model=self.model, chat_id=chat_id,
                )
            return "Sorry, I couldn't process that. Please try again."

    # ── New AI methods (Phase 1 additions) ──────────────────────────────────

    def get_engagement_action(
        self,
        action: str,
        niche: str = "",
        follower_count: int = None,
        region: str = "",
        chat_id: int = None,
        **kwargs,
    ) -> dict:
        """AI-powered response for a specific engagement action.

        Actions: growth_tips | hashtag_strategy | posting_schedule |
                 comment_templates | strategies
        """
        ctx_lines = []
        if niche:
            ctx_lines.append(f"- Niche: {niche}")
        if follower_count:
            ctx_lines.append(f"- Followers: {follower_count:,}")
        if region:
            ctx_lines.append(f"- Region: {region}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "- General Instagram account"

        action_prompts = {
            "growth_tips": f"""You are an Instagram growth expert.

Account context:
{context_block}

Provide the most impactful growth tips for this specific account. Prioritise by expected impact. All numbers, frequencies, and content ratios should be reasoned from the niche and account stage — do not use generic defaults.

Return JSON with:
- tips: list of tip objects, each with: priority, tip (title), detail (specific actionable guidance for this niche), impact (expected outcome explained), effort_level""",

            "hashtag_strategy": f"""You are an Instagram hashtag strategist.

Account context:
{context_block}

Design a complete hashtag strategy for this account. Determine the optimal tier breakdown, quantities, and rotation approach based on the niche competition and account size — do not default to a fixed split.

Return JSON with:
- strategy: object with breakdown (tiers with counts and reach ranges appropriate for this niche), rotation_approach, research_method, best_practices
- niche_specific_tips: tips specific to hashtag use in the {niche or 'this'} niche""",

            "posting_schedule": f"""You are an Instagram scheduling expert.

Account context:
{context_block}

Recommend an optimal posting schedule for this specific account. Base timing on the niche audience's behaviour and the target region — do not use generic peak hours.

Return JSON with:
- schedule: list of time slots with time, timezone, day_type (weekday/weekend), reason (why this time for this audience)
- frequency: recommended posts per day with reasoning
- content_format_rotation: which formats to use on which days
- note: any important caveats about testing and adjusting""",

            "comment_templates": f"""You are an Instagram engagement specialist.

Account context:
{context_block}

Write comment templates specifically for the {niche or 'this'} niche. Templates should feel genuine and niche-appropriate — not generic. Include guidance on personalising each one.

Return JSON with:
- templates: object with categories (e.g., praise, question, relatable, call_to_action) — each with niche-specific template strings
- personalization_guide: how to adapt these templates to feel authentic
- engagement_rules: guidelines for effective commenting in this specific niche""",

            "strategies": f"""You are an Instagram growth strategist.

Account context:
{context_block}

Provide comprehensive engagement strategies tailored to this account. All metrics and expected outcomes should reflect realistic performance for this specific niche and account stage.

Return JSON with:
- strategies: list of strategy objects, each with: name, description, how_to_implement, expected_impact (reasoned for this niche), effort_level, time_investment
- priority_order: which strategy to tackle first and why
- 30_day_roadmap: phased approach for the first month""",
        }

        prompt = action_prompts.get(action)
        if not prompt:
            return {"error": f"Unknown engagement action: {action}"}

        cache_key = self._make_cache_key(
            "get_engagement_action", niche=niche, action=action, region=region,
        )
        return self._call_groq_with_fallback(
            command="get_engagement_action", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.7, ttl_hours=48,
        )

    def generate_analytics_report(
        self,
        report_type: str = "daily",
        niche: str = "",
        follower_count: int = None,
        account_stage: str = "",
        content_mix: dict = None,
        region: str = "",
        chat_id: int = None,
    ) -> dict:
        """Generate an AI-estimated analytics report from account profile context."""
        ctx_lines = [f"- Report type: {report_type}"]
        if niche:
            ctx_lines.append(f"- Niche: {niche}")
        if follower_count:
            ctx_lines.append(f"- Current followers: {follower_count:,}")
        if account_stage:
            ctx_lines.append(f"- Account stage: {account_stage}")
        if region:
            ctx_lines.append(f"- Region: {region}")
        if content_mix:
            ctx_lines.append(f"- Content mix: {json.dumps(content_mix)}")
        context_block = "\n".join(ctx_lines)
        period_map = {"daily": "past 24 hours", "weekly": "past 7 days", "monthly": "past 30 days"}
        period = period_map.get(report_type, "past 24 hours")

        prompt = f"""You are an Instagram analytics expert.

Account context:
{context_block}

Generate a realistic {report_type} analytics report for this account covering the {period}. Base all estimates on what is typical for accounts of this size, niche, and stage. Do not use generic fixed numbers — reason from the specific context provided.

Return JSON with:
- report_type: "{report_type}"
- period: "{period}"
- metrics: realistic estimated metrics for this account (new_followers, engagement_rate, reach, impressions, saves, shares, comments — values should be plausible for this niche/size/stage)
- top_performing_content: what format and topic type likely performs best for this niche
- insights: list of data-driven observations specific to this niche and account stage
- growth_trajectory: honest assessment of the growth path if current strategy is maintained
- recommendations: prioritised list of actions to improve performance
- note: AI-estimated projections based on account profile — connect real analytics for precise data"""

        cache_key = self._make_cache_key(
            "generate_analytics_report", niche=niche,
            account_stage=account_stage, region=region, action=report_type,
        )
        return self._call_groq_with_fallback(
            command="generate_analytics_report", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.6, ttl_hours=12,
        )

    def project_monetization(
        self,
        niche: str = "",
        follower_count: int = None,
        engagement_rate: float = None,
        content_type: str = "",
        region: str = "",
        chat_id: int = None,
    ) -> dict:
        """Generate AI-reasoned monetization projections for the account."""
        ctx_lines = []
        if niche:
            ctx_lines.append(f"- Niche: {niche}")
        if follower_count:
            ctx_lines.append(f"- Followers: {follower_count:,}")
        if engagement_rate:
            ctx_lines.append(f"- Estimated engagement rate: {engagement_rate:.1%}")
        if content_type:
            ctx_lines.append(f"- Primary content type: {content_type}")
        if region:
            ctx_lines.append(f"- Market region: {region}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "- General Instagram creator"

        prompt = f"""You are an Instagram monetization strategist.

Account context:
{context_block}

Provide a detailed monetization analysis. Identify the revenue streams most suited to this niche and account stage — do not default to a fixed list. All revenue estimates should reflect realistic ranges for this specific niche and market.

Return JSON with:
- recommended_streams: list of revenue stream objects suited to this account, each with:
    name, why_it_fits (specific to this niche), monthly_revenue_range (realistic low-high for this account size/niche), implementation_steps, time_to_first_revenue
- streams_to_avoid: list of streams not suited to this account with reasons
- priority_order: which stream to start with and why
- monthly_projection_total: combined realistic monthly revenue range
- 90_day_roadmap: step-by-step monetization plan
- note: Projections are AI estimates based on account profile — actual results depend on execution and audience quality"""

        cache_key = self._make_cache_key(
            "project_monetization", niche=niche, account_stage="", region=region,
        )
        return self._call_groq_with_fallback(
            command="project_monetization", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.7, ttl_hours=24,
        )

    def suggest_content_category(
        self,
        user_context: str,
        available_categories: list,
        niche: str = "",
        goal: str = "",
        chat_id: int = None,
    ) -> dict:
        """AI-driven selection of the most relevant prompt category for the user."""
        categories_str = ", ".join(available_categories)
        extra = ""
        if niche:
            extra += f"\nNiche: {niche}"
        if goal:
            extra += f"\nGoal: {goal}"

        prompt = f"""You are an Instagram content strategist.

Available prompt categories: {categories_str}
User context: {user_context}{extra}

Select the most relevant categories from the available list for this user.

Return JSON with:
- recommended: list of 1-3 category names (exact strings from the available list)
- reasoning: why these categories fit the user's context
- suggested_category: single best match (exact string from the available list)"""

        cache_key = self._make_cache_key(
            "suggest_content_category", niche=niche, action=goal,
        )
        return self._call_groq_with_fallback(
            command="suggest_content_category", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.4, ttl_hours=24,
        )

    def forecast_viral_potential(
        self,
        content_idea: str,
        niche: str = "",
        account_stage: str = "",
        region: str = "",
        chat_id: int = None,
    ) -> dict:
        """AI-reasoned viral potential score for a content idea."""
        ctx_parts = []
        if niche:
            ctx_parts.append(f"niche: {niche}")
        if account_stage:
            ctx_parts.append(f"account stage: {account_stage}")
        if region:
            ctx_parts.append(f"region: {region}")
        context_note = f" ({', '.join(ctx_parts)})" if ctx_parts else ""

        prompt = f"""You are an Instagram viral content analyst.

Content idea{context_note}: \"{content_idea}\"

Evaluate the viral potential of this content idea. Base your assessment on the specific niche and audience — do not use generic keyword matching or fixed formulas.

Return JSON with:
- viral_score: estimated score 0-100
- virality_prediction: one of Very High | High | Medium | Low with brief explanation
- why_it_works: specific reasons this idea could go viral for this niche
- risks: factors that might limit performance
- predicted_reach_tier: broad/medium/niche explanation of expected distribution
- recommendations: list of specific improvements to maximise viral potential
- confidence_note: honest assessment of prediction certainty"""

        cache_key = self._make_cache_key(
            "forecast_viral_potential", niche=niche,
            account_stage=account_stage, region=region, topic=content_idea[:40],
        )
        return self._call_groq_with_fallback(
            command="forecast_viral_potential", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.6, ttl_hours=12,
        )

    def classify_intent(
        self,
        user_message: str,
        available_commands: list,
        chat_id: int = None,
    ) -> dict:
        """Classify free-text user intent into a known command with extracted parameters."""
        commands_str = ", ".join(available_commands)
        prompt = f"""You are an intent classifier for an Instagram growth bot.

Available commands: {commands_str}
User message: \"{user_message}\"

Classify the user's intent and extract any relevant parameters (niche, topic, account_size, etc.).

Return JSON with:
- command: best matching command from the available list (exact string)
- confidence: 0.0-1.0
- extracted_params: dict of any parameters mentioned or implied in the message
- fallback_to_chat: true if no command fits well (confidence < 0.5)"""

        cache_key = self._make_cache_key(
            "classify_intent", action=user_message[:50],
        )
        return self._call_groq_with_fallback(
            command="classify_intent", cache_key=cache_key,
            prompt=prompt, chat_id=chat_id, temperature=0.2, ttl_hours=1,
        )

    def generate_content_ideas(
        self,
        trends: list,
        niche: str = "",
        region: str = "",
        chat_id: int = None,
    ) -> dict:
        """Generate AI content ideas from a list of scraped trends."""
        trends_str = (
            "\n".join(f"- {t}" for t in trends[:20])
            if trends
            else "No specific trends provided"
        )
        ctx_parts = []
        if niche:
            ctx_parts.append(f"niche: {niche}")
        if region:
            ctx_parts.append(f"region: {region}")
        context_note = f" ({', '.join(ctx_parts)})" if ctx_parts else ""

        prompt = f"""You are an Instagram content strategist{context_note}.

Current trending topics:
{trends_str}

Generate creative content ideas based on these trends. Tailor ideas to the specific niche and audience — do not use generic templates.

Return JSON with:
- content_ideas: list of idea objects, each with:
    topic: specific content topic (not generic)
    format: Reel | Carousel | Story Series | Static Post
    angle: unique creative angle that makes this shareable
    trend_connection: how it connects to the trending topic
    hook: opening line for the caption
- trend_summary: what the trending data signals for content strategy
- best_opportunity: the single highest-potential idea with detailed execution notes"""

        cache_key = self._make_cache_key(
            "generate_content_ideas",
            niche=niche,
            region=region,
            topic=str(trends[:3]),
        )
        return self._call_groq_with_fallback(
            command="generate_content_ideas",
            cache_key=cache_key,
            prompt=prompt,
            chat_id=chat_id,
            temperature=0.75,
            ttl_hours=12,
        )


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
