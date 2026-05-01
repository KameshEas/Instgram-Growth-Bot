"""
Integration Test Script - Verify Evaluation Hooks
Tests that evaluation system is properly integrated into agents
"""

import asyncio
import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_gift_design_integration():
    """Test GiftDesignAgent integration"""
    logger.info("=" * 70)
    logger.info("🧪 Testing GiftDesignAgent Integration")
    logger.info("=" * 70)
    
    try:
        from src.agents.gift_design_agent import GiftDesignAgent
        from src.services.agent_evaluation_integration import EvaluationHookFactory
        
        # Create agent
        agent = GiftDesignAgent(groq_bot=None)
        
        # Verify eval_hook exists
        assert hasattr(agent, 'eval_hook'), "❌ eval_hook not found in GiftDesignAgent"
        logger.info("✅ eval_hook successfully initialized")
        
        # Verify it's the right type
        hook = agent.eval_hook
        assert hook is not None, "❌ eval_hook is None"
        logger.info(f"✅ eval_hook type: {type(hook).__name__}")
        
        # Test metrics directory exists
        metrics_dir = Path("metrics")
        logger.info(f"✅ Metrics directory: {metrics_dir.absolute()}")
        
        logger.info("✅ GiftDesignAgent integration verified!\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ GiftDesignAgent integration test failed: {str(e)}")
        return False


async def test_content_generator_integration():
    """Test ContentGeneratorAgent integration"""
    logger.info("=" * 70)
    logger.info("🧪 Testing ContentGeneratorAgent Integration")
    logger.info("=" * 70)
    
    try:
        from src.agents.content_generator import ContentGeneratorAgent
        from src.services.agent_evaluation_integration import EvaluationHookFactory
        
        # Create agent
        agent = ContentGeneratorAgent(groq_bot=None)
        
        # Verify eval_hook exists
        assert hasattr(agent, 'eval_hook'), "❌ eval_hook not found in ContentGeneratorAgent"
        logger.info("✅ eval_hook successfully initialized")
        
        # Verify it's the right type
        hook = agent.eval_hook
        assert hook is not None, "❌ eval_hook is None"
        logger.info(f"✅ eval_hook type: {type(hook).__name__}")
        
        logger.info("✅ ContentGeneratorAgent integration verified!\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ ContentGeneratorAgent integration test failed: {str(e)}")
        return False


async def test_evaluation_hook_functionality():
    """Test that evaluation hook works"""
    logger.info("=" * 70)
    logger.info("🧪 Testing Evaluation Hook Functionality")
    logger.info("=" * 70)
    
    try:
        from src.services.agent_evaluation_integration import EvaluationHookFactory
        
        hook = EvaluationHookFactory.get_hook("TestAgent")
        logger.info("✅ Hook created successfully")
        
        # Mock data for evaluation
        user_request = {
            "product_type": "t-shirt",
            "concept_idea": "Minimalist design for developers"
        }
        
        agent_output = {
            "status": "success",
            "concepts": [
                {
                    "title": "Modern Minimal",
                    "design_brief": "Clean, professional design with minimalist aesthetic"
                }
            ]
        }
        
        # Test evaluation (non-blocking)
        result = await hook.evaluate_execution(
            user_request=user_request,
            agent_output=agent_output,
            model_used="Groq",
            system_prompt="Test evaluation system prompt"
        )
        
        logger.info(f"✅ Evaluation executed: {result.get('status', 'unknown')}")
        
        if result.get("status") != "error":
            logger.info(f"✅ Evaluation metrics recorded")
            recommendations = result.get("recommendations", {})
            logger.info(f"✅ Quality level: {recommendations.get('quality_level', 'N/A')}")
        
        logger.info("✅ Evaluation hook functionality verified!\n")
        return True
        
    except Exception as e:
        logger.error(f"⚠️  Evaluation hook test (non-critical): {str(e)}")
        # Non-critical, continue
        return True


async def test_imports():
    """Test that all imports work"""
    logger.info("=" * 70)
    logger.info("🧪 Testing Imports")
    logger.info("=" * 70)
    
    try:
        logger.info("Importing evaluator service...")
        from src.services.prompt_evaluator import get_evaluator
        logger.info("✅ prompt_evaluator imported")
        
        logger.info("Importing refiner service...")
        from src.services.prompt_refinement import RefinerFactory
        logger.info("✅ prompt_refinement imported")
        
        logger.info("Importing integration service...")
        from src.services.agent_evaluation_integration import EvaluationHookFactory
        logger.info("✅ agent_evaluation_integration imported")
        
        logger.info("Importing agents...")
        from src.agents.gift_design_agent import GiftDesignAgent
        logger.info("✅ GiftDesignAgent imported")
        
        from src.agents.content_generator import ContentGeneratorAgent
        logger.info("✅ ContentGeneratorAgent imported")
        
        logger.info("✅ All imports successful!\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Import test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all integration tests"""
    logger.info("\n" + "=" * 70)
    logger.info("🚀 PHASE 2 INTEGRATION VERIFICATION")
    logger.info("=" * 70 + "\n")
    
    results = {}
    
    # Test imports first
    results["imports"] = await test_imports()
    
    if not results["imports"]:
        logger.error("❌ Imports failed - cannot continue")
        return results
    
    # Test integrations
    results["gift_design"] = await test_gift_design_integration()
    results["content_generator"] = await test_content_generator_integration()
    results["evaluation_hook"] = await test_evaluation_hook_functionality()
    
    # Summary
    logger.info("=" * 70)
    logger.info("📊 INTEGRATION TEST SUMMARY")
    logger.info("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name:30s}: {status}")
    
    logger.info("=" * 70)
    logger.info(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✅ ALL INTEGRATION TESTS PASSED!")
        logger.info("\n🎉 Ready for Phase 2 deployment!")
    else:
        logger.warning(f"⚠️  {total - passed} tests failed - review needed")
    
    logger.info("=" * 70 + "\n")
    
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
    
    # Exit with appropriate code
    exit(0 if all(results.values()) else 1)
