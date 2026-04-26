from typing import Dict, Any, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from datetime import datetime
import random

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class MonetizationAgent(BaseAgent):
    """Revenue stream advice and monetization tracking.

    When a ``groq_bot`` is supplied the agent uses Groq for real AI-generated
    revenue ideas.  Falls back to simulated dashboard data otherwise.
    """

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("Monetization")
        self._groq_bot = groq_bot
        self.revenue_streams = [
            "sponsored_posts",
            "affiliate_marketing",
            "digital_products",
            "email_list",
            "saas_links",
            "engagement_services"
        ]
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute monetization tracking"""
        try:
            action = input_data.get("action", "track")

            if action == "ideas_for_niche":
                return await self._ideas_for_niche(input_data)
            elif action == "track_revenue":
                return await self._track_revenue(input_data)
            elif action == "affiliate_link":
                return await self._add_affiliate_link(input_data)
            elif action == "sponsored_deal":
                return await self._track_sponsored_post(input_data)
            elif action == "digital_product":
                return await self._add_digital_product(input_data)
            elif action == "email_campaign":
                return await self._track_email_campaign(input_data)
            elif action == "dashboard":
                return await self._get_monetization_dashboard(input_data)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        
        except Exception as e:
            self.logger.error(f"Monetization error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _ideas_for_niche(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """AI-generated monetization ideas for a specific niche and audience size.

        Delegates to ``groq_bot.monetization_ideas()`` when available so
        suggestions are personalised and AI-powered instead of random numbers.
        Falls back to the simulated dashboard if Groq is unavailable.
        """
        niche = data.get("niche", "general")
        follower_count = int(data.get("follower_count", 10000))
        if self._groq_bot:
            try:
                result = self._groq_bot.monetization_ideas(
                    niche=niche, follower_count=follower_count
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq monetization fallback triggered: {e}")
        # Static fallback
        return await self._get_monetization_dashboard(data)

    async def _track_revenue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Track revenue from all streams"""
        try:
            revenue_breakdown = {
                "sponsored_posts": random.uniform(500, 2000),
                "affiliate_marketing": random.uniform(200, 800),
                "digital_products": random.uniform(300, 1500),
                "email_list": random.uniform(100, 500),
                "saas_links": random.uniform(50, 300),
                "engagement_services": random.uniform(0, 400)
            }
            
            total_revenue = sum(revenue_breakdown.values())
            
            return {
                "status": "success",
                "action": "track_revenue",
                "revenue_breakdown": revenue_breakdown,
                "total_revenue": round(total_revenue, 2),
                "currency": "USD",
                "tracked_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Revenue tracking error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _add_affiliate_link(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add and track affiliate link"""
        try:
            link_data = {
                "platform": data.get("platform", "amazon"),
                "product": data.get("product", "unknown"),
                "commission_rate": data.get("commission_rate", 0.05),
                "created_at": datetime.utcnow().isoformat(),
                "clicks": 0,
                "conversions": 0,
                "revenue": 0.0
            }
            
            return {
                "status": "success",
                "action": "affiliate_link",
                "link": link_data,
                "message": f"Affiliate link added for {data.get('platform')}"
            }
        except Exception as e:
            self.logger.error(f"Affiliate link error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _track_sponsored_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Track sponsored post deal"""
        try:
            deal_data = {
                "brand": data.get("brand", "Unknown Brand"),
                "deal_amount": data.get("deal_amount", 0),
                "post_count": data.get("post_count", 1),
                "posting_deadline": data.get("deadline", "TBD"),
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            }
            
            return {
                "status": "success",
                "action": "sponsored_deal",
                "deal": deal_data,
                "message": f"Sponsored deal with {data.get('brand')} tracked"
            }
        except Exception as e:
            self.logger.error(f"Sponsored post error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _add_digital_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add digital product for sale"""
        try:
            product_data = {
                "name": data.get("name", "New Product"),
                "type": data.get("type", "e-book"),
                "price": data.get("price", 0),
                "platform": data.get("platform", "gumroad"),
                "url": data.get("url", ""),
                "created_at": datetime.utcnow().isoformat(),
                "sales": 0,
                "revenue": 0.0
            }
            
            return {
                "status": "success",
                "action": "digital_product",
                "product": product_data,
                "message": f"Digital product '{data.get('name')}' added"
            }
        except Exception as e:
            self.logger.error(f"Digital product error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _track_email_campaign(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Track email campaign performance"""
        try:
            campaign_data = {
                "campaign_name": data.get("name", "Campaign"),
                "subscriber_count": data.get("subscriber_count", 0),
                "open_rate": random.uniform(0.2, 0.4),
                "click_rate": random.uniform(0.05, 0.15),
                "conversion_rate": random.uniform(0.02, 0.08),
                "revenue": random.uniform(50, 500),
                "created_at": datetime.utcnow().isoformat()
            }
            
            return {
                "status": "success",
                "action": "email_campaign",
                "campaign": campaign_data,
                "message": f"Email campaign tracked"
            }
        except Exception as e:
            self.logger.error(f"Email campaign error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _get_monetization_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get full monetization dashboard"""
        try:
            # Calculate projected monthly revenue
            daily_revenue = sum([random.uniform(50, 200) for _ in range(6)])
            monthly_projected = daily_revenue * 30
            yearly_projected = monthly_projected * 12
            
            return {
                "status": "success",
                "action": "dashboard",
                "daily_revenue": round(daily_revenue, 2),
                "monthly_projected": round(monthly_projected, 2),
                "yearly_projected": round(yearly_projected, 2),
                "active_streams": len(self.revenue_streams),
                "revenue_streams": self.revenue_streams,
                "last_updated": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Dashboard error: {str(e)}")
            return {"status": "error", "error": str(e)}
