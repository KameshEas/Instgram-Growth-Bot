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
        """Return the 4-row inline button main menu."""
        buttons = [
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
        """Handle /help command — show updated command reference."""
        text = (
            "📖 *Instagram Growth Advisor — Commands*\n\n"
            "⚙️ *Profile Setup*\n"
            "  /setup — Set your niche, audience & goals\n"
            "  /profile — View or edit your saved profile\n\n"
            "✍️ *Content Creation*\n"
            "  /caption `[describe your post]` — Viral caption + CTA\n"
            "  /hashtags `[topic]` — 30 hashtags in 3 tiers\n"
            "  /bio `[your current bio]` — AI-rewritten bio\n"
            "  /stories `[topic]` — 5 interactive Story ideas\n\n"
            "📅 *Planning*\n"
            "  /ideas — 7-post weekly content calendar\n"
            "  /schedule — Best posting times for your audience\n\n"
            "📊 *Growth & Analytics*\n"
            "  /trends `[niche]` — Trending topics & hashtags\n"
            "  /engagement `[size]` — Engagement strategy\n"
            "  /monetize `[niche] [followers]` — Revenue ideas\n"
            "  /analytics `[daily|weekly|monthly]` — Performance report\n"
            "  /audit — Profile improvement checklist\n\n"
            "🎨 *Prompt Library*\n"
            "  /generate `[category]` — AI image prompts\n"
            "  /categories — Browse all prompt categories\n"
            "  /search `[keyword]` — Find prompts by keyword\n"
            "  /inspire `[topic]` — 3 creative content angles\n\n"
            "💬 *Free-text chat*\n"
            "  Just type any question — I'll answer as your Instagram coach!\n\n"
            "💡 Tip: Run /setup first for personalised responses."
        )
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
                    for color in brief["color_palette"]:
                        color_name = color.get("name", "Color")
                        color_hex = color.get("hex", "#000000")
                        msg += f"  • {color_name} ({color_hex})\n"
                    msg += "\n"
                
                # Typography
                if brief.get("typography"):
                    msg += f"*✍️ Typography:*\n{escape_md(brief['typography'])}\n\n"
                
                # Key Elements
                if brief.get("key_elements"):
                    msg += "*🔑 Key Design Elements:*\n"
                    for elem in brief["key_elements"]:
                        msg += f"  • {escape_md(elem)}\n"
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
                    for tool in brief["tools"]:
                        msg += f"  • {escape_md(tool)}\n"
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

        if data in no_arg_cmds:
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
        full_text = update.message.text
        text_after_cmd = full_text.replace("/generate", "", 1).strip()

        if not text_after_cmd:
            await update.message.reply_text(
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
        DESIGN_CATEGORIES = {"design_posters", "ui_ux_design", "brand_identity"}
        
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

        wait_msg = (f"⏳ Enhancing your concept for *{category}*..."
                    if is_design_brief else
                    f"⏳ Fetching prompts for *{category}*{' [' + level + ']' if level else ' [mixed]'}...")
        await update.message.reply_text(wait_msg, parse_mode="Markdown")

        try:
            # Get user profile for context
            profile = self._get_profile(update.message.chat_id)
            niche = profile.get("niche", "")
            
            result = await self.orchestrator.execute({
                "command": "/generate",
                "category": category,
                "custom_prompt": custom_prompt,
                "user_input": custom_prompt,  # For design briefs
                "level": level,
                "chat_id": update.message.chat_id,
                "niche": niche,
            })
            
            if result and result.get("status") == "success":
                # Check if this is a design brief response
                if is_design_brief and "brief" in result:
                    await self._handle_design_brief_response(update, result, category)
                else:
                    # Standard prompt response
                    prompts = result.get("prompts", [])
                    is_custom = result.get("custom", False)
                    meta = result.get("meta", {})
                    cat_emoji = meta.get("emoji", "🎯")
                    tools = ", ".join(meta.get("tools", [])) or "DALL-E 3, Midjourney, Stable Diffusion"
                    best_for = meta.get("best_for", "")
                    res_level = result.get("level", level or "mixed")
                    level_labels = {"beginner": "🟢 Beginner", "professional": "🔵 Professional",
                                    "expert": "🔴 Expert", "mixed": "🌈 Mixed Levels"}
                    if is_custom:
                        msg = f"{cat_emoji} *Custom Prompt — {category}*\n"
                        if best_for:
                            msg += f"_{best_for}_\n"
                        msg += "─────────────────────\n\n"
                        msg += escape_md(prompts[0]) if prompts else "No prompt returned."
                        msg += f"\n\n🛠 Tools: {tools}"
                    else:
                        msg = f"{cat_emoji} *{category}* — {level_labels.get(res_level, res_level)}\n"
                        if best_for:
                            msg += f"_{best_for}_\n"
                        msg += "─────────────────────\n\n"
                        for i, p in enumerate(prompts, 1):
                            display = strip_transform_boilerplate(p) if category in _TRANSFORM_CATEGORIES else p
                            msg += f"*Prompt {i}:*\n{escape_md(display)}\n\n"
                        msg += f"─────────────────────\n🛠 Tools: {tools}\n"
                        msg += f"💡 Custom: `/generate {category} \"your concept\"`"
                    for chunk in self._send_long(msg):
                        await update.message.reply_text(chunk, parse_mode="Markdown")
                logger.info(f"[OK] /generate category={category}, design_brief={is_design_brief}")
            else:
                err = result.get("error", "Unknown") if isinstance(result, dict) else str(result)
                cats = result.get("available_categories", []) if isinstance(result, dict) else []
                rep = f"❌ {err}\n\nSee all categories: /categories"
                if cats:
                    rep += "\n\n" + "\n".join(f"• {c}" for c in cats[:10])
                await update.message.reply_text(rep)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            logger.error(f"generate_command error: {e}")

    async def categories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all prompt categories."""
        try:
            from src.prompts.templates import list_categories
            cats = list_categories()
            msg = "📚 *Prompt Categories*\n\n"
            msg += "\n".join(f"• `{c}`" for c in cats)
            msg += "\n\nUsage: `/generate [category]`"
            await update.message.reply_text(msg, parse_mode="Markdown")
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

    # ── free-text chat handler ────────────────────────────────────────────────

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Route free-text messages to Groq chat with profile context."""
        user_text = update.message.text.strip()
        chat_id = update.effective_chat.id

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
    app.add_handler(CommandHandler("content", handler.content_command))
    app.add_handler(CommandHandler("trends", handler.trends_command))
    app.add_handler(CommandHandler("engagement", handler.engagement_command))
    app.add_handler(CommandHandler("monetize", handler.monetize_command))
    app.add_handler(CommandHandler("analytics", handler.analytics_command))
    app.add_handler(CommandHandler("generate", handler.generate_command))
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

