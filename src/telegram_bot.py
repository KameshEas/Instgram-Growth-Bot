#!/usr/bin/env python3
"""
Telegram Bot Interface for Instagram Growth Bot
Access AI agents via Telegram commands (/content, /trends, /engagement, /monetize)
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from the .env file in the telegram-insta-bot directory
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    # Try parent directory if not found
    env_path_alt = Path(__file__).parent.parent.parent / ".env"
    if env_path_alt.exists():
        load_dotenv(dotenv_path=str(env_path_alt))

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
        text = f"Welcome to Instagram Growth Bot, {user.first_name}! 🎯\n\n"
        text += "Available Commands:\n\n"
        text += "📝 /content [topic] [style]\n"
        text += "   Generate viral-optimized Instagram captions\n"
        text += "   Example: /content fitness transformation motivational\n\n"
        text += "�️ /generate [category]\n"
        text += "   Generate image prompts from professional library\n"
        text += "   Example: /generate women_professional\n\n"
        text += "�📊 /trends [niche]\n"
        text += "   Analyze trending topics and hashtags\n"
        text += "   Example: /trends fitness\n\n"
        text += "👥 /engagement [size]\n"
        text += "   Get engagement strategy and daily targets\n"
        text += "   Example: /engagement micro\n\n"
        text += "💰 /monetize [niche] [followers]\n"
        text += "   Discover monetization strategies and revenue projections\n"
        text += "   Example: /monetize fitness 50000\n\n"
        text += "❓ /help - Show detailed help\n"
        
        await update.message.reply_text(text)
        logger.info(f"[OK] User {user.id} ({user.username}) started bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        logger.info(f"[DEBUG] /help command received from {update.effective_user.username}")
        text = "How to use Instagram Growth Bot:\n\n"
        text += "1. CONTENT GENERATION\n"
        text += "   /content [topic] [style]\n"
        text += "   Styles: engaging, motivational, humorous, inspirational\n"
        text += "   Example: /content fitness_transformation motivational\n\n"
        text += "2. IMAGE GENERATION PROMPTS\n"
        text += "   /generate [category]\n"
        text += "   Categories: general_photography, women_professional, women_transform, men_professional, men_transform, couples_general, couples_transform, design_posters, reel_scripts, captions_templates, email_subjects\n"
        text += "   Example: /generate women_professional\n"
        text += "   Returns: 3 professional prompts to use with DALL-E, Midjourney, Stable Diffusion\n\n"
        text += "3. TREND ANALYSIS\n"
        text += "   /trends [niche]\n"
        text += "   Example: /trends fitness\n"
        text += "   Returns: Top 5 trending topics with viral potential scores\n\n"
        text += "4. ENGAGEMENT STRATEGY\n"
        text += "   /engagement [size]\n"
        text += "   Sizes: micro (5K-100K), small (100K-500K), medium (500K+)\n"
        text += "   Example: /engagement micro\n"
        text += "   Returns: Daily targets, comment templates, timing\n\n"
        text += "5. MONETIZATION IDEAS\n"
        text += "   /monetize [niche] [follower_count]\n"
        text += "   Example: /monetize fitness 50000\n"
        text += "   Returns: Revenue streams, pricing, projections\n\n"
        text += "Tips:\n"
        text += "• Use underscores for multi-word inputs\n"
        text += "• Wait 2-5 seconds for AI to generate response\n"
        text += "• Each command calls Groq AI (fast, free, reliable)\n"
        
        await update.message.reply_text(text)
    
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
            
            if result and "trending_topics" in result:
                msg = f"✅ Trending topics in {niche}:\n\n"
                
                for i, topic in enumerate(result.get("trending_topics", [])[:5], 1):
                    topic_name = topic.get("topic") or topic.get("hashtag", "N/A")
                    viral_potential = topic.get("viral_potential", "N/A")
                    msg += f"{i}. {topic_name}\n   Viral Potential: {viral_potential}%\n\n"
                
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
        """Handle /generate command - Get image generation prompts"""
        logger.info(f"[DEBUG] /generate command received from {update.effective_user.username}")
        
        # Get the full command text and remove the /generate command itself
        full_text = update.message.text
        text_after_command = full_text.replace("/generate", "", 1).strip()
        
        if not text_after_command:
            await update.message.reply_text(
                "Usage: /generate [category]\n"
                "Or: /generate [category] \"Your custom prompt here\"\n\n"
                "Available categories:\n"
                "• general_photography\n"
                "• women_professional\n"
                "• women_transform\n"
                "• men_professional\n"
                "• men_transform\n"
                "• couples_general\n"
                "• couples_transform\n"
                "• design_posters\n"
                "• reel_scripts\n"
                "• captions_templates\n"
                "• email_subjects\n\n"
                "Examples:\n"
                "/generate women_professional\n"
                '/generate design_posters "A surreal visual of intertwined glowing threads..."\n'
                "/generate reel_scripts \"30-second video about...\""
            )
            return
        
        # Split to get category and custom prompt
        parts = text_after_command.split(" ", 1)
        category = parts[0].strip().lower()
        custom_prompt = None
        
        # Check if custom prompt is provided (looks for quoted text)
        if len(parts) > 1:
            custom_text = parts[1].strip()
            # Remove quotes if present
            if (custom_text.startswith('"') and custom_text.endswith('"')) or \
               (custom_text.startswith("'") and custom_text.endswith("'")):
                custom_prompt = custom_text[1:-1]
            elif custom_text.startswith('"') or custom_text.startswith("'"):
                # Handle case where quote might span multiple words
                custom_prompt = custom_text[1:]
                if custom_prompt.endswith('"') or custom_prompt.endswith("'"):
                    custom_prompt = custom_prompt[:-1]
        
        # Use custom prompt or library prompts
        if custom_prompt:
            await update.message.reply_text(f"[WAIT] Processing custom prompt for '{category}'...")
        else:
            await update.message.reply_text(f"[WAIT] Generating prompts for '{category}'...")
        
        try:
            result = self.bot.image_generation_prompts(category=category, custom_prompt=custom_prompt)
            
            if result and result.get("status") == "success":
                prompts = result.get("prompts", [])
                is_custom = result.get("custom", False)
                
                if is_custom:
                    # For custom prompts, send in a more compact format
                    prompt_text = prompts[0]
                    
                    # Split at structural boundaries to avoid mid-sentence cuts
                    def split_smart(text, max_len=3800):
                        """Split text intelligently at structural boundaries"""
                        if len(text) <= max_len:
                            return [text]
                        
                        parts = []
                        current_part = ""
                        
                        # Split on multiple structural markers
                        lines = text.split("\n")
                        
                        for line in lines:
                            # If adding this line would exceed limit, start new part
                            if len(current_part) + len(line) + 2 > max_len:
                                if current_part.strip():
                                    parts.append(current_part.strip())
                                current_part = line + "\n"
                            else:
                                current_part += line + "\n"
                        
                        if current_part.strip():
                            parts.append(current_part.strip())
                        
                        return parts if parts else [text]
                    
                    prompt_parts = split_smart(prompt_text, max_len=3500)  # More conservative limit
                    
                    # Send first part with header (check combined length)
                    header = f"✅ Custom Prompt - {result.get('category')}:\n\n"
                    first_msg = header + prompt_parts[0]
                    
                    # If combined header + first part exceeds limit, send header separately
                    if len(first_msg) > 4000:
                        await update.message.reply_text(header)
                        await update.message.reply_text(prompt_parts[0])
                    else:
                        await update.message.reply_text(first_msg)
                    
                    # Send remaining parts if any
                    for part in prompt_parts[1:]:
                        if len(part) > 0:
                            await update.message.reply_text(part)
                    
                    # Send footer with usage info
                    footer = f"\n💡 Ready to use with: DALL-E 3, Midjourney, Stable Diffusion\n"
                    footer += f"📚 Available: {', '.join(result.get('available_categories', []))}"
                    await update.message.reply_text(footer)
                    
                else:
                    # For library prompts, use original format
                    msg = f"✅ Image Generation Prompts - {result.get('category')}:\n\n"
                    
                    for i, prompt in enumerate(prompts, 1):
                        msg += f"{i}. {prompt}\n\n"
                    
                    msg += "💡 Tip: Use these with DALL-E 3, Midjourney, or Stable Diffusion\n"
                    msg += f"📚 Or provide custom: /generate {result.get('category')} \"your prompt\""
                    
                    categories_str = ", ".join(result.get('available_categories', []))
                    msg += f"\n📚 Available: {categories_str}"
                    
                    # Smart split for long messages
                    if len(msg) > 4000:
                        # Try to split at newline boundaries
                        lines = msg.split("\n")
                        current_msg = ""
                        
                        for line in lines:
                            if len(current_msg) + len(line) + 1 <= 3800:
                                current_msg += line + "\n"
                            else:
                                if current_msg:
                                    await update.message.reply_text(current_msg.strip())
                                current_msg = line + "\n"
                        
                        if current_msg:
                            await update.message.reply_text(current_msg.strip())
                    else:
                        await update.message.reply_text(msg)
                
                logger.info(f"[OK] Generated prompts for: {category}")
            else:
                error_msg = result.get("error", "Unknown error")
                categories = result.get("available_categories", [])
                
                msg = f"[ERROR] {error_msg}\n\n"
                if categories:
                    msg += f"Available categories:\n"
                    for cat in categories:
                        msg += f"• {cat}\n"
                
                await update.message.reply_text(msg)
                logger.error(f"Prompt generation failed: {result}")
        
        except Exception as e:
            await update.message.reply_text(f"[ERROR] {str(e)}")
            logger.error(f"Generate command error: {e}")


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
