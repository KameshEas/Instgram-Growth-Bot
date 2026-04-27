from typing import Dict, Any, List, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from datetime import datetime, timedelta
import random
import requests
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
import logging

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot

logger = logging.getLogger(__name__)


class TrendsAgent(BaseAgent):
    """Detect trending topics from real-world APIs (Reddit, GitHub, etc.) and
    enrich them with AI analysis via Groq.

    When a ``groq_bot`` is supplied the ``analyze_for_niche`` action combines
    live scraped trends with an AI-structured response (topHashtags,
    bestPostingTimes) that the Telegram handler already knows how to render.
    """

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("Trends")
        self._groq_bot = groq_bot
        
        # Fallback topics in case APIs fail
        self.fallback_topics = [
            "#trending",
            "#viral",
            "#contentcreator",
            "#socialmedia",
            "#instagram",
            "#reels",
            "#growth",
            "#explore",
            "#creative",
            "#photography",
            "#lifestyle",
            "#motivation",
            "#business",
            "#digitalmarketing",
            "#tips",
        ]
        
        # Cache for trends (to avoid hitting APIs too frequently)
        self.trends_cache = {}
        self.cache_expiry = timedelta(hours=6)
        self.last_fetch = {}
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache is still valid"""
        if key not in self.last_fetch:
            return False
        return datetime.now() - self.last_fetch[key] < self.cache_expiry
    
    async def _fetch_reddit_trends(self) -> List[str]:
        """Fetch trending topics from Reddit"""
        try:
            # Reddit popular posts (no API key required for basic access)
            url = "https://www.reddit.com/r/trending.json"
            headers = {"User-Agent": "PhotographyBot/1.0"}
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                trends = []
                
                # Extract trending subreddit topics
                for post in data.get("data", {}).get("children", [])[:10]:
                    try:
                        title = post["data"]["title"]
                        subreddit = post["data"]["subreddit"]
                        # Extract hashtag-like terms from titles
                        words = title.split()
                        for word in words:
                            if len(word) > 3 and not word.startswith("http"):
                                trends.append(f"#{word[:20]}")  # Limit length
                        trends.append(f"#{subreddit}")
                    except:
                        pass
                
                return trends[:15] if trends else self.fallback_topics
        except Exception as e:
            logger.warning(f"Reddit trends fetch failed: {str(e)}")
        
        return self.fallback_topics
    
    async def _fetch_github_trends(self) -> List[str]:
        """Fetch trending repositories from GitHub"""
        if not BS4_AVAILABLE:
            return []
        try:
            url = "https://github.com/trending"
            headers = {"User-Agent": "PhotographyBot/1.0"}

            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                trends = []
                
                # Extract trending repo names
                for repo in soup.select("h2 a")[:10]:
                    try:
                        repo_name = repo.get("href", "").strip("/").split("/")[-1]
                        if repo_name:
                            trends.append(f"#{repo_name}")
                    except:
                        pass
                
                return trends[:10] if trends else []
        except Exception as e:
            logger.warning(f"GitHub trends fetch failed: {str(e)}")
        
        return []
    
    async def _fetch_news_topics(self) -> List[str]:
        """Fetch trending news topics"""
        if not BS4_AVAILABLE:
            return []
        try:
            # Using Hacker News as proxy for real-time trends
            url = "https://news.ycombinator.com/"
            headers = {"User-Agent": "PhotographyBot/1.0"}

            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                trends = []
                
                # Extract top story titles
                for story in soup.select(".titleline > a")[:8]:
                    try:
                        title = story.get_text()
                        words = title.split()[:2]  # Take first 2 words
                        trend = " ".join(words)
                        if len(trend) > 3:
                            trends.append(f"#{trend[:20]}")
                    except:
                        pass
                
                return trends[:8] if trends else []
        except Exception as e:
            logger.warning(f"News topics fetch failed: {str(e)}")
        
        return []
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trends detection"""
        try:
            action = input_data.get("action", "detect")

            if action == "analyze_for_niche":
                return await self._analyze_for_niche(input_data)
            elif action == "detect":
                return await self._detect_trends(input_data)
            elif action == "trending_hashtags":
                return await self._get_trending_hashtags(input_data)
            elif action == "content_suggestions":
                return await self._suggest_content(input_data)
            elif action == "viral_forecast":
                return await self._forecast_viral_content(input_data)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        
        except Exception as e:
            self.logger.error(f"Trends error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _analyze_for_niche(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Combine live web trends with AI analysis for a specific niche.

        Steps:
        1. Scrape all real-time trends (Reddit / GitHub / HN) into combined list.
        2. Pass the full scraped list to Groq so AI reasons from real data.
        Falls back to raw scrape result when Groq is unavailable.
        """
        niche = data.get("niche", "photography")
        region = data.get("region", "")
        try:
            # Step 1 — collect all scraped data first
            reddit_trends = await self._fetch_reddit_trends()
            github_trends = await self._fetch_github_trends()
            news_trends = await self._fetch_news_topics()
            combined_scraped: List[str] = reddit_trends + github_trends + news_trends

            # Step 2 — AI analysis from scraped data
            if self._groq_bot:
                try:
                    ai_result = self._groq_bot.analyze_trends(
                        niche=niche,
                        region=region,
                        scraped_trends=combined_scraped,
                    )
                    if isinstance(ai_result, dict) and ai_result:
                        ai_result["agent"] = "TrendsAgent"
                        await self.log_execution(data, ai_result, "success")
                        return ai_result
                except Exception as e:
                    self.logger.warning(f"Groq trends fallback triggered: {e}")

            # Fallback — return raw scraped data
            fallback = {
                "status": "success",
                "niche": niche,
                "agent": "TrendsAgent",
                "real_web_trends": combined_scraped[:20],
                "note": "AI unavailable — showing raw scraped trends only",
            }
            await self.log_execution(data, fallback, "success")
            return fallback

        except Exception as e:
            self.logger.error(f"Analyze for niche error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _detect_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect current trending topics from real APIs"""
        try:
            # Check cache first
            cache_key = "trends_detect"
            if self._is_cache_valid(cache_key):
                cached_trends = self.trends_cache.get(cache_key)
                if cached_trends:
                    return {
                        "status": "success",
                        "action": "detect",
                        "source": "cache",
                        "trending": cached_trends,
                        "detected_at": datetime.utcnow().isoformat(),
                        "cache_expires_in": str(self.cache_expiry)
                    }
            
            # Fetch from real APIs
            trends = {}
            
            # Get Reddit trends
            reddit_trends = await self._fetch_reddit_trends()
            trends["reddit"] = reddit_trends
            
            # Get GitHub trends
            github_trends = await self._fetch_github_trends()
            if github_trends:
                trends["github"] = github_trends
            
            # Get news trends
            news_trends = await self._fetch_news_topics()
            if news_trends:
                trends["news"] = news_trends
            
            # Cache the results
            self.trends_cache[cache_key] = trends
            self.last_fetch[cache_key] = datetime.now()
            
            return {
                "status": "success",
                "action": "detect",
                "source": "live_apis",
                "trending": trends,
                "detected_at": datetime.utcnow().isoformat(),
                "note": "Trends fetched from Reddit, GitHub, and News sources"
            }
        except Exception as e:
            self.logger.error(f"Trend detection error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _get_trending_hashtags(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get trending hashtags for niche — AI classifies tiers from scraped data."""
        try:
            niche = data.get("niche", "photography")
            region = data.get("region", "")

            # Collect scraped data
            trends_response = await self._detect_trends({})
            all_trends: List[str] = []
            if trends_response.get("status") == "success":
                trending = trends_response.get("trending", {})
                for topics in trending.values():
                    all_trends.extend(topics)
            if not all_trends:
                all_trends = self.fallback_topics

            # AI classifies and categorises
            if self._groq_bot:
                try:
                    ai_result = self._groq_bot.analyze_trends(
                        niche=niche, region=region, scraped_trends=all_trends,
                    )
                    if isinstance(ai_result, dict) and ai_result.get("trending_hashtags"):
                        await self.log_execution(data, ai_result, "success")
                        return {
                            "status": "success",
                            "action": "trending_hashtags",
                            "niche": niche,
                            **ai_result,
                        }
                except Exception as e:
                    self.logger.warning(f"Groq hashtag fallback: {e}")

            # Fallback — return raw list uncategorised
            return {
                "status": "success",
                "action": "trending_hashtags",
                "niche": niche,
                "hashtags": {"all": list(set(all_trends))[:30]},
                "note": "AI unavailable — unclassified scraped hashtags",
                "detected_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Hashtag fetch error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _suggest_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest content based on current trends — AI-generated when Groq is available."""
        try:
            trend = data.get("trend", "")
            niche = data.get("niche", "")
            region = data.get("region", "")

            if self._groq_bot:
                try:
                    result = self._groq_bot.generate_content_ideas(
                        trends=[trend] if trend else [],
                        niche=niche,
                        region=region,
                    )
                    if isinstance(result, dict) and result:
                        result["action"] = "content_suggestions"
                        await self.log_execution(data, result, "success")
                        return result
                except Exception as e:
                    self.logger.warning(f"Groq content ideas fallback: {e}")

            return {
                "status": "unavailable",
                "action": "content_suggestions",
                "message": "AI is currently unavailable. Please try again shortly.",
                "generated_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Content suggestion error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _forecast_viral_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Forecast virality potential of content ideas — AI-powered."""
        try:
            content_idea = data.get("content_idea", "")
            niche = data.get("niche", "")
            account_stage = data.get("account_stage", "")
            region = data.get("region", "")

            if self._groq_bot:
                try:
                    result = self._groq_bot.forecast_viral_potential(
                        content_idea=content_idea,
                        niche=niche,
                        account_stage=account_stage,
                        region=region,
                    )
                    if isinstance(result, dict) and result:
                        result["action"] = "viral_forecast"
                        await self.log_execution(data, result, "success")
                        return result
                except Exception as e:
                    self.logger.warning(f"Groq viral forecast fallback: {e}")

            return {
                "status": "unavailable",
                "action": "viral_forecast",
                "message": "AI is currently unavailable. Please try again shortly.",
                "generated_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Viral forecast error: {str(e)}")
            return {"status": "error", "error": str(e)}
