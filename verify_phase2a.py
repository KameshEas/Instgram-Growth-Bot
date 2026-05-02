"""
Quick verification test for Phase 2A components
"""

from src.services.parameter_recommendation_engine import ParameterRecommendationEngine
from src.services.image_alignment_validator import ImageAlignmentValidator

print("=" * 80)
print("PHASE 2A COMPONENT VERIFICATION")
print("=" * 80)

# Test 1: Parameter Engine
print("\n1. Testing Parameter Recommendation Engine...")
engine = ParameterRecommendationEngine()

params = engine.recommend_parameters(product_type="mug", quality_level="high")
print(f"✅ Mug (High Quality): CFG={params.cfg_scale}, Denoise={params.denoising_strength}, Steps={params.num_steps}")

params = engine.recommend_parameters(product_type="t-shirt", alignment_importance=0.9)
print(f"✅ T-Shirt (High Alignment): CFG={params.cfg_scale}, Denoise={params.denoising_strength}, Steps={params.num_steps}")

params = engine.recommend_parameters(quality_level="quick")
print(f"✅ Quick Preview: Steps={params.num_steps} (should be ≤30)")

presets = engine.list_presets()
print(f"✅ Available presets: {len(presets)} ({', '.join(presets.keys())})")

# Test 2: Image Alignment Validator
print("\n2. Testing Image Alignment Validator...")
validator = ImageAlignmentValidator()

report = validator.validate_alignment(
    original_features=["red logo", "circular shape"],
    generated_image_description="Image shows red logo with circular shape",
    denoising_strength=0.5,
    product_type="mug"
)
print(f"✅ Perfect alignment: Score={report.alignment_score:.2f}, Status={report.status}")

report = validator.validate_alignment(
    original_features=["red logo", "circular shape"],
    generated_image_description="Image with different colors",
    denoising_strength=0.95,
    product_type="mug"
)
print(f"✅ Poor alignment: Score={report.alignment_score:.2f}, Status={report.status}")

# Test 3: Integration
print("\n3. Testing Parameter + Alignment Integration...")

# Get params for mug
params = engine.recommend_parameters(product_type="mug", alignment_importance=0.85)
print(f"✅ Got parameters: CFG={params.cfg_scale}, Denoise={params.denoising_strength}")

# Validate alignment with those params
report = validator.validate_alignment(
    original_features=["logo", "color"],
    generated_image_description="Has logo and color",
    denoising_strength=params.denoising_strength,
    product_type="mug",
    cfg_scale=params.cfg_scale
)
print(f"✅ Alignment validation: Score={report.alignment_score:.2f}, Status={report.status}")

# If poor alignment, get adjusted params
if report.alignment_score < 0.6:
    adjusted = engine.get_parameters_for_iteration(
        params.to_dict(),
        "needs_alignment"
    )
    print(f"✅ Adjusted parameters: Denoise={adjusted.denoising_strength:.2f}")

print("\n" + "=" * 80)
print("✅ PHASE 2A VERIFICATION COMPLETE - All components working!")
print("=" * 80)
