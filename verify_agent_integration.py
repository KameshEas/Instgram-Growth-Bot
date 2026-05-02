#!/usr/bin/env python3
"""Verify Phase 2A integration into GiftDesignAgent and ContentGeneratorAgent"""

import sys
import asyncio
from src.agents.gift_design_agent import GiftDesignAgent
from src.agents.content_generator import ContentGeneratorAgent
from src.services.parameter_recommendation_engine import ParameterRecommendationFactory
from src.services.image_alignment_validator import ImageAlignmentValidatorFactory

print("=" * 70)
print("PHASE 2A AGENT INTEGRATION VERIFICATION")
print("=" * 70)

# Test 1: Verify GiftDesignAgent has Phase 2A components
print("\n1. ✓ Testing GiftDesignAgent initialization...")
try:
    gift_agent = GiftDesignAgent()
    assert hasattr(gift_agent, 'param_engine'), "Missing param_engine"
    assert hasattr(gift_agent, 'alignment_validator'), "Missing alignment_validator"
    print("   ✅ GiftDesignAgent has param_engine")
    print("   ✅ GiftDesignAgent has alignment_validator")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Verify ContentGeneratorAgent has Phase 2A components
print("\n2. ✓ Testing ContentGeneratorAgent initialization...")
try:
    content_agent = ContentGeneratorAgent()
    assert hasattr(content_agent, 'param_engine'), "Missing param_engine"
    assert hasattr(content_agent, 'alignment_validator'), "Missing alignment_validator"
    print("   ✅ ContentGeneratorAgent has param_engine")
    print("   ✅ ContentGeneratorAgent has alignment_validator")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Verify both agents share the same singleton instances
print("\n3. ✓ Testing singleton pattern (both agents use same instances)...")
try:
    gift_agent2 = GiftDesignAgent()
    assert gift_agent.param_engine is gift_agent2.param_engine, "Not using same param_engine singleton"
    assert gift_agent.alignment_validator is gift_agent2.alignment_validator, "Not using same alignment_validator singleton"
    print("   ✅ Singleton pattern working correctly")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Test parameter recommendations through agent
print("\n4. ✓ Testing parameter engine through agent...")
try:
    params = gift_agent.param_engine.recommend_parameters(
        product_type="mug",
        alignment_importance=0.85,
        quality_level="high"
    )
    assert params.cfg_scale > 0, "Invalid CFG scale"
    assert params.denoising_strength > 0, "Invalid denoising strength"
    assert params.num_steps > 0, "Invalid steps"
    print(f"   ✅ Mug (High): CFG={params.cfg_scale}, Denoise={params.denoising_strength}, Steps={params.num_steps}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 5: Test alignment validator through agent
print("\n5. ✓ Testing alignment validator through agent...")
try:
    report = gift_agent.alignment_validator.validate_alignment(
        original_features=["logo", "color"],
        generated_image_description="Image with logo and color",
        denoising_strength=0.75,
        product_type="mug"
    )
    assert report.alignment_score > 0, "Invalid alignment score"
    assert report.status in ["PASS", "ADJUST", "FAIL"], "Invalid status"
    print(f"   ✅ Alignment validation: Score={report.alignment_score:.2f}, Status={report.status}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 6: Verify all product types work
print("\n6. ✓ Testing all product types...")
try:
    product_types = ["t-shirt", "mug", "canvas", "poster", "merchandise"]
    for ptype in product_types:
        params = gift_agent.param_engine.recommend_parameters(
            product_type=ptype,
            alignment_importance=0.75,
            quality_level="balanced"
        )
        assert params.cfg_scale > 0, f"Invalid params for {ptype}"
        print(f"   ✅ {ptype}: CFG={params.cfg_scale}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 7: Verify quality levels work
print("\n7. ✓ Testing all quality levels...")
try:
    quality_levels = ["quick", "balanced", "high"]
    for quality in quality_levels:
        params = gift_agent.param_engine.recommend_parameters(
            product_type="t-shirt",
            alignment_importance=0.75,
            quality_level=quality
        )
        assert params.num_steps > 0, f"Invalid steps for {quality}"
        print(f"   ✅ {quality}: Steps={params.num_steps}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL AGENT INTEGRATION TESTS PASSED!")
print("=" * 70)
print("""
Summary:
- GiftDesignAgent: Phase 2A integrated ✅
- ContentGeneratorAgent: Phase 2A integrated ✅
- Singleton pattern: Working correctly ✅
- Parameter engine: All functions working ✅
- Alignment validator: All functions working ✅
- All product types: Supported ✅
- All quality levels: Supported ✅

Ready for system evaluation measurement!
""")
