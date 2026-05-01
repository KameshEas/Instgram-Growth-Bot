"""Unit Tests for GiftDesignAgent"""

import asyncio
import pytest
from src.agents.gift_design_agent import GiftDesignAgent
from src.prompts.templates import (
    list_gift_products,
    get_gift_product_meta,
    get_all_tones,
    GIFT_PRODUCTS,
    GIFT_DESIGN_TONES,
)


@pytest.fixture
def agent():
    """Create GiftDesignAgent instance for testing"""
    return GiftDesignAgent(groq_bot=None)


class TestGiftDesignAgentBasics:
    """Test basic GiftDesignAgent functionality"""

    def test_agent_initialization(self, agent):
        """Test agent initializes correctly"""
        assert agent is not None
        assert agent.name == "GiftDesign"
        assert agent.products == list_gift_products()
        assert agent.tones == get_all_tones()

    def test_products_available(self, agent):
        """Test all products are loaded"""
        products = agent.products
        assert "t_shirt" in products
        assert "mug" in products
        assert "hoodie" in products
        assert "pillow" in products
        assert "poster" in products
        assert len(products) >= 10


class TestGiftProductMetadata:
    """Test gift product metadata functions"""

    def test_get_gift_product_meta(self):
        """Test getting metadata for each product"""
        for product in list_gift_products():
            meta = get_gift_product_meta(product)
            assert meta is not None
            assert "emoji" in meta
            assert "display_name" in meta
            assert "printable_area" in meta
            assert "constraints" in meta
            assert "best_for" in meta
            assert "tools" in meta

    def test_unknown_product_returns_default(self):
        """Test unknown product returns sensible defaults"""
        meta = get_gift_product_meta("unknown_product")
        assert meta["emoji"] == "🎁"
        assert meta["display_name"] == "Custom Gift"
        assert "tools" in meta


class TestDesignTones:
    """Test design tone functionality"""

    def test_all_tones_have_descriptions(self):
        """Test all tones have descriptions"""
        for tone in get_all_tones():
            from src.prompts.templates import get_tone_description
            desc = get_tone_description(tone)
            assert desc is not None
            assert len(desc) > 0
            assert tone in GIFT_DESIGN_TONES

    def test_tone_variations(self):
        """Test that we have diverse tone options"""
        tones = get_all_tones()
        expected_tones = [
            "minimalist", "playful", "elegant", "sporty", "vintage",
            "artistic", "professional", "nature", "tech", "romantic"
        ]
        for expected in expected_tones:
            assert expected in tones, f"Expected tone '{expected}' not found"


@pytest.mark.asyncio
async def test_list_products_action(agent):
    """Test list_products action"""
    result = await agent._list_products({})
    assert result["status"] == "success"
    assert "products" in result
    assert len(result["products"]) >= 10
    assert result["action"] == "list_products"


@pytest.mark.asyncio
async def test_list_tones_action(agent):
    """Test list_tones action"""
    result = await agent._list_tones({})
    assert result["status"] == "success"
    assert "tones" in result
    assert len(result["tones"]) >= 10
    assert result["action"] == "list_tones"


@pytest.mark.asyncio
async def test_get_product_specs_action(agent):
    """Test get_product_specs action"""
    result = await agent._get_product_specs({
        "product_type": "t_shirt"
    })
    assert result["status"] == "success"
    assert result["product_type"] == "t_shirt"
    assert "specifications" in result
    assert "emoji" in result["specifications"]


@pytest.mark.asyncio
async def test_missing_required_fields(agent):
    """Test error handling for missing required fields"""
    # Missing product_type
    result = await agent._generate_design_concepts({
        "concept_idea": "A nice design"
    })
    assert result["status"] == "error"
    assert "product_type is required" in result["message"]

    # Missing concept_idea
    result = await agent._generate_design_concepts({
        "product_type": "t_shirt"
    })
    assert result["status"] == "error"
    assert "concept_idea is required" in result["message"]


@pytest.mark.asyncio
async def test_invalid_product_type(agent):
    """Test error handling for invalid product type"""
    result = await agent._generate_design_concepts({
        "product_type": "invalid_product",
        "concept_idea": "A nice design for my t-shirt"
    })
    assert result["status"] == "error"
    assert "Unknown product type" in result["message"]


@pytest.mark.asyncio
async def test_short_concept_idea_rejected(agent):
    """Test that short concept ideas are rejected"""
    result = await agent._generate_design_concepts({
        "product_type": "mug",
        "concept_idea": "ok"  # Too short
    })
    assert result["status"] == "error"
    assert "descriptive" in result["message"].lower()


@pytest.mark.asyncio
async def test_execute_with_unknown_action(agent):
    """Test execute with unknown action"""
    result = await agent.execute({
        "action": "unknown_action"
    })
    assert result["status"] == "error"
    assert "Unknown action" in result["message"]


class TestProductSpecifications:
    """Test product specifications are properly defined"""

    def test_tshirt_specs(self):
        """Test t-shirt specifications"""
        meta = get_gift_product_meta("t_shirt")
        assert "1000x1200" in meta["printable_area"].lower()
        assert meta["emoji"] == "👕"

    def test_mug_specs(self):
        """Test mug specifications"""
        meta = get_gift_product_meta("mug")
        assert "wrap" in meta["constraints"].lower() or "cylindrical" in meta["constraints"].lower()
        assert meta["emoji"] == "☕"

    def test_poster_specs(self):
        """Test poster specifications"""
        meta = get_gift_product_meta("poster")
        assert "18x24" in meta["printable_area"] or "4320x5760" in meta["printable_area"]
        assert meta["emoji"] == "🖼️"

    def test_all_products_have_tools(self):
        """Test all products have recommended tools"""
        for product in list_gift_products():
            meta = get_gift_product_meta(product)
            assert isinstance(meta["tools"], list)
            assert len(meta["tools"]) > 0
            # Should support at least DALL-E 3 or Midjourney
            tools_str = " ".join(meta["tools"]).lower()
            assert "dall-e" in tools_str or "midjourney" in tools_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
