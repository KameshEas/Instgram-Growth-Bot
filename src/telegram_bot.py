#!/usr/bin/env python3
"""
Telegram Bot — Instagram Growth Advisor
All commands routed through ContentOrchestratorAgent.
User profiles stored in SQLite for personalised AI responses.
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
    env_path_alt = Path(__file__).parent.parent.parent / ".env"
    if env_path_alt.exists():
        load_dotenv(dotenv_path=str(env_path_alt), override=True)

# Create logs directory
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)


def escape_md(text: str) -> str:
    """Escape special characters for Telegram legacy Markdown v1."""
    # Handle non-string inputs gracefully
    if not isinstance(text, str):
        text = str(text)
    for ch in ("*", "_", "`", "["):
        text = text.replace(ch, "\\" + ch)
    return text


_TRANSFORM_CATEGORIES = {"women_transform", "men_transform", "couples_transform"}


def strip_transform_boilerplate(prompt: str) -> str:
    prefix = "EXACT FACE MATCH + IDENTITY PRESERVATION: "
    if prompt.startswith(prefix):
        prompt = prompt[len(prefix):]
    for marker in (" Facial feature preservation", ". Facial feature preservation"):
        idx = prompt.find(marker)
        if idx != -1:
            prompt = prompt[:idx].rstrip(".,; ")
            break
    return prompt.strip()


# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/telegram_bot.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Ensure stdout/stderr use UTF-8 to avoid UnicodeEncodeError on Windows consoles
try:
    if sys.stdout and (sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr and (sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ── Telegram imports ──────────────────────────────────────────────────────────
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        ConversationHandler,
        ContextTypes,
        filters,
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.error("[ERROR] python-telegram-bot not installed")
    logger.error("[INFO] Install with: pip install python-telegram-bot==20.3")


# ── Bot imports ───────────────────────────────────────────────────────────────
try:
    from src.main import InstagramGrowthBot
except ImportError as e:
    logger.error(f"[ERROR] Cannot import InstagramGrowthBot: {e}")
    raise

try:
    from src.agents.orchestrator import ContentOrchestratorAgent
except ImportError as e:
    logger.error(f"[ERROR] Cannot import ContentOrchestratorAgent: {e}")
    raise

try:
    from src.database.user_db import get_profile, save_profile, update_profile, delete_profile
    DB_AVAILABLE = True
except ImportError as e:
    logger.warning(f"[WARN] user_db not available — profiles disabled: {e}")
    DB_AVAILABLE = False


# ── ConversationHandler states ────────────────────────────────────────────────
SETUP_NICHE, SETUP_AUDIENCE, SETUP_GOALS = range(3)



class TelegramBotHandler:
    """Handles Telegram bot interactions with Instagram Growth Bot"""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("[ERROR] TELEGRAM_BOT_TOKEN not found in .env file")
        self.bot = InstagramGrowthBot()
        self.orchestrator = ContentOrchestratorAgent(groq_bot=self.bot)
        logger.info("[OK] Telegram bot handler initialized")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _get_profile(self, chat_id: int) -> dict:
        """Return the user's profile dict, or an empty dict if DB unavailable."""
        if DB_AVAILABLE:
            return get_profile(chat_id) or {}
        return {}

    @staticmethod
    def _main_menu_keyboard() -> InlineKeyboardMarkup:
        """Return the main menu with all features including Phase 3."""
        buttons = [
            [InlineKeyboardButton("📷 Generate Prompts", callback_data="cat_select")],
            [InlineKeyboardButton("✍️ Caption", callback_data="cmd_caption"),
             InlineKeyboardButton("#️⃣ Hashtags", callback_data="cmd_hashtags"),
             InlineKeyboardButton("📝 Bio", callback_data="cmd_bio")],
            [InlineKeyboardButton("📅 Ideas", callback_data="cmd_ideas"),
             InlineKeyboardButton("⏰ Schedule", callback_data="cmd_schedule"),
             InlineKeyboardButton("📖 Stories", callback_data="cmd_stories")],
            [InlineKeyboardButton("📊 Trends", callback_data="cmd_trends"),
             InlineKeyboardButton("💬 Engagement", callback_data="cmd_engagement"),
             InlineKeyboardButton("💰 Monetize", callback_data="cmd_monetize")],
            [InlineKeyboardButton("🔍 Audit", callback_data="cmd_audit"),
             InlineKeyboardButton("📈 Analytics", callback_data="cmd_analytics"),
             InlineKeyboardButton("👤 Profile", callback_data="cmd_profile")],
            # Phase 2: Favorites, History, Settings
            [InlineKeyboardButton("💾 Favorites", callback_data="cmd_favorites"),
             InlineKeyboardButton("📜 History", callback_data="cmd_history"),
             InlineKeyboardButton("⚙️ Settings", callback_data="cmd_settings")],
            # Phase 3: Smart Analytics & Recommendations
            [InlineKeyboardButton("📊 Stats", callback_data="cmd_stats"),
             InlineKeyboardButton("🎯 Recommend", callback_data="cmd_recommend"),
             InlineKeyboardButton("🔄 Regenerate", callback_data="cmd_regenerate")],
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def _category_keyboard() -> InlineKeyboardMarkup:
        """Return inline keyboard for photo category selection."""
        buttons = [
            [InlineKeyboardButton("📷 General Photography", callback_data="gen_general_photography")],
            [InlineKeyboardButton("👩 Women Professional", callback_data="gen_women_professional"),
             InlineKeyboardButton("👨 Men Professional", callback_data="gen_men_professional")],
            [InlineKeyboardButton("👩✨ Women Transform", callback_data="gen_women_transform"),
             InlineKeyboardButton("👨✨ Men Transform", callback_data="gen_men_transform")],
            [InlineKeyboardButton("💑 Couples Transform", callback_data="gen_couples_transform")],
            [InlineKeyboardButton("🎨 Design Posters", callback_data="gen_design_posters"),
             InlineKeyboardButton("🎁 Design Gifts", callback_data="gen_design_gifts")],
            [InlineKeyboardButton("🖥️ UI/UX Design", callback_data="gen_ui_ux_design"),
             InlineKeyboardButton("🏢 Brand Identity", callback_data="gen_brand_identity")],
            [InlineKeyboardButton("🎭 Illustration", callback_data="gen_illustration_art"),
             InlineKeyboardButton("🎬 Animation", callback_data="gen_animation_motion")],
            [InlineKeyboardButton("📸 Fine Art", callback_data="gen_photography_styles"),
             InlineKeyboardButton("📄 Print Design", callback_data="gen_print_design")],
            [InlineKeyboardButton("◀️ Back to Menu", callback_data="back_menu")],
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def _prompt_action_buttons(prompt_id: str = "1") -> InlineKeyboardMarkup:
        """Return action buttons for generated prompts."""
        buttons = [
            [InlineKeyboardButton("💾 Save", callback_data=f"save_prompt_{prompt_id}"),
             InlineKeyboardButton("🔄 Refine", callback_data=f"refine_prompt_{prompt_id}"),
             InlineKeyboardButton("📋 Copy", callback_data=f"copy_prompt_{prompt_id}")],
            [InlineKeyboardButton("🔄 Generate More", callback_data="gen_more"),
             InlineKeyboardButton("📚 See All", callback_data="see_all_categories")],
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def _send_long(text: str, max_len: int = 4000) -> list:
        """Split text into chunks of at most max_len characters."""
        if len(text) <= max_len:
            return [text]
        parts, current = [], ""
        for line in text.split("\n"):
            if len(current) + len(line) + 1 > max_len:
                if current.strip():
                    parts.append(current.strip())
                current = line + "\n"
            else:
                current += line + "\n"
        if current.strip():
            parts.append(current.strip())
        return parts or [text]

    # ── /start ────────────────────────────────────────────────────────────────

    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start — personalized welcome + main menu."""
        user = update.effective_user
        chat_id = update.effective_chat.id
        profile = self._get_profile(chat_id)

        if profile and profile.get("niche"):
            niche = profile["niche"]
            size = profile.get("audience_size", "your account")
            intro = (
                f"👋 Welcome back, *{user.first_name}!*\n"
                f"Your profile: *{niche}* · *{size}*\n\n"
                "All AI responses are tailored to you. What would you like to do today?"
            )
        else:
            intro = (
                f"👋 Hey *{user.first_name}*, welcome to your *Instagram Growth Advisor!*\n\n"
                "I'm your personal AI coach for growing on Instagram.\n"
                "Start by setting up your profile with /setup so I can personalise every response for you.\n\n"
                "Or just tap a button below to get started right away:"
            )

        await update.message.reply_text(
            intro,
            parse_mode="Markdown",
            reply_markup=self._main_menu_keyboard(),
        )
        logger.info(f"[OK] /start — user {user.id} ({user.username})")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command — show updated command reference with better organization."""
        text = (
            "📖 *Instagram Growth Advisor — Complete Command Guide*\n\n"
            "🚀 *Quick Start*\n"
            "  /start — Main menu with all commands\n"
            "  /setup — Personalize your profile (niche, audience, goals)\n\n"
            "📷 *AI Image Prompt Generation*\n"
            "  /generate — Browse & select photo categories\n"
            "  /categories — Browse all available categories\n"
            "  /search `[keyword]` — Find categories by keyword\n"
            "  /logo_create — Generate high-res PNG logos + design system\n\n"
            "✍️ *Content Creation*\n"
            "  /caption — Viral captions with CTAs\n"
            "  /hashtags — 30 trending hashtags in 3 tiers\n"
            "  /bio — Rewrite your Instagram bio\n"
            "  /stories — 5 interactive Story ideas\n\n"
            "📅 *Planning & Strategy*\n"
            "  /ideas — 7-post weekly content calendar\n"
            "  /schedule — Best posting times for your niche\n"
            "  /trends — Trending topics & hashtags for your niche\n"
            "  /engagement — Personalized engagement strategy\n"
            "  /monetize — Revenue & partnership ideas\n\n"
            "📊 *Analytics & Insights*\n"
            "  /analytics — Daily/weekly/monthly performance reports\n"
            "  /audit — Profile improvement checklist\n\n"
            "⚙️ *Profile Management*\n"
            "  /profile — View & edit your saved profile\n"
            "  /set_role — Set your professional role (for personalization)\n"
            "  /settings — View & manage your preferences\n\n"
            "💾 *Phase 2: Favorites & History* ✨\n"
            "  /favorites — View all saved favorite prompts\n"
            "  /history — See your prompt generation history\n"
            "  💡 Tip: Use [💾 Save] button when generating prompts!\n\n"
            "🎯 *Phase 3: Smart Analytics* ✨✨\n"
            "  /stats — View your generation statistics\n"
            "  /recommend — Get personalized category recommendations\n"
            "  /regenerate — Quickly regenerate last request\n"
            "  💡 Tip: Your history powers smart suggestions!\n\n"
            "💡 *Pro Tip:* Use /setup first to unlock fully personalized responses!"
        )
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=self._main_menu_keyboard()
        )
    
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
            result = await self.orchestrator.execute({
                "command": "/content",
                "topic": topic,
                "style": style,
            })
            
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
            result = await self.orchestrator.execute({
                "command": "/trends",
                "niche": niche,
            })
            
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
            result = await self.orchestrator.execute({
                "command": "/engagement",
                "account_size": account_size,
            })
            
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
            result = await self.orchestrator.execute({
                "command": "/monetize",
                "niche": niche,
                "follower_count": followers,
            })
            
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
    
    # ── /setup (ConversationHandler) ──────────────────────────────────────────

    async def setup_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Step 0: kick off the /setup conversation."""
        buttons = [
            [InlineKeyboardButton("Lifestyle", callback_data="niche_Lifestyle"),
             InlineKeyboardButton("Fashion", callback_data="niche_Fashion")],
            [InlineKeyboardButton("Food", callback_data="niche_Food"),
             InlineKeyboardButton("Fitness", callback_data="niche_Fitness")],
            [InlineKeyboardButton("Business", callback_data="niche_Business"),
             InlineKeyboardButton("Travel", callback_data="niche_Travel")],
            [InlineKeyboardButton("Tech", callback_data="niche_Tech"),
             InlineKeyboardButton("Other", callback_data="niche_Other")],
        ]
        await update.message.reply_text(
            "⚙️ *Profile Setup (1/3)*\n\nWhat is your Instagram niche?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return SETUP_NICHE

    async def setup_niche(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Step 1: save niche, ask audience size."""
        query = update.callback_query
        await query.answer()
        niche = query.data.replace("niche_", "")
        context.user_data["setup_niche"] = niche

        buttons = [
            [InlineKeyboardButton("Just Starting (0–1K)", callback_data="aud_Just Starting")],
            [InlineKeyboardButton("Growing (1K–10K)", callback_data="aud_1K–10K")],
            [InlineKeyboardButton("Established (10K–50K)", callback_data="aud_10K–50K")],
            [InlineKeyboardButton("Popular (50K–200K)", callback_data="aud_50K–200K")],
            [InlineKeyboardButton("Influencer (200K+)", callback_data="aud_200K+")],
        ]
        await query.edit_message_text(
            f"✅ Niche: *{niche}*\n\n⚙️ *Profile Setup (2/3)*\n\nHow big is your audience?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return SETUP_AUDIENCE

    async def setup_audience(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Step 2: save audience size, ask goals."""
        query = update.callback_query
        await query.answer()
        audience = query.data.replace("aud_", "")
        context.user_data["setup_audience"] = audience

        buttons = [
            [InlineKeyboardButton("Grow Followers", callback_data="goal_Grow Followers"),
             InlineKeyboardButton("Make Money", callback_data="goal_Make Money")],
            [InlineKeyboardButton("Build Brand", callback_data="goal_Build Brand"),
             InlineKeyboardButton("Get Brand Deals", callback_data="goal_Get Brand Deals")],
            [InlineKeyboardButton("All of the above", callback_data="goal_All")],
        ]
        await query.edit_message_text(
            f"✅ Niche: *{context.user_data['setup_niche']}* · Audience: *{audience}*\n\n"
            "⚙️ *Profile Setup (3/3)*\n\nWhat is your main goal?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return SETUP_GOALS

    async def setup_goals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Step 3: save goals + persist to SQLite, end conversation."""
        query = update.callback_query
        await query.answer()
        goal_raw = query.data.replace("goal_", "")
        goals = ["Grow Followers", "Make Money", "Build Brand", "Get Brand Deals"] \
            if goal_raw == "All" else [goal_raw]

        niche = context.user_data.get("setup_niche", "")
        audience = context.user_data.get("setup_audience", "")
        chat_id = update.effective_chat.id
        username = update.effective_user.username or update.effective_user.first_name

        if DB_AVAILABLE:
            save_profile(chat_id, username=username, niche=niche,
                         audience_size=audience, goals=goals)

        await query.edit_message_text(
            f"✅ *Profile saved!*\n\n"
            f"Niche: *{niche}*\n"
            f"Audience: *{audience}*\n"
            f"Goals: *{', '.join(goals)}*\n\n"
            "All responses are now personalised for you.\n"
            "Tap a button below to get started:",
            parse_mode="Markdown",
            reply_markup=self._main_menu_keyboard(),
        )
        context.user_data.clear()
        return ConversationHandler.END

    async def setup_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        await update.message.reply_text("Setup cancelled. Run /setup any time to save your profile.")
        return ConversationHandler.END

    # ── /profile ──────────────────────────────────────────────────────────────

    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show the user's saved profile."""
        chat_id = update.effective_chat.id
        profile = self._get_profile(chat_id)

        if not profile or not profile.get("niche"):
            await update.message.reply_text(
                "You don't have a profile yet.\nRun /setup to create one."
            )
            return

        niche = profile.get("niche", "—")
        audience = profile.get("audience_size", "—")
        goals = ", ".join(profile.get("goals", [])) or "—"
        created = (profile.get("created_at") or "")[:10]

        msg = (
            f"👤 *Your Profile*\n\n"
            f"Niche: *{niche}*\n"
            f"Audience: *{audience}*\n"
            f"Goals: *{goals}*\n"
            f"Saved: {created}\n\n"
            "Run /setup to update your profile."
        )
        await update.message.reply_text(msg, parse_mode="Markdown")

    # ── /caption ──────────────────────────────────────────────────────────────

    async def caption_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate a viral caption for a described post."""
        if not context.args:
            await update.message.reply_text(
                "Usage: /caption [describe your post]\n"
                "Example: /caption sunrise hike in the mountains with morning fog"
            )
            return

        desc = " ".join(context.args)
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")
        size = profile.get("audience_size", "")

        await update.message.reply_text(f"✍️ Generating caption for: _{desc}_...", parse_mode="Markdown")
        try:
            result = self.bot.caption_generator(desc, niche=niche, audience_size=size)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            caption = result.get("caption", "")
            cta = result.get("cta", "")
            hashtags = result.get("hashtags", [])
            reach = result.get("estimated_reach", "")

            msg = f"✍️ *Caption*\n\n{escape_md(caption)}\n\n"
            if cta:
                msg += f"📣 *CTA:* {escape_md(cta)}\n\n"
            if hashtags:
                msg += "🏷 *Hashtags:*\n" + " ".join(f"#{h}" for h in hashtags) + "\n\n"
            if reach:
                msg += f"📊 Estimated reach: *{reach}*"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"caption_command error: {e}")

    # ── /hashtags ─────────────────────────────────────────────────────────────

    async def hashtags_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate 30 hashtags in 3 tiers."""
        if not context.args:
            await update.message.reply_text(
                "Usage: /hashtags [topic]\nExample: /hashtags morning workout"
            )
            return

        topic = " ".join(context.args)
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")

        await update.message.reply_text(f"#️⃣ Building hashtag pack for *{topic}*...", parse_mode="Markdown")
        try:
            result = self.bot.hashtag_pack(topic, niche=niche)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            broad = result.get("broad", [])
            niche_tags = result.get("niche", [])
            micro = result.get("micro", [])
            tip = result.get("tip", "")

            msg = f"#️⃣ *Hashtag Pack — {topic}*\n\n"
            msg += f"🌍 *Broad (1M+ posts):*\n{' '.join(f'#{h}' for h in broad)}\n\n"
            msg += f"🎯 *Niche (100K–1M):*\n{' '.join(f'#{h}' for h in niche_tags)}\n\n"
            msg += f"🔬 *Micro (<100K):*\n{' '.join(f'#{h}' for h in micro)}\n\n"
            if tip:
                msg += f"💡 Tip: {tip}"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"hashtags_command error: {e}")

    # ── /bio ──────────────────────────────────────────────────────────────────

    async def bio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """AI-rewrite an Instagram bio."""
        if not context.args:
            await update.message.reply_text(
                "Usage: /bio [your current bio]\n"
                "Example: /bio Personal trainer helping busy moms stay fit"
            )
            return

        current = " ".join(context.args)
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")
        goals = profile.get("goals", [])

        await update.message.reply_text("📝 Optimising your bio...", parse_mode="Markdown")
        try:
            result = self.bot.bio_optimizer(current, niche=niche, goals=goals)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            rewritten = result.get("rewritten_bio", "")
            hook = result.get("hook", "")
            value_prop = result.get("value_prop", "")
            cta = result.get("cta", "")
            keywords = result.get("keywords", [])
            chars = result.get("char_count", len(rewritten))

            msg = f"📝 *Optimised Bio* ({chars}/150 chars)\n\n"
            msg += f"`{escape_md(rewritten)}`\n\n"
            if hook:
                msg += f"🪝 *Hook:* {escape_md(hook)}\n"
            if value_prop:
                msg += f"💎 *Value:* {escape_md(value_prop)}\n"
            if cta:
                msg += f"📣 *CTA:* {escape_md(cta)}\n"
            if keywords:
                msg += f"\n🔑 *Keywords:* {', '.join(keywords)}"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"bio_command error: {e}")

    # ── /ideas ────────────────────────────────────────────────────────────────

    async def ideas_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate a 7-post weekly content calendar."""
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")
        size = profile.get("audience_size", "")

        if not niche:
            await update.message.reply_text(
                "Run /setup first so I can personalise your content calendar.\n"
                "Or use: /content [topic] [style] for a quick caption."
            )
            return

        await update.message.reply_text(
            f"📅 Building your weekly content calendar for *{niche}*...", parse_mode="Markdown"
        )
        try:
            result = self.bot.content_calendar(niche=niche, audience_size=size)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            theme = result.get("week_theme", "")
            posts = result.get("posts", [])
            tip = result.get("pro_tip", "")

            msg = f"📅 *Weekly Content Calendar*\n"
            if theme:
                msg += f"Theme: _{escape_md(theme)}_\n"
            msg += "\n"

            day_emoji = {
                "Monday": "1️⃣", "Tuesday": "2️⃣", "Wednesday": "3️⃣",
                "Thursday": "4️⃣", "Friday": "5️⃣", "Saturday": "6️⃣", "Sunday": "7️⃣",
            }
            for post in posts:
                day = post.get("day", "")
                fmt = post.get("format", "")
                topic = post.get("topic", "")
                angle = post.get("caption_angle", "")
                time_str = post.get("best_time", "")
                emoji = day_emoji.get(day, "•")
                msg += f"{emoji} *{day}* — {fmt}\n"
                msg += f"  {escape_md(topic)}\n"
                if angle:
                    msg += f"  _{escape_md(angle)}_\n"
                if time_str:
                    msg += f"  ⏰ {time_str}\n"
                msg += "\n"

            if tip:
                msg += f"💡 *Tip:* {escape_md(tip)}"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"ideas_command error: {e}")

    # ── /schedule ─────────────────────────────────────────────────────────────

    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get optimal posting schedule."""
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")
        size = profile.get("audience_size", "")

        await update.message.reply_text("⏰ Calculating your optimal posting schedule...")
        try:
            result = self.bot.posting_schedule(niche=niche, audience_size=size)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            best_times = result.get("best_times", [])
            weekly = result.get("weekly_schedule", {})
            freq = result.get("frequency", "")
            tz = result.get("timezone_note", "")
            tip = result.get("pro_tip", "")

            msg = "⏰ *Optimal Posting Schedule*\n\n"
            if freq:
                msg += f"📌 Post *{freq}x per week*\n\n"

            if best_times:
                msg += "🏆 *Best Times to Post:*\n"
                for t in best_times:
                    time_str = t.get("time", "")
                    day_type = t.get("day_type", "")
                    reason = t.get("reason", "")
                    msg += f"• *{time_str}* ({day_type})"
                    if reason:
                        msg += f" — _{escape_md(reason)}_"
                    msg += "\n"
                msg += "\n"

            if weekly:
                msg += "📆 *Weekly Plan:*\n"
                for day, fmt in weekly.items():
                    msg += f"• {day}: {fmt}\n"
                msg += "\n"

            if tz:
                msg += f"🌐 {escape_md(tz)}\n"
            if tip:
                msg += f"\n💡 *Tip:* {escape_md(tip)}"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"schedule_command error: {e}")

    # ── /stories ──────────────────────────────────────────────────────────────

    async def stories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate 5 interactive Story ideas."""
        if not context.args:
            await update.message.reply_text(
                "Usage: /stories [topic]\nExample: /stories morning routine"
            )
            return

        topic = " ".join(context.args)
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")

        await update.message.reply_text(f"📖 Generating Story ideas for *{topic}*...", parse_mode="Markdown")
        try:
            result = self.bot.story_ideas(topic, niche=niche)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            stories = result.get("stories", [])
            hook = result.get("hook_tip", "")

            type_emoji = {
                "Poll": "🗳", "Quiz": "🧠", "Countdown": "⏳",
                "Slider": "💛", "Question Box": "❓", "This or That": "🔀",
            }
            msg = f"📖 *Story Ideas — {topic}*\n\n"
            for i, s in enumerate(stories, 1):
                stype = s.get("type", "Story")
                title = s.get("title", "")
                prompt_text = s.get("prompt", "")
                tip = s.get("engagement_tip", "")
                emoji = type_emoji.get(stype, "•")
                msg += f"{emoji} *{stype} {i}: {escape_md(title)}*\n"
                msg += f"  _{escape_md(prompt_text)}_\n"
                if tip:
                    msg += f"  💡 {escape_md(tip)}\n"
                msg += "\n"

            if hook:
                msg += f"🪝 *First-slide hook tip:* {escape_md(hook)}"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"stories_command error: {e}")

    # ── /audit ────────────────────────────────────────────────────────────────

    async def audit_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Run an advisory profile audit."""
        profile = self._get_profile(update.effective_chat.id)
        niche = profile.get("niche", "")
        size = profile.get("audience_size", "")
        goals = profile.get("goals", [])

        if not niche:
            await update.message.reply_text(
                "Run /setup first so I can audit your profile properly.\n"
                "The more I know about you, the better the audit."
            )
            return

        await update.message.reply_text(f"🔍 Running profile audit for *{niche}*...", parse_mode="Markdown")
        try:
            result = self.bot.profile_audit(niche=niche, audience_size=size, goals=goals)
            if "error" in result:
                await update.message.reply_text(f"❌ {result['error']}")
                return

            score = result.get("score", "?")
            checklist = result.get("checklist", [])
            wins = result.get("quick_wins", [])
            note = result.get("note", "")

            status_emoji = {"Good": "✅", "Needs Work": "⚠️", "Critical": "🔴"}
            msg = f"🔍 *Profile Audit*\n\n📊 Health Score: *{score}/100*\n\n"
            for item in checklist:
                area = item.get("area", "")
                status = item.get("status", "")
                finding = item.get("finding", "")
                action = item.get("action", "")
                icon = status_emoji.get(status, "•")
                msg += f"{icon} *{area}* ({status})\n"
                msg += f"  📋 {escape_md(finding)}\n"
                msg += f"  ➡️ {escape_md(action)}\n\n"

            if wins:
                msg += "⚡ *Quick Wins This Week:*\n"
                for w in wins:
                    msg += f"• {escape_md(w)}\n"
                msg += "\n"

            if note:
                msg += f"_Note: {escape_md(note)}_"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"audit_command error: {e}")

    # ── /design_gift ──────────────────────────────────────────────────────────

    async def design_gift_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /design_gift — Generate personalized gift design concepts."""
        full_text = update.message.text
        text_after_cmd = full_text.replace("/design_gift", "", 1).strip()

        if not text_after_cmd:
            await update.message.reply_text(
                "🎁 *Generate Custom Gift Design Concepts*\n\n"
                "Usage:\n"
                "  `/design_gift [product] \"[concept idea]\"`\n\n"
                "Supported Products:\n"
                "  • t_shirt • mug • hoodie • pillow • poster\n"
                "  • hat • notebook • water_bottle • phone_case • sweater\n\n"
                "Professional Roles (optional):\n"
                "  • ui_ux_designer • graphic_designer • developer • content_creator\n"
                "  • marketer • social_media_manager • photographer • brand_strategist\n"
                "  • product_manager • illustrator • motion_designer\n\n"
                "Examples:\n"
                "• `/design_gift t_shirt \"Motivational quote for gym enthusiasts\"`\n"
                "• `/design_gift mug \"Coffee lover, minimalist style\"`\n"
                "• `/design_gift pillow \"Birthday gift for my best friend\"`\n\n"
                "_Tip: Set your role with `/set_role [role]` to get personalized design guidance!_",
                parse_mode="Markdown",
            )
            return

        # Parse input: product type and concept
        parts = text_after_cmd.split(" ", 1)
        if len(parts) < 2:
            await update.message.reply_text(
                "❌ Please provide: product type and concept idea\n"
                "Example: `/design_gift t_shirt \"Motivational quote for my gym\"`",
                parse_mode="Markdown",
            )
            return

        product_type = parts[0].strip().lower()
        concept_text = parts[1].strip().strip("\"'")

        if len(concept_text) < 5:
            await update.message.reply_text(
                "❌ Concept idea too short. Please provide a more descriptive concept (min 5 characters)"
            )
            return

        await update.message.reply_text(
            f"✨ Generating 3 design concepts for *{product_type}*...\n_(This may take 10-15 seconds)_",
            parse_mode="Markdown",
        )

        try:
            # Get user profile for context
            profile = self._get_profile(update.message.chat_id)
            niche = profile.get("niche", "")
            user_role = profile.get("user_role", "")  # Get saved professional role

            result = await self.orchestrator.execute({
                "command": "/design_gift",
                "action": "generate_concepts",
                "product_type": product_type,
                "concept_idea": concept_text,
                "brand_colors": profile.get("brand_colors", []),
                "tone": profile.get("design_tone", ""),
                "occasion": "",
                "recipient_type": "",
                "user_role": user_role,
                "chat_id": update.message.chat_id,
                "niche": niche,
            })

            if result and result.get("status") == "success":
                await self._handle_gift_design_response(update, result)
            else:
                error_msg = result.get("message") if isinstance(result, dict) else str(result)
                await update.message.reply_text(f"❌ Error: {error_msg}")
                logger.error(f"Gift design failed: {result}")

        except Exception as e:
            await update.message.reply_text(f"❌ Error generating design concepts: {e}")
            logger.error(f"design_gift_command error: {e}")

    async def set_role_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /set_role — Set user's professional role for personalized designs."""
        text_after_cmd = update.message.text.replace("/set_role", "", 1).strip().lower()

        if not text_after_cmd:
            await update.message.reply_text(
                "👤 *Set Your Professional Role*\n\n"
                "Usage: `/set_role [role]`\n\n"
                "Available Roles:\n"
                "• `ui_ux_designer` — UI/UX Design\n"
                "• `graphic_designer` — Graphic Design\n"
                "• `developer` — Web/Software Development\n"
                "• `content_creator` — Content Creation\n"
                "• `marketer` — Marketing\n"
                "• `social_media_manager` — Social Media\n"
                "• `photographer` — Photography\n"
                "• `brand_strategist` — Brand Strategy\n"
                "• `product_manager` — Product Management\n"
                "• `illustrator` — Illustration\n"
                "• `motion_designer` — Motion Design\n\n"
                "Example: `/set_role graphic_designer`\n\n"
                "_Your role personalizes design concepts and recommendations!_",
                parse_mode="Markdown",
            )
            return

        role = text_after_cmd.split()[0].lower()

        # Validate role from the orchestrator
        result = await self.orchestrator.execute({
            "command": "/list_roles",
            "action": "list_roles",
        })

        available_roles = []
        if result and result.get("status") == "success":
            available_roles = [r["key"] for r in result.get("roles", [])]

        if role not in available_roles:
            available_str = ", ".join(available_roles) if available_roles else "ui_ux_designer, graphic_designer, developer..."
            await update.message.reply_text(
                f"❌ Unknown role: `{role}`\n\nAvailable roles: {available_str}",
                parse_mode="Markdown",
            )
            return

        # Get role info and save
        role_result = await self.orchestrator.execute({
            "command": "/design_gift",
            "action": "get_role_info",
            "user_role": role,
        })

        if role_result and role_result.get("status") == "success":
            role_info = role_result.get("role_info", {})
            profile = self._get_profile(update.message.chat_id)
            profile["user_role"] = role
            self._save_profile(update.message.chat_id, profile)

            await update.message.reply_text(
                f"✅ *Role Set: {role_info.get('display_name')}*\n\n"
                f"{role_info.get('emoji')} {role_info.get('guidance')}\n\n"
                f"_Your designs will now be tailored to your {role_info.get('display_name')} expertise!_",
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text(f"❌ Error setting role. Please try again.")

    # ── Universal Prompts Response Handler ────────────────────────────────────────

    async def _handle_universal_prompts_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE, result: dict, category: str):
        """Format and send universal prompt response."""
        try:
            variations = result.get("variations", [])
            if not variations:
                await update.message.reply_text("❌ No prompts generated. Try again.")
                return

            cat_display = category.replace("_", " ").title()
            meta = result.get("meta", {})
            cat_emoji = meta.get("emoji", "🎯")

            header = f"{cat_emoji} *{cat_display}*\n\n"
            header += f"✨ *{len(variations)} Variations*\n"
            header += "─────────────────────────────────────\n\n"

            await update.message.reply_text(header, parse_mode="Markdown")

            # Send each variation with action buttons
            for idx, var in enumerate(variations, 1):
                msg = f"*✨ Variation {idx}*\n"
                msg += "─────────────────────────────────────\n\n"

                if var.get("title"):
                    msg += f"*{escape_md(var['title'])}*\n\n"

                if var.get("style"):
                    msg += f"_Style: {escape_md(var['style'])}_\n\n"

                if var.get("prompt"):
                    msg += f"*Prompt:*\n`{escape_md(var['prompt'][:500])}`\n\n"

                if var.get("negative_prompt"):
                    msg += f"*Negative:* `{escape_md(var['negative_prompt'][:200])}`\n\n"

                if var.get("aspect_ratio"):
                    msg += f"*Aspect Ratio:* `{var['aspect_ratio']}`\n\n"

                if var.get("keywords"):
                    keywords_str = ", ".join(var["keywords"][:8])
                    msg += f"*Keywords:* `{keywords_str}`\n"

                for chunk in self._send_long(msg):
                    await update.message.reply_text(chunk, parse_mode="Markdown")

                # Add action buttons for each prompt
                # Store prompt data in context for later retrieval (Phase 2)
                context.user_data[f"prompt_{idx}"] = {
                    "category": category,
                    "title": var.get("title"),
                    "style": var.get("style"),
                    "prompt": var.get("prompt"),
                    "negative_prompt": var.get("negative_prompt"),
                    "aspect_ratio": var.get("aspect_ratio"),
                    "keywords": var.get("keywords", []),
                }

                action_buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("💾 Save", callback_data=f"save_fav_{idx}"),
                     InlineKeyboardButton("📋 Copy", callback_data=f"copy_prompt_{idx}"),
                     InlineKeyboardButton("✏️ Refine", callback_data=f"refine_prompt_{idx}")],
                ])
                await update.message.reply_text(
                    "👇 Actions:",
                    reply_markup=action_buttons
                )

                if idx < len(variations):
                    await update.message.reply_text("─────────────────────────────────────")

            # Save to history (Phase 2)
            try:
                from src.database.user_db import save_history
                save_history(
                    chat_id=update.effective_chat.id,
                    category=category,
                    user_input=result.get("user_idea", ""),
                    prompt_count=len(variations)
                )
            except Exception as e:
                logger.warning(f"Failed to save history: {e}")

            # Final summary with next steps
            summary = f"✅ Generated {len(variations)} prompt variations!\n\n"
            summary += "*Next Steps:*\n"
            summary += "📋 Copy any prompt and paste into DALL-E 3, Midjourney, or Flux\n"
            summary += "💾 Use [💾 Save] button to save favorites\n"
            summary += "🔄 Use /generate for another category\n"
            summary += "📜 View history: /history"

            summary_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Generate More", callback_data="gen_more"),
                 InlineKeyboardButton("📜 History", callback_data="cmd_history")],
                [InlineKeyboardButton("💾 Favorites", callback_data="cmd_favorites"),
                 InlineKeyboardButton("🏠 Menu", callback_data="back_menu")],
            ])

            await update.message.reply_text(
                summary,
                parse_mode="Markdown",
                reply_markup=summary_buttons
            )

        except Exception as e:
            logger.error(f"Universal prompts formatting error: {e}")
            await update.message.reply_text(f"❌ Error formatting prompts: {e}")

    # ── Legacy Design Brief Response Handler (kept for compatibility) ────────────────────────────────────────

    async def _handle_gift_design_response(self, update: Update, result: dict):
        """Format and send gift design concept response with briefs + image prompts."""
        try:
            concepts = result.get("concepts", [])
            product_type = result.get("product_type", "")
            product_display = result.get("product_display_name", product_type.replace("_", " ").title())
            product_emoji = result.get("product_emoji", "🎁")

            if not concepts:
                await update.message.reply_text("❌ No design concepts generated. Try again.")
                return

            header = f"{product_emoji} *Gift Design Concepts — {product_display}*\n\n"
            header += "✨ *3 Creative Variations with Image Prompts*\n"
            header += "─────────────────────────────────────\n\n"
            await update.message.reply_text(header, parse_mode="Markdown")

            # Send each concept as separate messages
            for idx, concept in enumerate(concepts, 1):
                msg = f"*🎨 Option {idx}: {concept.get('title', 'Design ' + str(idx))}*\n"
                msg += "─────────────────────────────────────\n\n"

                # Design Brief
                brief = concept.get("design_brief", {})
                if brief.get("core_message"):
                    msg += f"*📝 Concept:*\n{escape_md(brief.get('core_message', ''))}\n\n"

                if brief.get("visual_style"):
                    msg += f"*🎨 Visual Style:*\n{escape_md(brief.get('visual_style', ''))}\n\n"

                # Color Palette
                palette = brief.get("color_palette", [])
                if palette:
                    msg += "*🎨 Color Palette:*\n"
                    if isinstance(palette, list):
                        for color in palette[:4]:  # Limit to 4 colors
                            if isinstance(color, dict):
                                color_name = color.get("name", "Color")
                                color_hex = color.get("hex", "#000000")
                            else:
                                color_name = str(color)
                                color_hex = "#000000"
                            msg += f"  • {color_name} ({color_hex})\n"
                    msg += "\n"

                # Typography
                if brief.get("typography"):
                    msg += f"*✍️ Typography:*\n{escape_md(brief.get('typography', ''))}\n\n"

                # Key Elements
                elements = brief.get("key_elements", [])
                if elements:
                    msg += "*🔑 Key Elements:*\n"
                    if isinstance(elements, list):
                        for elem in elements[:5]:
                            msg += f"  • {escape_md(str(elem))}\n"
                    msg += "\n"

                # Design Tip
                if brief.get("design_tip"):
                    msg += f"💡 *Tip:* {escape_md(brief.get('design_tip', ''))}\n\n"

                # Send brief
                for chunk in self._send_long(msg):
                    await update.message.reply_text(chunk, parse_mode="Markdown")

                # Image Prompts
                prompts = concept.get("image_prompts", {})
                dalle_prompt = prompts.get("dalle3", "")
                mj_prompt = prompts.get("midjourney", "")

                if dalle_prompt or mj_prompt:
                    prompt_msg = "🖼️ *Image Generation Prompts:*\n"
                    prompt_msg += "─────────────────────────────────────\n\n"

                    if dalle_prompt:
                        prompt_msg += "*📸 DALL-E 3:*\n"
                        prompt_msg += f"`{dalle_prompt}`\n\n"

                    if mj_prompt:
                        prompt_msg += "*🎨 Midjourney:*\n"
                        prompt_msg += f"`{mj_prompt}`\n\n"

                    prompt_msg += "_Copy either prompt and paste it into DALL-E 3 or Midjourney to generate your design!_\n"

                    for chunk in self._send_long(prompt_msg):
                        await update.message.reply_text(chunk, parse_mode="Markdown")

                # Separator
                if idx < len(concepts):
                    await update.message.reply_text("─────────────────────────────────────")

            # Final message
            summary = f"✅ Generated {len(concepts)} design concepts for your {product_display}!\n\n"
            summary += "🚀 *Next Steps:*\n"
            summary += "1. Copy a prompt from above\n"
            summary += "2. Paste into DALL-E 3 or Midjourney\n"
            summary += "3. Generate and customize your design\n"
            summary += "4. Use for print-on-demand services!\n\n"
            summary += "_Pro tip: Try variations of the concepts to find your perfect design._"
            await update.message.reply_text(summary, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Gift design formatting error: {e}")
            await update.message.reply_text(f"❌ Error formatting design concepts: {e}")

    # ── Design Brief Response Handler ────────────────────────────────────────

    async def _handle_design_brief_response(self, update: Update, result: dict, category: str):
        """Format and send design brief response with all sections."""
        try:
            brief_data = result.get("brief", {})
            briefs = brief_data.get("briefs", [])
            
            if not briefs:
                await update.message.reply_text("❌ No design briefs generated. Try again.")
                return
            
            cat_display = category.replace("_", " ").title()
            header = f"🎨 *Design Brief — {cat_display}*\n\n"
            header += "✨ *3 Creative Variations*\n"
            header += "─────────────────────────────────────\n\n"
            
            await update.message.reply_text(header, parse_mode="Markdown")
            
            # Send each brief as a separate message for clarity
            for idx, brief in enumerate(briefs, 1):
                msg = f"*📋 Option {idx}: {brief.get('title', 'Brief ' + str(idx))}*\n"
                msg += "─────────────────────────────────────\n\n"
                
                # Core Message
                if brief.get("core_message"):
                    msg += f"*📝 Core Message:*\n{escape_md(brief['core_message'])}\n\n"
                
                # Project Requirements
                if brief.get("requirements"):
                    msg += f"*📐 Project Requirements:*\n{escape_md(brief['requirements'])}\n\n"
                
                # Visual Style
                if brief.get("visual_style"):
                    msg += f"*🎨 Visual Style:*\n{escape_md(brief['visual_style'])}\n\n"
                
                # Color Palette
                if brief.get("color_palette"):
                    msg += "*🎨 Color Palette:*\n"
                    palette = brief["color_palette"]
                    if isinstance(palette, list):
                        for color in palette:
                            if isinstance(color, dict):
                                color_name = color.get("name", "Color")
                                color_hex = color.get("hex", "#000000")
                            else:
                                # Handle non-dict items
                                color_name = str(color) if color else "Color"
                                color_hex = "#000000"
                            msg += f"  • {color_name} ({color_hex})\n"
                    else:
                        # If palette itself is not a list, convert to string
                        msg += f"  {escape_md(str(palette))}\n"
                    msg += "\n"
                
                # Typography
                if brief.get("typography"):
                    msg += f"*✍️ Typography:*\n{escape_md(brief['typography'])}\n\n"
                
                # Key Elements
                if brief.get("key_elements"):
                    msg += "*🔑 Key Design Elements:*\n"
                    elements = brief["key_elements"]
                    if isinstance(elements, list):
                        for elem in elements:
                            msg += f"  • {escape_md(elem)}\n"
                    else:
                        msg += f"  {escape_md(str(elements))}\n"
                    msg += "\n"
                
                # Composition
                if brief.get("composition"):
                    msg += f"*📐 Composition & Layout:*\n{escape_md(brief['composition'])}\n\n"
                
                # Deliverables
                if brief.get("deliverables"):
                    msg += f"*📦 Deliverables:*\n{escape_md(brief['deliverables'])}\n\n"
                
                # Tools
                if brief.get("tools"):
                    msg += "*🛠 Recommended Tools:*\n"
                    tools = brief["tools"]
                    if isinstance(tools, list):
                        for tool in tools:
                            msg += f"  • {escape_md(tool)}\n"
                    else:
                        msg += f"  {escape_md(str(tools))}\n"
                    msg += "\n"
                
                # Send brief in chunks if needed
                for chunk in self._send_long(msg):
                    await update.message.reply_text(chunk, parse_mode="Markdown")
                
                # Add separator between briefs
                if idx < len(briefs):
                    await update.message.reply_text("─────────────────────────────────────")
            
            # Final summary
            summary = f"✅ Generated {len(briefs)} design brief variations.\n"
            summary += "Pick the direction that resonates most with your brand! 🎯"
            await update.message.reply_text(summary)
            
        except Exception as e:
            logger.error(f"Design brief formatting error: {e}")
            await update.message.reply_text(f"❌ Error formatting design brief: {e}")

    # ── Inline button router ───────────────────────────────────────────────────

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Route main-menu inline button taps to the relevant command handler."""
        query = update.callback_query
        await query.answer()
        data = query.data

        # Map callback → (handler method, prompt if args needed)
        no_arg_cmds = {
            "cmd_ideas": self.ideas_command,
            "cmd_schedule": self.schedule_command,
            "cmd_audit": self.audit_command,
            "cmd_profile": self.profile_command,
            "cmd_analytics": None,  # handled below
        }
        prompt_cmds = {
            "cmd_caption": ("✍️ Send your post description:", "/caption"),
            "cmd_hashtags": ("#️⃣ Send a topic for hashtags:", "/hashtags"),
            "cmd_bio": ("📝 Paste your current bio:", "/bio"),
            "cmd_stories": ("📖 Send a topic for Story ideas:", "/stories"),
            "cmd_trends": ("📊 Send your niche for trends:", "/trends"),
            "cmd_engagement": ("💬 Send your account size (e.g. micro, small, 10K):", "/engagement"),
            "cmd_monetize": ("💰 Send: [niche] [followers] (e.g. fitness 50000):", "/monetize"),
        }

        # ── Category Selection Callbacks ──
        if data == "cat_select":
            await query.message.reply_text(
                "📷 *Choose a Photo Category:*\n\nSelect the type of prompts you want to generate:",
                reply_markup=self._category_keyboard(),
                parse_mode="Markdown"
            )
        elif data.startswith("gen_"):
            # Extract category from callback (e.g., "gen_women_professional" → "women_professional")
            category = data.replace("gen_", "")
            context.user_data["selected_category"] = category
            await query.message.reply_text(
                f"📷 *{category.replace('_', ' ').title()}*\n\n"
                f"Generating prompts... ⏳",
                parse_mode="Markdown"
            )
            # Create fake update to call generate_command
            fake_update = update
            context.args = [category]
            await self.generate_command(fake_update, context)
        elif data == "back_menu":
            await query.message.reply_text(
                "👋 Back to main menu:",
                reply_markup=self._main_menu_keyboard()
            )
        elif data == "cmd_help":
            await self.help_command(update, context)
        elif data == "gen_more":
            category = context.user_data.get("selected_category", "general_photography")
            await query.message.reply_text(
                f"🔄 Generating more prompts for *{category.replace('_', ' ').title()}*...",
                parse_mode="Markdown"
            )
            fake_update = update
            context.args = [category]
            await self.generate_command(fake_update, context)
        elif data == "see_all_categories":
            await query.message.reply_text(
                "📷 *Available Categories:*",
                reply_markup=self._category_keyboard(),
                parse_mode="Markdown"
            )
        # ── Prompt Action Callbacks (Phase 2) ──
        elif data.startswith("save_fav_"):
            prompt_idx = data.replace("save_fav_", "")
            await query.answer("💾 Saving to favorites...", show_alert=False)
            try:
                from src.database.user_db import save_favorite
                # Get prompt data from context
                prompt_data = context.user_data.get(f"prompt_{prompt_idx}", {})
                if prompt_data and prompt_data.get("prompt"):
                    fav = save_favorite(
                        chat_id=update.effective_chat.id,
                        category=prompt_data.get("category", "general"),
                        prompt=prompt_data.get("prompt"),
                        title=prompt_data.get("title"),
                        style=prompt_data.get("style"),
                        negative_prompt=prompt_data.get("negative_prompt"),
                        aspect_ratio=prompt_data.get("aspect_ratio"),
                        keywords=prompt_data.get("keywords", []),
                    )
                    await query.answer("✅ Saved to favorites!", show_alert=True)
                else:
                    await query.answer("❌ Could not find prompt data", show_alert=True)
            except Exception as e:
                logger.warning(f"Failed to save favorite: {e}")
                await query.answer(f"❌ Error: {str(e)[:50]}", show_alert=True)

        elif data.startswith("copy_prompt_"):
            prompt_idx = data.replace("copy_prompt_", "")
            prompt_data = context.user_data.get(f"prompt_{prompt_idx}", {})
            if prompt_data and prompt_data.get("prompt"):
                # Store for user to copy
                await query.answer("📋 Prompt ready! Copy from above message", show_alert=False)
            else:
                await query.answer("❌ Could not find prompt", show_alert=True)

        elif data.startswith("refine_prompt_"):
            prompt_idx = data.replace("refine_prompt_", "")
            context.user_data["pending_cmd"] = f"/refine {prompt_idx}"
            await query.message.reply_text(
                "✏️ *Refine This Prompt*\n\nDescribe what you'd like to improve or change:"
            )

        # ── Phase 2 Command Callbacks ──
        elif data == "cmd_favorites":
            await self.favorites_command(update, context)
        elif data == "cmd_history":
            await self.history_command(update, context)
        elif data == "cmd_settings":
            await self.settings_command(update, context)
        elif data == "cmd_set_role":
            await self.set_role_command(update, context)

        # ── Phase 3 Callbacks ──
        elif data == "cmd_stats":
            await self.stats_command(update, context)
        elif data == "cmd_recommend":
            await self.recommend_command(update, context)
        elif data == "cmd_regenerate":
            await self.regenerate_command(update, context)

        elif data in no_arg_cmds:
            if data == "cmd_analytics":
                fake_update = update
                context.args = ["daily"]
                await self.analytics_command(fake_update, context)
            else:
                await no_arg_cmds[data](update, context)
        elif data in prompt_cmds:
            prompt_text, cmd = prompt_cmds[data]
            context.user_data["pending_cmd"] = cmd
            await query.message.reply_text(
                f"{prompt_text}\n\n_(or type `{cmd} [your text]` directly)_",
                parse_mode="Markdown",
            )
        else:
            logger.debug(f"[WARN] Unknown callback: {data}")

    # ── prompt library commands ───────────────────────────────────────────────

    async def generate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /generate [category] [level] ["custom concept"] or design brief."""
        # Handle both regular messages and callback-triggered invocations
        if context.args:
            # Called from button callback with category in context.args
            text_after_cmd = " ".join(context.args)
            context.args = None  # Clear for next call
        else:
            # Regular /generate command
            full_text = update.message.text if update.message else ""
            text_after_cmd = full_text.replace("/generate", "", 1).strip()

        # Get the message object (works for both regular messages and callback queries)
        msg_obj = update.message if update.message else (update.callback_query.message if update.callback_query else None)
        if not msg_obj:
            return

        if not text_after_cmd:
            await msg_obj.reply_text(
                "🎨 *Generate Prompts & Design Briefs*\n\n"
                "Usage:\n"
                "  `/generate [category]`\n"
                "  `/generate [category] [level]`\n"
                "  `/generate [category] \"custom concept\"`\n"
                "  `/generate design_posters \"full design content\"`\n\n"
                "Levels: `beginner` 🟢 · `professional` 🔵 · `expert` 🔴\n\n"
                "Examples:\n"
                "• `/generate ui_ux_design professional`\n"
                "• `/generate design_posters \"Diwali sale poster\"`\n"
                "• `/generate design_posters \"🌸 Dream Knot...\"`\n\n"
                "See all categories: /categories",
                parse_mode="Markdown",
            )
            return

        LEVELS = {"beginner", "professional", "expert"}
        DESIGN_CATEGORIES = {"design_posters", "ui_ux_design", "brand_identity", "design_gifts"}
        
        category = text_after_cmd.split()[0].strip().lower()
        remaining = text_after_cmd[len(category):].strip()
        level = None
        custom_prompt = None
        
        if remaining:
            next_tok = remaining.split(" ", 1)[0].lower()
            if next_tok in LEVELS:
                level = next_tok
                remaining = remaining[len(next_tok):].strip()
        
        if remaining:
            custom_prompt = remaining.strip("\"'")

        # Determine if this is a design brief request
        is_design_brief = category in DESIGN_CATEGORIES and custom_prompt

        # Phase 2: Enhanced progress indicator
        cat_display = category.replace("_", " ").title()
        wait_msg = (f"⏳ *Enhancing your concept*\n\n📁 Category: {cat_display}\n🎨 Style: Custom design"
                    if is_design_brief else
                    f"⏳ *Generating AI Prompts*\n\n📁 Category: {cat_display}\n💭 Creating variations...")

        wait_msg_obj = await msg_obj.reply_text(wait_msg, parse_mode="Markdown")

        # Store message ID for potential status update
        context.user_data["progress_msg_id"] = wait_msg_obj.message_id

        try:
            # Get user profile for context
            chat_id = update.effective_chat.id
            profile = self._get_profile(chat_id)
            niche = profile.get("niche", "")

            result = await self.orchestrator.execute({
                "command": "/generate",
                "category": category,
                "custom_prompt": custom_prompt,
                "user_input": custom_prompt,  # For design briefs
                "level": level,
                "chat_id": chat_id,
                "niche": niche,
            })
            # If agent requests clarification, ask user a single question and persist state
            if result and result.get("status") == "clarify":
                question = result.get("question", "Could you clarify your request?")
                await msg_obj.reply_text(f"❓ {question}")
                # Save minimal input to resume after clarification
                pending = {
                    "question": question,
                    "input": {
                        "command": "/generate",
                        "category": category,
                        "custom_prompt": custom_prompt,
                        "user_input": custom_prompt,
                        "level": level,
                        "chat_id": chat_id,
                        "niche": niche,
                    }
                }
                if result.get("clarify_fields"):
                    pending["fields"] = result.get("clarify_fields")
                context.user_data["pending_clarification"] = pending
                return
            
            if result and result.get("status") == "success":
                # Use unified prompt handler for all categories with variations
                if "variations" in result:
                    await self._handle_universal_prompts_response(update, context, result, category)
                # Keep legacy handlers for compatibility with old response shapes
                elif is_design_brief and "brief" in result:
                    await self._handle_design_brief_response(update, result, category)
                elif "concepts" in result:
                    await self._handle_gift_design_response(update, result)
                else:
                    # Fallback for any other response shape
                    await msg_obj.reply_text("❌ Unexpected response format. Please try again.")
                logger.info(f"[OK] /generate category={category}, design_brief={is_design_brief}")
            else:
                err = result.get("error", "Unknown error") if isinstance(result, dict) else str(result)

                # Build better error message with recovery options
                error_msg = "❌ *Couldn't Generate Prompts*\n\n"
                error_msg += f"_Error: {escape_md(err)}_\n\n"
                error_msg += "*Quick Fixes:*\n"
                error_msg += "1️⃣ Try again with a different category\n"
                error_msg += "2️⃣ Check your category name (use /categories)\n"
                error_msg += "3️⃣ Try without custom text\n\n"
                error_msg += "*Recovery Options:*"

                recovery_buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("📚 Browse Categories", callback_data="cat_select"),
                     InlineKeyboardButton("🔄 Retry", callback_data="gen_more")],
                    [InlineKeyboardButton("❓ Get Help", callback_data="cmd_help")],
                ])

                await msg_obj.reply_text(
                    error_msg,
                    parse_mode="Markdown",
                    reply_markup=recovery_buttons
                )
        except Exception as e:
            error_msg = (
                "⚠️ *Something Went Wrong*\n\n"
                f"_Error: {escape_md(str(e)[:100])}_\n\n"
                "*What to do:*\n"
                "• Try /start to return to main menu\n"
                "• Use /help for command guide\n"
                "• Try again in a moment"
            )
            recovery_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Main Menu", callback_data="back_menu"),
                 InlineKeyboardButton("📚 Get Help", callback_data="cmd_help")],
            ])
            await msg_obj.reply_text(
                error_msg,
                parse_mode="Markdown",
                reply_markup=recovery_buttons
            )
            logger.error(f"generate_command error: {e}")

    async def logo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /logo_create key=value flags to generate logo prompts and deliverables."""
            # Example: /logo_create brand_name="Acme Inc" preferred_colors="#ff0000,#00ff00" png_resolution=4000x4000 dpi=300 variant_count=3
            args = context.args or []
            if not args:
                await update.message.reply_text(
                    "Usage: /logo_create brand_name=\"Acme Inc\" preferred_colors=\"#ff0000,#00ff00\" png_resolution=4000x4000 dpi=300 variant_count=3 logo_type=combination",
                    parse_mode="Markdown",
                )
                return

            import shlex
            try:
                toks = shlex.split(" ".join(args))
            except Exception:
                toks = args

            kv = {}
            for t in toks:
                if "=" in t:
                    k, v = t.split("=", 1)
                    kv[k.strip()] = v.strip()

            if not kv:
                kv["brand_name"] = " ".join(args)

            components = {
                "brand_name": kv.get("brand_name", "").strip('"'),
                "tagline": kv.get("tagline", "").strip('"'),
                "industry": kv.get("industry", "").strip('"'),
                "brand_tone": kv.get("brand_tone", "").strip('"'),
                "preferred_colors": kv.get("preferred_colors", "").strip('"'),
                "logo_type": kv.get("logo_type", "combination").strip('"'),
                "variant_count": int(kv.get("variant_count", 3)) if kv.get("variant_count") else 3,
                "png_resolution": kv.get("png_resolution", "4000x4000").strip('"'),
                "dpi": int(kv.get("dpi", 300)) if kv.get("dpi") else 300,
                "background": kv.get("background", "transparent").strip('"'),
                "additional_png_sizes": kv.get("additional_png_sizes", "2000x2000,1024x1024,32x32").strip('"'),
            }

            await update.message.reply_text(f"⏳ Generating logo prompts for *{components['brand_name'] or 'brand'}*...", parse_mode="Markdown")
            try:
                result = await self.orchestrator.execute({
                    "command": "/generate",
                    "category": "logo_create",
                    "components": components,
                    "chat_id": update.message.chat_id,
                    "niche": self._get_profile(update.message.chat_id).get("niche", ""),
                })

                if result and result.get("status") == "success":
                    prompts = result.get("prompts", [])
                    for p in prompts[:3]:
                        text = p.get("prompt") if isinstance(p, dict) else str(p)
                        for chunk in self._send_long(text):
                            await update.message.reply_text(chunk)
                    await update.message.reply_text("✅ Logo prompt generation complete. Review deliverables in the job details.")
                else:
                    await update.message.reply_text(f"❌ Failed to generate logo prompts: {result}")
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {e}")
                logger.error(f"logo_command error: {e}")

    async def categories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all prompt categories with interactive buttons."""
        try:
            msg = (
                "📷 *Prompt Categories*\n\n"
                "Choose a category below to generate AI prompts:\n\n"
                "👇 *Photo Categories:*\n"
                "  • General photography and lifestyle\n"
                "  • Professional portraits (women/men)\n"
                "  • Identity-locked transformations\n"
                "  • Fine art and editorial photography\n\n"
                "👇 *Design Categories:*\n"
                "  • Social media posters\n"
                "  • Gift designs & merchandise\n"
                "  • UI/UX interfaces\n"
                "  • Brand identity & logos\n"
                "  • Illustrations & art\n"
                "  • Animation & motion graphics\n"
                "  • Print design\n\n"
                "💡 *Tap a category below to get started!*"
            )
            await update.message.reply_text(
                msg,
                parse_mode="Markdown",
                reply_markup=self._category_keyboard()
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"categories_command error: {e}")

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search prompts by keyword."""
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
                msg = f"🔍 *Results for \"{keyword}\"* — {result['count']} found\n"
                msg += "─────────────────────────────────\n\n"
                for i, item in enumerate(results[:6], 1):
                    cat = item.get("category", "")
                    preview = item["prompt"][:120] + ("..." if len(item["prompt"]) > 120 else "")
                    msg += f"*{i}.* `{cat}`\n{escape_md(preview)}\n\n"
                msg += f"Use: `/generate {results[0]['category']}`"
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text(
                    f"🔍 No results for *{keyword}*.\n\nTry: /categories", parse_mode="Markdown"
                )
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"search_command error: {e}")

    async def inspire_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate 3 creative angles for a topic."""
        if not context.args:
            await update.message.reply_text(
                "💡 *Inspire Mode*\n\nUsage: `/inspire [topic]`\nExample: `/inspire Indian wedding`",
                parse_mode="Markdown",
            )
            return
        topic = " ".join(context.args)
        await update.message.reply_text(f"💡 Generating angles for *{topic}*...", parse_mode="Markdown")
        try:
            prompt = (
                f'Generate 3 creative visual content angles for: "{topic}"\n\n'
                "For each give:\n1. Angle name (5 words max)\n"
                "2. Best prompt-library category\n"
                "3. One-sentence concept (max 20 words)\n"
                "4. Difficulty: beginner / professional / expert\n\n"
                "Plain text, numbered, max 200 words."
            )
            resp = self.bot.client.chat.completions.create(
                model=self.bot.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=300,
            )
            ideas = resp.choices[0].message.content.strip()
            msg = f"💡 *Creative Angles — {topic}*\n─────────────────────────────────\n\n"
            msg += ideas
            msg += "\n\n─────────────────────────────────\n"
            msg += "Use: `/generate [category] \"concept\"`"
            await update.message.reply_text(msg, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"inspire_command error: {e}")

    # ── PHASE 2: Favorites, History & Settings ───────────────────────────────

    async def favorites_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's saved favorite prompts."""
        try:
            from src.database.user_db import get_user_favorites
            chat_id = update.effective_chat.id
            favorites = get_user_favorites(chat_id, limit=10)

            if not favorites:
                await update.message.reply_text(
                    "💾 *Your Favorites*\n\nNo saved prompts yet.\n\n"
                    "💡 Tip: Use [💾 Save] button when generating prompts to save your favorites!",
                    parse_mode="Markdown",
                    reply_markup=self._main_menu_keyboard()
                )
                return

            msg = f"💾 *Your Favorite Prompts* ({len(favorites)} saved)\n\n"
            msg += "─────────────────────────────────\n\n"

            for idx, fav in enumerate(favorites, 1):
                msg += f"*{idx}. {fav.get('title', 'Prompt')}*\n"
                msg += f"📁 Category: `{fav.get('category')}`\n"
                msg += f"🎨 Style: _{fav.get('style', 'N/A')}_\n"
                msg += f"📝 `{escape_md(fav.get('prompt', '')[:80])}...`\n"
                msg += f"📅 Saved: {fav.get('created_at', 'N/A')[:10]}\n\n"

            msg += "─────────────────────────────────\n"
            msg += "🔄 *Coming Soon:* Copy & use favorite buttons"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")

            await update.message.reply_text(
                "📚 What's next?",
                reply_markup=self._main_menu_keyboard()
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error loading favorites: {e}")
            logger.error(f"favorites_command error: {e}")

    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's prompt generation history."""
        try:
            from src.database.user_db import get_user_history
            chat_id = update.effective_chat.id
            history = get_user_history(chat_id, limit=15)

            if not history:
                await update.message.reply_text(
                    "📜 *Your History*\n\nNo generated prompts yet.\n\n"
                    "💡 Start generating with /generate or tap [📷 Generate Prompts]!",
                    parse_mode="Markdown",
                    reply_markup=self._main_menu_keyboard()
                )
                return

            msg = f"📜 *Recent Generations* ({len(history)} total)\n\n"
            msg += "─────────────────────────────────\n\n"

            for idx, hist in enumerate(history, 1):
                msg += f"*{idx}.* 📁 `{hist.get('category')}`\n"
                if hist.get('user_input'):
                    msg += f"   Input: _{escape_md(hist.get('user_input', '')[:50])}..._\n"
                msg += f"   📅 {hist.get('created_at', 'N/A')[:10]}\n\n"

            msg += "─────────────────────────────────\n"
            msg += "💾 Use [💾 Save] to add to favorites"

            for chunk in self._send_long(msg):
                await update.message.reply_text(chunk, parse_mode="Markdown")

            await update.message.reply_text(
                "📚 What's next?",
                reply_markup=self._main_menu_keyboard()
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error loading history: {e}")
            logger.error(f"history_command error: {e}")

    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show and edit user settings/preferences."""
        try:
            from src.database.user_db import get_profile
            chat_id = update.effective_chat.id
            profile = get_profile(chat_id)

            if not profile:
                await update.message.reply_text(
                    "⚙️ *Settings*\n\nNo profile yet.\n\n"
                    "💡 Tip: Use /setup to create your profile and unlock personalized features!",
                    parse_mode="Markdown",
                )
                return

            niche = profile.get("niche", "Not set")
            audience_size = profile.get("audience_size", "Not set")
            username = profile.get("username", "Not set")

            msg = "⚙️ *Your Settings*\n\n"
            msg += "─────────────────────────────────\n"
            msg += f"👤 *Username:* {username}\n"
            msg += f"🎯 *Niche:* {niche}\n"
            msg += f"📊 *Audience Size:* {audience_size}\n"
            msg += "─────────────────────────────────\n\n"

            msg += "*Customize:*\n"
            msg += "• `/setup` — Edit your profile\n"
            msg += "• `/set_role` — Set your professional role\n\n"

            msg += "*Preferences:*\n"
            msg += "• 🌙 Dark mode (coming soon)\n"
            msg += "• 📬 Notifications (coming soon)\n"
            msg += "• 🌍 Language (coming soon)\n"

            settings_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ Edit Profile", callback_data="cmd_profile"),
                 InlineKeyboardButton("🎯 Set Role", callback_data="cmd_set_role")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="back_menu")],
            ])

            await update.message.reply_text(
                msg,
                parse_mode="Markdown",
                reply_markup=settings_buttons
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error loading settings: {e}")
            logger.error(f"settings_command error: {e}")

    # ── PHASE 3: Smart Analytics & Recommendations ───────────────────────────

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's generation and favorites statistics."""
        try:
            from src.database.user_db import get_generation_stats, get_category_stats
            chat_id = update.effective_chat.id

            stats = get_generation_stats(chat_id)
            cat_stats = get_category_stats(chat_id)

            msg = "📊 *Your AI Generation Stats*\n\n"
            msg += "─────────────────────────────────\n"
            msg += f"📈 *Total Generations:* {stats['total_generations']}\n"
            msg += f"💾 *Total Favorites:* {stats['total_favorites']}\n"
            msg += f"⭐ *Favorite Rate:* {stats['favorite_rate']}\n"
            msg += "─────────────────────────────────\n\n"

            if cat_stats:
                msg += "*🎯 Favorite Categories:*\n"
                for idx, (cat, count) in enumerate(list(cat_stats.items())[:5], 1):
                    cat_display = cat.replace("_", " ").title()
                    msg += f"{idx}. {cat_display}: {count} saved\n"
                msg += "\n"

            most_used = stats.get("favorite_categories", {})
            if most_used:
                msg += "*📈 Most Used Categories:*\n"
                for idx, (cat, count) in enumerate(list(most_used.items())[:5], 1):
                    msg += f"{idx}. {cat.replace('_', ' ').title()}: {count} times\n"

            stats_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 Recommendations", callback_data="cmd_recommend"),
                 InlineKeyboardButton("💾 Favorites", callback_data="cmd_favorites")],
                [InlineKeyboardButton("🏠 Menu", callback_data="back_menu")],
            ])

            await update.message.reply_text(
                msg,
                parse_mode="Markdown",
                reply_markup=stats_buttons
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error loading stats: {e}")
            logger.error(f"stats_command error: {e}")

    async def recommend_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show smart category recommendations based on user history."""
        try:
            from src.database.user_db import get_smart_recommendations, get_most_used_categories
            chat_id = update.effective_chat.id

            recommendations = get_smart_recommendations(chat_id)
            most_used = get_most_used_categories(chat_id, limit=5)

            msg = "🎯 *Recommended For You*\n\n"
            msg += "Based on your generation history, try these categories:\n\n"

            if most_used:
                for idx, (cat, count) in enumerate(most_used, 1):
                    cat_display = cat.replace("_", " ").title()
                    emoji = "👩" if "women" in cat else "👨" if "men" in cat else "🎨"
                    msg += f"{emoji} *{cat_display}*\n"
                    msg += f"   You've generated {count} times\n"
            else:
                msg += "Start generating to get personalized recommendations!\n"

            msg += "\n📝 *Next:*\n"
            msg += "Tap category below or use /generate [category]"

            rec_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Regenerate Last", callback_data="cmd_regenerate"),
                 InlineKeyboardButton("📷 Generate New", callback_data="cat_select")],
                [InlineKeyboardButton("🏠 Menu", callback_data="back_menu")],
            ])

            await update.message.reply_text(
                msg,
                parse_mode="Markdown",
                reply_markup=rec_buttons
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error loading recommendations: {e}")
            logger.error(f"recommend_command error: {e}")

    async def regenerate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Regenerate the user's last generation with one click."""
        try:
            from src.database.user_db import get_last_generation
            chat_id = update.effective_chat.id

            last_gen = get_last_generation(chat_id)

            if not last_gen:
                await update.message.reply_text(
                    "🔄 *Regenerate Last*\n\n"
                    "No previous generations found.\n\n"
                    "💡 Tip: Generate some prompts first with /generate!",
                    parse_mode="Markdown",
                    reply_markup=self._main_menu_keyboard()
                )
                return

            category = last_gen.get("category", "general_photography")
            cat_display = category.replace("_", " ").title()

            msg = f"🔄 *Regenerating*\n\n"
            msg += f"📁 Category: {cat_display}\n"
            msg += f"⏳ Creating 3 new variations..."

            await update.message.reply_text(msg, parse_mode="Markdown")

            # Trigger generation with last category
            fake_update = update
            context.args = [category]
            await self.generate_command(fake_update, context)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"regenerate_command error: {e}")

    # ── free-text chat handler ────────────────────────────────────────────────

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Route free-text messages to Groq chat with profile context."""
        user_text = update.message.text.strip()
        chat_id = update.effective_chat.id
        # First, check if we're waiting for a clarification answer
        pending_clar = context.user_data.get("pending_clarification")
        if pending_clar:
            # Treat this message as the clarification answer
            answer = user_text
            # If pending_clar asked for structured fields, try to parse key:value pairs
            parsed = None
            if pending_clar.get("fields"):
                try:
                    parts = [p.strip() for p in user_text.split(";") if p.strip()]
                    parsed = {}
                    for part in parts:
                        if ":" in part:
                            k, v = part.split(":", 1)
                            parsed[k.strip()] = v.strip()
                    if not parsed:
                        parsed = None
                except Exception:
                    parsed = None
            await update.message.reply_text("✅ Thanks — generating updated prompts...")
            input_data = pending_clar.get("input", {})
            if parsed:
                input_data["clarification_answer"] = parsed
            else:
                input_data["clarification_answer"] = answer
            input_data["clarified"] = True
            try:
                result = await self.orchestrator.execute(input_data)
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {e}")
                context.user_data.pop("pending_clarification", None)
                return

            # Clear pending state
            context.user_data.pop("pending_clarification", None)

            # If generation succeeded, display prompts (simple short-format)
            if result and result.get("status") == "success":
                prompts = result.get("prompts", [])
                msg = "✅ Generated prompts:\n\n"
                for i, p in enumerate(prompts, 1):
                    msg += f"{i}. {p}\n\n"
                for chunk in self._send_long(msg):
                    await update.message.reply_text(chunk, parse_mode="Markdown")
                return
            else:
                err = result.get("error", "Unknown") if isinstance(result, dict) else str(result)
                await update.message.reply_text(f"❌ {err}")
                return

        # Check if waiting for argument after inline button tap
        pending = context.user_data.pop("pending_cmd", None)
        if pending:
            fake_args = user_text.split()
            context.args = fake_args
            dispatch = {
                "/caption": self.caption_command,
                "/hashtags": self.hashtags_command,
                "/bio": self.bio_command,
                "/stories": self.stories_command,
                "/trends": self.trends_command,
                "/engagement": self.engagement_command,
                "/monetize": self.monetize_command,
            }
            if pending in dispatch:
                await dispatch[pending](update, context)
                return

        # Free-text Groq chat
        profile = self._get_profile(chat_id)
        await update.message.reply_text("💬 Thinking...")
        try:
            reply = self.bot.chat_response(user_text, profile=profile)
            for chunk in self._send_long(reply):
                await update.message.reply_text(chunk)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"handle_message error: {e}")

    async def analytics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analytics [daily|weekly|monthly] — show performance report via AnalyticsAgent."""
        logger.info(f"[DEBUG] /analytics from {update.effective_user.username}")

        VALID = {"daily", "weekly", "monthly"}
        report_type = context.args[0].lower() if context.args else "daily"
        if report_type not in VALID:
            report_type = "daily"

        await update.message.reply_text(f"[WAIT] Generating {report_type} analytics report...")

        try:
            result = await self.orchestrator.execute({
                "command": "/analytics",
                "report_type": report_type,
            })


            if result and result.get("status") == "success":
                report = result.get("report", {})
                note = report.get("note", "")
                metrics = report.get("metrics", {})
                period = report.get("period") or report.get("date", "")
                insights = report.get("insights") or report.get("recommendations", [])

                msg = f"📊 *{report_type.title()} Analytics Report*\n"
                if period:
                    msg += f"_{period}_\n"
                if note:
                    msg += f"⚠️ {note}\n"
                msg += "━━━━━━━━━━━━━━━━━━━━━\n\n"

                msg += "📈 *Metrics*\n"
                for key, val in metrics.items():
                    label = key.replace("_", " ").title()
                    if isinstance(val, float) and val < 1:
                        display = f"{val:.1%}"
                    elif isinstance(val, float):
                        display = f"{val:.2f}"
                    else:
                        display = str(val)
                    msg += f"• {label}: {display}\n"

                if insights:
                    msg += "\n💡 *Insights*\n"
                    for tip in insights[:4]:
                        msg += f"• {tip}\n"

                msg += "\n_Use /analytics daily|weekly|monthly_"

                if len(msg) > 4000:
                    await update.message.reply_text(msg[:4000], parse_mode="Markdown")
                    await update.message.reply_text(msg[4000:], parse_mode="Markdown")
                else:
                    await update.message.reply_text(msg, parse_mode="Markdown")

                logger.info(f"[OK] Analytics report generated: {report_type}")
            else:
                await update.message.reply_text(f"[ERROR] Failed to generate report\n{result}")
                logger.error(f"Analytics failed: {result}")

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            logger.error(f"Analytics command error: {e}")




def _build_app(handler: "TelegramBotHandler") -> "Application":
    """Build and configure the Telegram Application with all handlers."""
    app = Application.builder().token(handler.bot_token).build()

    # /setup — multi-step ConversationHandler
    setup_conv = ConversationHandler(
        entry_points=[CommandHandler("setup", handler.setup_start)],
        states={
            SETUP_NICHE: [CallbackQueryHandler(handler.setup_niche, pattern=r"^niche_")],
            SETUP_AUDIENCE: [CallbackQueryHandler(handler.setup_audience, pattern=r"^aud_")],
            SETUP_GOALS: [CallbackQueryHandler(handler.setup_goals, pattern=r"^goal_")],
        },
        fallbacks=[CommandHandler("cancel", handler.setup_cancel)],
        per_user=True,
    )
    app.add_handler(setup_conv)

    # Standard commands
    app.add_handler(CommandHandler("start", handler.start))
    app.add_handler(CommandHandler("help", handler.help_command))
    app.add_handler(CommandHandler("profile", handler.profile_command))
    app.add_handler(CommandHandler("caption", handler.caption_command))
    app.add_handler(CommandHandler("hashtags", handler.hashtags_command))
    app.add_handler(CommandHandler("bio", handler.bio_command))
    app.add_handler(CommandHandler("ideas", handler.ideas_command))
    app.add_handler(CommandHandler("schedule", handler.schedule_command))
    app.add_handler(CommandHandler("stories", handler.stories_command))
    app.add_handler(CommandHandler("audit", handler.audit_command))
    app.add_handler(CommandHandler("design_gift", handler.design_gift_command))
    app.add_handler(CommandHandler("set_role", handler.set_role_command))
    app.add_handler(CommandHandler("content", handler.content_command))
    app.add_handler(CommandHandler("trends", handler.trends_command))
    app.add_handler(CommandHandler("engagement", handler.engagement_command))
    app.add_handler(CommandHandler("monetize", handler.monetize_command))
    app.add_handler(CommandHandler("analytics", handler.analytics_command))
    app.add_handler(CommandHandler("generate", handler.generate_command))
    app.add_handler(CommandHandler("logo_create", handler.logo_command))
    app.add_handler(CommandHandler("categories", handler.categories_command))
    app.add_handler(CommandHandler("search", handler.search_command))
    app.add_handler(CommandHandler("inspire", handler.inspire_command))

    # Inline button callbacks
    app.add_handler(CallbackQueryHandler(handler.button_callback))

    # Free-text handler (must come last)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_message))

    return app


async def main():
    """Main function - Start Telegram bot"""
    if not TELEGRAM_AVAILABLE:
        logger.error("[ERROR] Telegram library not available.")
        return

    try:
        handler = TelegramBotHandler()
    except ValueError as e:
        logger.error(str(e))
        return

    app = _build_app(handler)

    logger.info("[OK] Telegram bot started (polling mode)")
    logger.info("[OK] Bot is waiting for commands...")
    logger.info("[INFO] Press Ctrl+C to stop")

    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            await app.updater.stop()
            await app.stop()


def main_sync():
    """Synchronous wrapper to run the bot using proper event loop handling"""
    if not TELEGRAM_AVAILABLE:
        logger.error("[ERROR] Telegram library not available.")
        return

    try:
        handler = TelegramBotHandler()
    except ValueError as e:
        logger.error(str(e))
        return

    app = _build_app(handler)

    async def error_handler(update, context):
        logger.error(f"[CRITICAL] Telegram error: {context.error}")
        logger.error(f"Update: {update}")

    app.add_error_handler(error_handler)

    logger.info("[OK] Telegram bot started (polling mode)")
    logger.info("[OK] Bot is waiting for commands...")
    logger.info("[INFO] Press Ctrl+C to stop")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("[OK] Bot stopped by user")
    except Exception as e:
        logger.error(f"[ERROR] Bot error: {e}")

