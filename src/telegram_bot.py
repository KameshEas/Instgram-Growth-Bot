#!/usr/bin/env python3
"""
Telegram Bot Interface for Instagram Growth Bot
Access AI agents via Telegram commands (/content, /trends, /engagement, /monetize)
"""

import os
import sys
import logging
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from the .env file in the telegram-insta-bot directory
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path), override=True)
else:
    # Try parent directory if not found
    env_path_alt = Path(__file__).parent.parent.parent / ".env"
    if env_path_alt.exists():
        load_dotenv(dotenv_path=str(env_path_alt), override=True)

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/telegram_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import telegram
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.error("[ERROR] python-telegram-bot not installed")
    logger.error("[INFO] Install with: pip install python-telegram-bot==20.3")

# Import Instagram Growth Bot
try:
    from src.main import InstagramGrowthBot
except ImportError as e:
    logger.error(f"[ERROR] Cannot import InstagramGrowthBot: {e}")
    logger.error("[INFO] Make sure you're in the telegram-insta-bot directory")
    raise


class TelegramBotHandler:
    """Handles Telegram bot interactions with Instagram Growth Bot"""
    
    def __init__(self):
        """Initialize the Telegram bot handler"""
        # Get bot token from .env file
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not self.bot_token:
            raise ValueError("[ERROR] TELEGRAM_BOT_TOKEN not found in .env file")
        
        self.bot = InstagramGrowthBot()
        logger.info("[OK] Telegram bot handler initialized")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Catch-all message handler for debugging"""
        logger.info(f"[DEBUG] Message received: {update.message.text}")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        logger.info(f"[DEBUG] /start command received from {update.effective_user.username}")
        user = update.effective_user
        text = f"👋 *Welcome, {user.first_name}!*\n\n"
        text += "*Instagram Growth Bot* — Your AI creative studio\n"
        text += "300+ prompts · 18 categories · 3 skill levels\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━━\n"
        text += "🎨 *PROMPT LIBRARY*\n"
        text += "  /categories — Browse all 18 categories\n"
        text += "  /generate `[category]` — Get 3 prompts\n"
        text += "  /generate `[category] [level]` — Filter by skill\n"
        text += '  /generate `[category] "concept"` — AI enhance\n'
        text += "  /search `[keyword]` — Find matching prompts\n"
        text += "  /inspire `[topic]` — 3 creative angles\n\n"
        text += "📊 *GROWTH TOOLS*\n"
        text += "  /content `[topic] [style]` — Generate captions\n"
        text += "  /trends `[niche]` — Trending topics\n"
        text += "  /engagement `[size]` — Engagement strategy\n"
        text += "  /monetize `[niche] [followers]` — Revenue ideas\n\n"
        text += "🟢 Beginner  🔵 Professional  🔴 Expert\n"
        text += "━━━━━━━━━━━━━━━━━━━━━\n"
        text += "/help — Full usage guide"

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"[OK] User {user.id} ({user.username}) started bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        logger.info(f"[DEBUG] /help command received from {update.effective_user.username}")
        text = "📖 *Full Usage Guide*\n\n"
        text += "*🎨 PROMPT LIBRARY*\n"
        text += "• `/generate [category]` — 3 mixed-level prompts\n"
        text += "• `/generate [category] beginner` — 🟢 simple prompts\n"
        text += "• `/generate [category] professional` — 🔵 pro prompts\n"
        text += "• `/generate [category] expert` — 🔴 advanced prompts\n"
        text += '• `/generate design_posters "Diwali poster"` — AI enhance\n'
        text += '• `/generate ui_ux_design expert "fitness app"` — Level + AI\n\n'
        text += "• `/categories` — All 18 categories with tools\n"
        text += "• `/search logo` — Find prompts by keyword\n"
        text += "• `/inspire Indian wedding` — 3 creative angles\n\n"
        text += "*📊 GROWTH TOOLS*\n"
        text += "• `/content fitness motivational` — Viral captions\n"
        text += "• `/trends fitness` — Trending hashtags\n"
        text += "• `/engagement micro` — Daily targets + templates\n"
        text += "• `/monetize fitness 50000` — Revenue strategies\n\n"
        text += "*📂 18 CATEGORIES*\n"
        text += "📷 Photography · ✨ Transform · 💑 Couples\n"
        text += "🎨 Design · 🏷️ Brand · 🖌️ Illustration · 🖨️ Print · 📦 3D\n"
        text += "🖥️ UI/UX · 🎞️ Animation · 📸 Photo Styles\n"
        text += "🎬 Reels · ✍️ Captions · 📧 Email\n\n"
        text += "💡 Tip: Use `/categories` to see all with tools & examples"

        await update.message.reply_text(text, parse_mode="Markdown")
    
    async def content_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /content command - Generate captions"""
        logger.info(f"[DEBUG] /content command received from {update.effective_user.username}")
        if len(context.args) < 2:
            await update.message.reply_text(
                "Usage: /content [topic] [style]\n"
                "Styles: engaging, motivational, humorous, inspirational\n"
                "Example: /content fitness_transformation motivational"
            )
            return
        
        # Parse arguments
        topic = " ".join(context.args[:-1]).replace("_", " ")
        style = context.args[-1].replace("_", " ")
        
        # Send status message
        await update.message.reply_text(f"[WAIT] Generating content for '{topic}' ({style})...")
        
        try:
            # Call bot
            result = self.bot.generate_content(topic=topic, style=style)
            
            if result and "captions" in result:
                msg = f"✅ Generated {len(result.get('captions', []))} captions for '{topic}':\n\n"
                
                # Show captions
                for i, caption in enumerate(result.get("captions", []), 1):
                    text = caption.get("text") or caption.get("caption", "")
                    virality = caption.get("virality_score", "N/A")
                    msg += f"{i}. [Virality: {virality}%]\n{text[:150]}...\n\n"
                
                # Show hashtags
                hashtags = result.get("hashtags", [])
                if hashtags:
                    msg += "Suggested Hashtags:\n"
                    for tag in hashtags[:10]:
                        clean_tag = tag.replace("#", "")
                        msg += f"#{clean_tag} "
                
                # Send message (Telegram limit: 4096 chars)
                if len(msg) > 4000:
                    await update.message.reply_text(msg[:4000])
                    await update.message.reply_text(msg[4000:])
                else:
                    await update.message.reply_text(msg)
                
                logger.info(f"[OK] Content generated for: {topic}")
            else:
                await update.message.reply_text(f"[ERROR] Failed to generate content\n{result}")
                logger.error(f"Content generation failed: {result}")
        
        except Exception as e:
            await update.message.reply_text(f"[ERROR] {str(e)}")
            logger.error(f"Content command error: {e}")
    
    async def trends_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /trends command - Analyze trends"""
        logger.info(f"[DEBUG] /trends command received from {update.effective_user.username}")
        if len(context.args) < 1:
            await update.message.reply_text(
                "Usage: /trends [niche]\n"
                "Example: /trends fitness"
            )
            return
        
        niche = context.args[0].replace("_", " ")
        
        await update.message.reply_text(f"[WAIT] Analyzing trends for '{niche}'...")
        
        try:
            result = self.bot.analyze_trends(niche=niche)
            
            # If result is a string, try to parse it
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    pass
            
            # Handle both old and new response formats
            if result and isinstance(result, dict) and ("trending_topics" in result or "topHashtags" in result):
                msg = f"✅ Trending topics in {niche}:\n\n"
                
                # Try new format first (topHashtags)
                if "topHashtags" in result:
                    for i, hashtag_obj in enumerate(result.get("topHashtags", [])[:5], 1):
                        hashtag = hashtag_obj.get("hashtag", "N/A")
                        viral_potential = hashtag_obj.get("viralPotential", "N/A")
                        msg += f"{i}. {hashtag}\n   Viral Potential: {viral_potential}%\n\n"
                else:
                    # Fall back to old format
                    for i, topic in enumerate(result.get("trending_topics", [])[:5], 1):
                        topic_name = topic.get("topic") or topic.get("hashtag", "N/A")
                        viral_potential = topic.get("viral_potential", "N/A")
                        msg += f"{i}. {topic_name}\n   Viral Potential: {viral_potential}%\n\n"
                
                # Add posting times if available
                if "bestPostingTimes" in result:
                    msg += "⏰ Best Posting Times:\n"
                    for time_obj in result.get("bestPostingTimes", [])[:3]:
                        time_slot = time_obj.get("time", "N/A")
                        engagement = time_obj.get("engagementRate", "N/A")
                        msg += f"• {time_slot}: {engagement}% engagement\n"
                    msg += "\n"
                
                msg += "Use /content to generate posts for these trending topics"
                
                if len(msg) > 4000:
                    await update.message.reply_text(msg[:4000])
                    await update.message.reply_text(msg[4000:])
                else:
                    await update.message.reply_text(msg)
                
                logger.info(f"[OK] Trends analyzed for: {niche}")
            else:
                await update.message.reply_text(f"[ERROR] Failed to analyze trends\n{result}")
                logger.error(f"Trend analysis failed: {result}")
        
        except Exception as e:
            await update.message.reply_text(f"[ERROR] {str(e)}")
            logger.error(f"Trends command error: {e}")
    
    async def engagement_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /engagement command - Get engagement strategy"""
        logger.info(f"[DEBUG] /engagement command received from {update.effective_user.username}")
        if len(context.args) < 1:
            await update.message.reply_text(
                "Usage: /engagement [size]\n"
                "Sizes: micro (5K-100K), small (100K-500K), medium (500K+)\n"
                "Example: /engagement micro"
            )
            return
        
        account_size = context.args[0].replace("_", " ")
        
        await update.message.reply_text(f"[WAIT] Creating engagement strategy for {account_size} account...")
        
        try:
            result = self.bot.engagement_strategy(account_size=account_size)
            
            if result and "engagement_targets" in result:
                targets = result.get("engagement_targets", {})
                msg = f"✅ Engagement Strategy ({account_size} account):\n\n"
                
                msg += "📈 Daily Targets:\n"
                msg += f"• Follows: {targets.get('daily_follows', 'N/A')}\n"
                msg += f"• Likes: {targets.get('daily_likes', 'N/A')}\n"
                msg += f"• Comments: {targets.get('daily_comments', 'N/A')}\n\n"
                
                # Show comment templates
                templates = result.get("comment_templates", [])
                if templates:
                    msg += "💬 Sample Comment Templates:\n"
                    for i, template in enumerate(templates[:3], 1):
                        text = template.get("template") if isinstance(template, dict) else template
                        msg += f"{i}. {text}\n"
                
                # Show timing recommendations
                timing = result.get("timing_recommendations", {})
                if timing:
                    msg += "\n⏰ Timing:\n"
                    peak_hours = timing.get("peak_hours", [])
                    best_days = timing.get("best_days", [])
                    if peak_hours:
                        msg += f"• Peak Hours: {', '.join(str(h) for h in peak_hours[:3])}\n"
                    if best_days:
                        msg += f"• Best Days: {', '.join(best_days[:3])}\n"
                
                if len(msg) > 4000:
                    await update.message.reply_text(msg[:4000])
                    await update.message.reply_text(msg[4000:])
                else:
                    await update.message.reply_text(msg)
                
                logger.info(f"[OK] Engagement strategy created for: {account_size}")
            else:
                await update.message.reply_text(f"[ERROR] Failed to generate strategy\n{result}")
                logger.error(f"Engagement strategy failed: {result}")
        
        except Exception as e:
            await update.message.reply_text(f"[ERROR] {str(e)}")
            logger.error(f"Engagement command error: {e}")
    
    async def monetize_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /monetize command - Get monetization ideas"""
        logger.info(f"[DEBUG] /monetize command received from {update.effective_user.username}")
        if len(context.args) < 2:
            await update.message.reply_text(
                "Usage: /monetize [niche] [follower_count]\n"
                "Example: /monetize fitness 50000"
            )
            return
        
        niche = context.args[0].replace("_", " ")
        try:
            followers = int(context.args[1])
        except ValueError:
            await update.message.reply_text("[ERROR] Follower count must be a number\nExample: /monetize fitness 50000")
            return
        
        await update.message.reply_text(f"[WAIT] Finding monetization ideas for {niche} ({followers} followers)...")
        
        try:
            result = self.bot.monetization_ideas(niche=niche, follower_count=followers)
            
            strategies_key = "Monetization Strategies" if "Monetization Strategies" in result else "monetization_strategies"
            
            if result and strategies_key in result:
                strategies = result.get(strategies_key, [])
                msg = f"✅ Monetization Ideas for {niche} ({followers}+ followers):\n\n"
                
                for i, strategy in enumerate(strategies[:4], 1):
                    name = strategy.get("Strategy") or strategy.get("name", "Strategy")
                    desc = strategy.get("Description") or strategy.get("description", "")
                    revenue = strategy.get("Revenue Projection") or strategy.get("realistic_revenue_projection", "N/A")
                    
                    msg += f"{i}. {name}\n"
                    if desc:
                        msg += f"   {desc[:100]}\n"
                    msg += f"   💵 {revenue}\n\n"
                
                if len(msg) > 4000:
                    await update.message.reply_text(msg[:4000])
                    await update.message.reply_text(msg[4000:])
                else:
                    await update.message.reply_text(msg)
                
                logger.info(f"[OK] Monetization ideas for: {niche}")
            else:
                await update.message.reply_text(f"[ERROR] Failed to generate ideas\n{result}")
                logger.error(f"Monetization ideas failed: {result}")
        
        except Exception as e:
            await update.message.reply_text(f"[ERROR] {str(e)}")
            logger.error(f"Monetize command error: {e}")
    
    async def generate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /generate [category] [level] ["custom prompt"] — get image generation prompts."""
        logger.info(f"[DEBUG] /generate command from {update.effective_user.username}")

        full_text = update.message.text
        text_after_command = full_text.replace("/generate", "", 1).strip()

        if not text_after_command:
            await update.message.reply_text(
                "🎨 *Generate Prompts*\n\n"
                "Usage:\n"
                "  `/generate [category]`\n"
                "  `/generate [category] [level]`\n"
                "  `/generate [category] \"custom concept\"`\n"
                "  `/generate [category] [level] \"custom concept\"`\n\n"
                "Levels: `beginner` 🟢 · `professional` 🔵 · `expert` 🔴\n\n"
                "Examples:\n"
                "• `/generate ui_ux_design professional`\n"
                "• `/generate design_posters expert \"Diwali sale poster\"`\n"
                "• `/generate brand_identity beginner`\n\n"
                "See all categories: `/categories`",
                parse_mode="Markdown",
            )
            return

        # Parse: category + optional level + optional quoted prompt
        LEVELS = {"beginner", "professional", "expert"}
        tokens = text_after_command.split(" ", 2)
        category = tokens[0].strip().lower()
        level = None
        custom_prompt = None

        remaining = text_after_command[len(category):].strip()

        # Check if second token is a difficulty level
        if remaining:
            next_token = remaining.split(" ", 1)[0].lower()
            if next_token in LEVELS:
                level = next_token
                remaining = remaining[len(next_token):].strip()

        # Extract quoted custom prompt from remaining text
        if remaining:
            if (remaining.startswith('"') or remaining.startswith("'")):
                custom_prompt = remaining.strip("\"'")
            else:
                custom_prompt = remaining

        if custom_prompt:
            lvl_label = f" [{level}]" if level else ""
            await update.message.reply_text(f"⏳ Enhancing your concept for *{category}*{lvl_label}...", parse_mode="Markdown")
        else:
            lvl_label = f" [{level}]" if level else " [mixed levels]"
            await update.message.reply_text(f"⏳ Fetching prompts for *{category}*{lvl_label}...", parse_mode="Markdown")

        try:
            result = self.bot.image_generation_prompts(category=category, custom_prompt=custom_prompt, level=level)

            if result and result.get("status") == "success":
                prompts = result.get("prompts", [])
                is_custom = result.get("custom", False)
                meta = result.get("meta", {})
                cat_emoji = meta.get("emoji", "🎯")
                tools = ", ".join(meta.get("tools", [])) or "DALL-E 3, Midjourney, Stable Diffusion"
                best_for = meta.get("best_for", "")
                res_level = result.get("level", level or "mixed")

                from src.prompts.templates import DIFFICULTY_EMOJI
                lvl_icon = DIFFICULTY_EMOJI.get(res_level, "")

                def split_smart(text, max_len=3500):
                    if len(text) <= max_len:
                        return [text]
                    parts, current = [], ""
                    for line in text.split("\n"):
                        if len(current) + len(line) + 2 > max_len:
                            if current.strip():
                                parts.append(current.strip())
                            current = line + "\n"
                        else:
                            current += line + "\n"
                    if current.strip():
                        parts.append(current.strip())
                    return parts or [text]

                if is_custom:
                    header = f"{cat_emoji} *Custom Prompt — {category}* {lvl_icon}\n"
                    if best_for:
                        header += f"Best for: {best_for}\n"
                    header += "─────────────────────\n\n"

                    parts = split_smart(prompts[0])
                    first = header + parts[0]
                    if len(first) > 4000:
                        await update.message.reply_text(header, parse_mode="Markdown")
                        await update.message.reply_text(parts[0])
                    else:
                        await update.message.reply_text(first, parse_mode="Markdown")
                    for part in parts[1:]:
                        if part:
                            await update.message.reply_text(part)

                    footer = f"\n🛠 Tools: {tools}"
                    await update.message.reply_text(footer)

                else:
                    level_labels = {"beginner": "🟢 Beginner", "professional": "🔵 Professional",
                                    "expert": "🔴 Expert", "mixed": "🌈 Mixed Levels"}
                    level_display = level_labels.get(res_level, res_level.title())

                    msg = f"{cat_emoji} *{category}* — {level_display}\n"
                    if best_for:
                        msg += f"Best for: {best_for}\n"
                    msg += "─────────────────────\n\n"

                    for i, prompt in enumerate(prompts, 1):
                        msg += f"*Prompt {i}:*\n{prompt}\n\n"

                    msg += f"─────────────────────\n"
                    msg += f"🛠 Tools: {tools}\n"
                    msg += f"💡 Custom: `/generate {category} \"your concept\"`\n"
                    msg += f"🔢 Levels: `/generate {category} beginner|professional|expert`"

                    parts = split_smart(msg)
                    await update.message.reply_text(parts[0], parse_mode="Markdown")
                    for part in parts[1:]:
                        if part:
                            await update.message.reply_text(part, parse_mode="Markdown")

                logger.info(f"[OK] Prompts served — category={category}, level={res_level}")
            else:
                error_msg = result.get("error", "Unknown error")
                cats = result.get("available_categories", [])
                msg = f"❌ {error_msg}\n\nSee all categories: /categories"
                if cats:
                    msg += "\n\n" + "\n".join(f"• {c}" for c in cats[:10])
                await update.message.reply_text(msg)

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            logger.error(f"Generate command error: {e}")

    async def categories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /categories — list all prompt categories with metadata."""
        logger.info(f"[DEBUG] /categories from {update.effective_user.username}")
        try:
            from src.prompts.templates import list_categories, get_category_meta, get_all_prompts_count
            cats = list_categories()
            total = get_all_prompts_count()

            msg = f"📚 *Prompt Library — {total}+ Prompts*\n\n"
            msg += "🟢 Beginner  🔵 Professional  🔴 Expert\n"
            msg += "─────────────────────────────────\n\n"

            sections = {
                "📷 Photography": ["general_photography", "women_professional", "men_professional",
                                   "couples_general", "photography_styles"],
                "✨ Transformation": ["women_transform", "men_transform", "couples_transform"],
                "🎨 Design & Visual": ["design_posters", "brand_identity", "illustration_art",
                                       "print_design", "product_3d"],
                "🖥️ Digital": ["ui_ux_design", "animation_motion"],
                "📝 Content": ["reel_scripts", "captions_templates", "email_subjects"],
            }

            for section, section_cats in sections.items():
                msg += f"*{section}*\n"
                for cat in section_cats:
                    if cat in cats:
                        meta = get_category_meta(cat)
                        emoji = meta.get("emoji", "•")
                        tools = meta.get("tools", [])
                        tool_str = f" — {', '.join(tools[:2])}" if tools else ""
                        msg += f"  {emoji} `{cat}`{tool_str}\n"
                msg += "\n"

            msg += "─────────────────────────────────\n"
            msg += "Usage: `/generate [category]`\n"
            msg += "With level: `/generate [category] expert`\n"
            msg += "With concept: `/generate [category] \"concept\"`"

            await update.message.reply_text(msg, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            logger.error(f"Categories command error: {e}")

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search [keyword] — find prompts across all categories."""
        logger.info(f"[DEBUG] /search from {update.effective_user.username}")
        if not context.args:
            await update.message.reply_text(
                "🔍 *Search Prompts*\n\nUsage: `/search [keyword]`\nExample: `/search logo`",
                parse_mode="Markdown",
            )
            return

        keyword = " ".join(context.args)
        await update.message.reply_text(f"🔍 Searching for *{keyword}*...", parse_mode="Markdown")

        try:
            result = self.bot.search_prompts(keyword)
            if result.get("status") == "success" and result.get("count", 0) > 0:
                results = result["results"]
                from src.prompts.templates import DIFFICULTY_EMOJI
                msg = f"🔍 *Results for \"{keyword}\"* — {result['count']} found\n"
                msg += "─────────────────────────────────\n\n"
                for i, item in enumerate(results[:6], 1):
                    cat = item.get("category", "")
                    lvl = item.get("level", "")
                    lvl_icon = DIFFICULTY_EMOJI.get(lvl, "")
                    prompt_preview = item["prompt"][:120] + ("..." if len(item["prompt"]) > 120 else "")
                    msg += f"*{i}.* `{cat}` {lvl_icon}\n{prompt_preview}\n\n"
                msg += f"Use full prompt: `/generate {results[0]['category']}`"
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text(
                    f"🔍 No results for *{keyword}*.\n\nTry: `/categories` to browse all.", parse_mode="Markdown"
                )
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            logger.error(f"Search command error: {e}")

    async def inspire_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /inspire [topic] — AI generates 3 creative angles."""
        logger.info(f"[DEBUG] /inspire from {update.effective_user.username}")
        if not context.args:
            await update.message.reply_text(
                "💡 *Inspire Mode*\n\nUsage: `/inspire [topic]`\nExample: `/inspire Indian wedding`",
                parse_mode="Markdown",
            )
            return

        topic = " ".join(context.args)
        await update.message.reply_text(f"💡 Generating creative angles for *{topic}*...", parse_mode="Markdown")

        try:
            enhancement_prompt = f"""Generate 3 creative visual content angles for the topic: "{topic}"

For each angle give:
1. Angle name (5 words max)
2. Best category: one of [design_posters, ui_ux_design, brand_identity, illustration_art, photography_styles, animation_motion, print_design, product_3d, women_transform, men_transform]
3. One-sentence concept (max 20 words)
4. Difficulty: beginner / professional / expert

Format as plain text with clear numbering. Be creative and diverse. Max 200 words total."""

            response = self.bot.client.chat.completions.create(
                model=self.bot.model,
                messages=[{"role": "user", "content": enhancement_prompt}],
                temperature=0.9,
                max_tokens=280,
            )
            ideas = response.choices[0].message.content.strip()

            msg = f"💡 *Creative Angles — {topic}*\n"
            msg += "─────────────────────────────────\n\n"
            msg += ideas
            msg += "\n\n─────────────────────────────────\n"
            msg += "Use: `/generate [category] \"concept\"` to create a prompt for any angle above."

            await update.message.reply_text(msg, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            logger.error(f"Inspire command error: {e}")




async def main():
    """Main function - Start Telegram bot"""
    if not TELEGRAM_AVAILABLE:
        logger.error("[ERROR] Telegram library not available. Install with:")
        logger.error("pip install python-telegram-bot==20.3")
        return
    
    try:
        handler = TelegramBotHandler()
    except ValueError as e:
        logger.error(str(e))
        return
    
    # Create application
    app = Application.builder().token(handler.bot_token).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", handler.start))
    app.add_handler(CommandHandler("help", handler.help_command))
    app.add_handler(CommandHandler("content", handler.content_command))
    app.add_handler(CommandHandler("trends", handler.trends_command))
    app.add_handler(CommandHandler("engagement", handler.engagement_command))
    app.add_handler(CommandHandler("monetize", handler.monetize_command))
    app.add_handler(CommandHandler("generate", handler.generate_command))
    app.add_handler(CommandHandler("categories", handler.categories_command))
    app.add_handler(CommandHandler("search", handler.search_command))
    app.add_handler(CommandHandler("inspire", handler.inspire_command))
    
    # Start polling
    logger.info("[OK] Telegram bot started (polling mode)")
    logger.info("[OK] Bot is waiting for commands...")
    logger.info("[INFO] Press Ctrl+C to stop")
    
    # Start and run polling with proper event loop handling
    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        try:
            # Keep the bot running - wait for interrupt signal
            await asyncio.Event().wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            await app.updater.stop()
            await app.stop()


def main_sync():
    """Synchronous wrapper to run the bot using proper event loop handling"""
    if not TELEGRAM_AVAILABLE:
        logger.error("[ERROR] Telegram library not available. Install with:")
        logger.error("pip install python-telegram-bot>=20.7")
        return
    
    try:
        handler = TelegramBotHandler()
    except ValueError as e:
        logger.error(str(e))
        return
    
    # Create application
    app = Application.builder().token(handler.bot_token).build()
    
    # Add error handler
    async def error_handler(update, context):
        logger.error(f"[CRITICAL] Telegram error: {context.error}")
        logger.error(f"Update: {update}")
    
    app.add_error_handler(error_handler)
    
    # Add command handlers
    app.add_handler(CommandHandler("start", handler.start))
    app.add_handler(CommandHandler("help", handler.help_command))
    app.add_handler(CommandHandler("content", handler.content_command))
    app.add_handler(CommandHandler("trends", handler.trends_command))
    app.add_handler(CommandHandler("engagement", handler.engagement_command))
    app.add_handler(CommandHandler("monetize", handler.monetize_command))
    app.add_handler(CommandHandler("generate", handler.generate_command))
    app.add_handler(CommandHandler("categories", handler.categories_command))
    app.add_handler(CommandHandler("search", handler.search_command))
    app.add_handler(CommandHandler("inspire", handler.inspire_command))
    
    # Add catch-all message handler for debugging
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_message))
    
    # Start polling
    logger.info("[OK] Telegram bot started (polling mode)")
    logger.info("[OK] Bot is waiting for commands...")
    logger.info("[INFO] Press Ctrl+C to stop")
    
    # Use run_polling() directly - this handles event loops properly
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("[OK] Bot stopped by user")
    except Exception as e:
        logger.error(f"[ERROR] Bot error: {e}")
