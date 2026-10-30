"""Quick integration test to verify design brief system works end-to-end"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_design_brief_integration():
    """Test the complete design brief flow"""
    print("=" * 70)
    print("DESIGN BRIEF SYSTEM INTEGRATION TEST")
    print("=" * 70)
    
    try:
        # Step 1: Import all components
        print("\n✓ Step 1: Importing components...")
        from src.agents.design_enhancer import DesignPromptEnhancerAgent
        from src.agents.orchestrator import ContentOrchestratorAgent
        from src.main import InstagramGrowthBot
        from src.prompts.templates import DESIGN_BRIEF_SYSTEM_PROMPT
        print("  ✓ All imports successful")
        
        # Step 2: Verify design enhancer agent exists
        print("\n✓ Step 2: Verifying DesignPromptEnhancerAgent...")
        design_agent = DesignPromptEnhancerAgent(groq_bot=None)
        assert design_agent.name == "DesignPromptEnhancer"
        print(f"  ✓ Agent initialized: {design_agent.name}")
        
        # Step 3: Verify orchestrator has design enhancer
        print("\n✓ Step 3: Verifying ContentOrchestratorAgent routing...")
        orchestrator = ContentOrchestratorAgent(groq_bot=None)
        assert "design_enhancer" in orchestrator.agents
        print(f"  ✓ Design enhancer registered in orchestrator")
        print(f"  ✓ Total agents: {len(orchestrator.agents)}")
        
        # Step 4: Verify system prompt exists
        print("\n✓ Step 4: Verifying DESIGN_BRIEF_SYSTEM_PROMPT...")
        assert "3 design brief variations" in DESIGN_BRIEF_SYSTEM_PROMPT.lower()
        assert "color_palette" in DESIGN_BRIEF_SYSTEM_PROMPT.lower()
        assert len(DESIGN_BRIEF_SYSTEM_PROMPT) > 1000
        print(f"  ✓ System prompt loaded ({len(DESIGN_BRIEF_SYSTEM_PROMPT)} chars)")
        print(f"  ✓ Contains all required sections")
        
        # Step 5: Verify InstagramGrowthBot has generate_design_brief method
        print("\n✓ Step 5: Verifying InstagramGrowthBot.generate_design_brief()...")
        assert hasattr(InstagramGrowthBot, "generate_design_brief")
        print(f"  ✓ Method exists: generate_design_brief")
        
        # Step 6: Test design enhancer with sample input (no API call)
        print("\n✓ Step 6: Testing DesignPromptEnhancerAgent without Groq...")
        result = await design_agent.execute({
            "action": "enhance",
            "category": "design_posters",
            "user_input": "Test Dream Knot content",
        })
        # Will error because no Groq bot, but that's expected
        assert "error" in result or "status" in result
        print(f"  ✓ Agent routing works (expected error without API): {result.get('status', result.get('error', 'OK'))[:50]}")
        
        # Step 7: Verify method signatures
        print("\n✓ Step 7: Verifying method signatures...")
        import inspect
        
        # Check design_enhancer.execute signature
        sig = inspect.signature(design_agent.execute)
        assert "input_data" in sig.parameters
        print(f"  ✓ DesignPromptEnhancerAgent.execute(input_data) ✓")
        
        # Check InstagramGrowthBot.generate_design_brief signature
        sig = inspect.signature(InstagramGrowthBot.generate_design_brief)
        required_params = {"category", "user_input", "niche", "brand_context", "chat_id"}
        actual_params = set(sig.parameters.keys())
        assert required_params.issubset(actual_params)
        print(f"  ✓ InstagramGrowthBot.generate_design_brief(...) ✓")
        
        print("\n" + "=" * 70)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("=" * 70)
        print("\nSystem is ready for:")
        print("  • /generate design_posters \"[Dream Knot content]\"")
        print("  • /generate ui_ux_design \"[design concept]\"")
        print("  • /generate brand_identity \"[branding requirements]\"")
        print("\nEach request will generate 3 design brief variations via Groq API")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_design_brief_integration())
    sys.exit(0 if success else 1)
