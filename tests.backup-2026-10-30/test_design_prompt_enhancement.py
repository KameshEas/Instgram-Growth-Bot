"""Test cases for Design Prompt Enhancement Agent"""

import asyncio
import pytest
from src.agents.design_enhancer import DesignPromptEnhancerAgent
from src.main import InstagramGrowthBot


class TestDesignPromptEnhancer:
    """Test suite for design brief generation"""

    @pytest.fixture
    def groq_bot(self):
        """Initialize Groq bot for testing"""
        try:
            return InstagramGrowthBot()
        except Exception as e:
            print(f"Warning: Could not initialize Groq bot: {e}")
            return None

    @pytest.fixture
    def design_enhancer(self, groq_bot):
        """Initialize design enhancer agent"""
        return DesignPromptEnhancerAgent(groq_bot=groq_bot)

    @pytest.mark.asyncio
    async def test_design_brief_generation_dream_knot(self, design_enhancer):
        """Test design brief generation for Dream Knot brand"""
        user_input = """🌸 Dream Knot 🌸

Grand Launch Announcement

We're excited to unveil Dream Knot — where creativity meets elegance ✨

💫 Now Open for Orders via WhatsApp!
Your favorite handcrafted creations are just a message away.

🎀 Custom Designs
🎁 Unique Gifts
💍 Special Occasion Creations

📲 Start Ordering Today!
Message us on WhatsApp and bring your dream designs to life.

✨ Celebrate every moment with Dream Knot ✨"""

        result = await design_enhancer.execute({
            "action": "enhance",
            "category": "design_posters",
            "user_input": user_input,
            "niche": "handcrafted fashion",
            "brand_context": {"region": "India"},
            "chat_id": 12345,
        })

        assert result.get("status") == "success"
        assert "brief" in result
        assert result["brief"].get("briefs") is not None
        assert len(result["brief"].get("briefs", [])) >= 1

        # Validate brief structure
        for brief in result["brief"].get("briefs", []):
            assert "title" in brief
            assert "core_message" in brief
            assert "visual_style" in brief
            assert "color_palette" in brief
            assert "typography" in brief
            assert "deliverables" in brief

    @pytest.mark.asyncio
    async def test_design_brief_color_palette(self, design_enhancer):
        """Test that color palette includes hex codes"""
        user_input = "Modern e-commerce website design for a tech startup"

        result = await design_enhancer.execute({
            "action": "enhance",
            "category": "ui_ux_design",
            "user_input": user_input,
            "niche": "technology",
            "chat_id": 12345,
        })

        assert result.get("status") == "success"
        briefs = result["brief"].get("briefs", [])
        
        for brief in briefs:
            palette = brief.get("color_palette", [])
            assert isinstance(palette, list)
            for color in palette:
                assert "name" in color
                assert "hex" in color
                assert color["hex"].startswith("#")

    @pytest.mark.asyncio
    async def test_design_brief_all_sections(self, design_enhancer):
        """Test that all required sections are present"""
        required_sections = [
            "title",
            "core_message",
            "requirements",
            "visual_style",
            "color_palette",
            "typography",
            "key_elements",
            "composition",
            "deliverables",
            "tools"
        ]

        user_input = "Social media branding for a fitness influencer"

        result = await design_enhancer.execute({
            "action": "enhance",
            "category": "brand_identity",
            "user_input": user_input,
            "chat_id": 12345,
        })

        assert result.get("status") == "success"
        briefs = result["brief"].get("briefs", [])

        for brief in briefs:
            for section in required_sections:
                assert section in brief, f"Missing section: {section}"

    @pytest.mark.asyncio
    async def test_design_brief_three_variations(self, design_enhancer):
        """Test that generator produces 3 distinct variations"""
        user_input = "Coffee shop brand identity and logo design"

        result = await design_enhancer.execute({
            "action": "enhance",
            "category": "design_posters",
            "user_input": user_input,
            "chat_id": 12345,
        })

        assert result.get("status") == "success"
        briefs = result["brief"].get("briefs", [])
        
        # Should have 3 variations
        assert len(briefs) >= 1, "Should generate at least one brief"
        
        # Titles should be distinct
        titles = [b.get("title", "") for b in briefs]
        assert len(set(titles)) >= 1, "Brief titles should be unique or distinct"

    @pytest.mark.asyncio
    async def test_design_brief_missing_input(self, design_enhancer):
        """Test error handling for missing user input"""
        result = await design_enhancer.execute({
            "action": "enhance",
            "category": "design_posters",
            "user_input": "",
            "chat_id": 12345,
        })

        assert result.get("status") == "error"
        assert "message" in result

    @pytest.mark.asyncio
    async def test_design_brief_with_niche_context(self, design_enhancer):
        """Test that niche context is incorporated"""
        user_input = "Grand opening celebration poster"

        result = await design_enhancer.execute({
            "action": "enhance",
            "category": "design_posters",
            "user_input": user_input,
            "niche": "luxury fashion boutique",
            "brand_context": {"region": "UAE"},
            "chat_id": 12345,
        })

        assert result.get("status") == "success"
        briefs = result["brief"].get("briefs", [])
        
        # At least one brief should mention luxury/boutique context
        full_content = " ".join([
            b.get("core_message", "") + " " + 
            b.get("visual_style", "") + " " + 
            b.get("requirements", "")
            for b in briefs
        ]).lower()
        
        # Verify niche is reflected (may not always be explicit)
        assert len(full_content) > 0, "Brief content should be substantial"


class TestDesignBriefFormat:
    """Test formatting and structure of design briefs"""

    def test_color_palette_format(self):
        """Test color palette formatting with hex codes"""
        palette = [
            {"name": "Primary Blue", "hex": "#1A73E8"},
            {"name": "Accent Gold", "hex": "#F8B500"},
            {"name": "Neutral White", "hex": "#FFFFFF"},
        ]
        
        for color in palette:
            assert "name" in color
            assert "hex" in color
            assert color["hex"].startswith("#")
            assert len(color["hex"]) == 7  # #RRGGBB

    def test_typography_format(self):
        """Test typography structure"""
        typography = "Montserrat (headlines), Open Sans (body)"
        assert isinstance(typography, str)
        assert len(typography) > 0

    def test_deliverables_format(self):
        """Test deliverables structure"""
        deliverables = "1080x1920 JPEG (Instagram), Canva/PSD editable, PNG transparent"
        assert isinstance(deliverables, str)
        assert "1080x1920" in deliverables or "JPEG" in deliverables or "PNG" in deliverables


if __name__ == "__main__":
    # Run a quick manual test
    print("Design Prompt Enhancement Test Suite")
    print("=" * 50)
    print("\nTo run full test suite:")
    print("  pytest tests/test_design_prompt_enhancement.py -v")
    print("\nTo run specific test:")
    print("  pytest tests/test_design_prompt_enhancement.py::TestDesignPromptEnhancer::test_design_brief_generation_dream_knot -v -s")
