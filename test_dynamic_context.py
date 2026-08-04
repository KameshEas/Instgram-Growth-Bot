#!/usr/bin/env python3
"""
Test Part B: Dynamic Context Builder

Verifies that the dynamic_context_builder generates different guidance
for different niches and categories (never a preset).
"""

from src.prompts.dynamic_context_builder import DynamicContextBuilder


def test_dynamic_niche_variation():
    """Verify different niches produce different guidance."""
    print("Testing: Dynamic niche variation in context guidance")
    print("-" * 60)

    category = "general_photography"

    # Call with two different niches
    guidance_underwater = DynamicContextBuilder.build_category_guidance(
        category=category,
        niche="underwater welding",
        user_idea=""
    )

    guidance_luxury = DynamicContextBuilder.build_category_guidance(
        category=category,
        niche="luxury travel",
        user_idea=""
    )

    # Verify both are non-empty
    assert len(guidance_underwater) > 0, "Should generate guidance for underwater welding"
    assert len(guidance_luxury) > 0, "Should generate guidance for luxury travel"

    # Verify they are different (niche is interpolated)
    assert guidance_underwater != guidance_luxury, "Different niches should produce different guidance"

    # Verify niche text is included verbatim
    assert "underwater welding" in guidance_underwater, "Niche should appear in guidance"
    assert "luxury travel" in guidance_luxury, "Niche should appear in guidance"

    print("[OK] Different niches produce different guidance")
    print("[OK] Niche text interpolated verbatim (not substituted)")

    print("\nGuidance sample for 'underwater welding': {} chars generated".format(len(guidance_underwater)))
    print("\nGuidance sample for 'luxury travel': {} chars generated".format(len(guidance_luxury)))


def test_category_specific_guidance():
    """Verify different categories have different structural guidance."""
    print("\n" + "-" * 60)
    print("Testing: Category-specific structural guidance")
    print("-" * 60)

    niche = "test_niche"

    guidance_logo = DynamicContextBuilder.build_category_guidance(
        category="logo_create",
        niche=niche,
        user_idea=""
    )

    guidance_ui = DynamicContextBuilder.build_category_guidance(
        category="ui_ux_design",
        niche=niche,
        user_idea=""
    )

    # Verify both are non-empty
    assert len(guidance_logo) > 0, "Should generate guidance for logo_create"
    assert len(guidance_ui) > 0, "Should generate guidance for ui_ux_design"

    # Verify they are different (category-specific guidance)
    assert guidance_logo != guidance_ui, "Different categories should produce different guidance"

    # Verify category-specific concepts are present
    assert ("Memorable" in guidance_logo or "scalable" in guidance_logo), "Logo guidance should mention memorability/scalability"
    assert ("interface" in guidance_ui or "UX" in guidance_ui), "UI guidance should mention interface/UX"

    print("[OK] Different categories produce different guidance")
    print("[OK] Category-specific concepts are present")

    print("\nGuidance for 'logo_create': {} chars".format(len(guidance_logo)))
    print("\nGuidance for 'ui_ux_design': {} chars".format(len(guidance_ui)))


def test_no_preset_substitution():
    """Verify unusual niches don't get substituted with presets."""
    print("\n" + "-" * 60)
    print("Testing: No preset substitution for unusual niches")
    print("-" * 60)

    unusual_niche = "left-handed chainsaw juggling for seniors"

    guidance = DynamicContextBuilder.build_category_guidance(
        category="general_photography",
        niche=unusual_niche,
        user_idea=""
    )

    # Verify the exact unusual niche is present (not substituted)
    assert unusual_niche in guidance, "Should use user's exact niche, not substitute"
    assert "unusual" not in unusual_niche.lower(), "Test setup: niche should be unusual"

    print("[OK] Unusual niche preserved verbatim")
    print("[OK] No substitution or fallback to preset topics")

    print("\nGenerated guidance includes exact niche:")
    print("Niche: {}".format(unusual_niche))


if __name__ == "__main__":
    test_dynamic_niche_variation()
    test_category_specific_guidance()
    test_no_preset_substitution()

    print("\n" + "=" * 60)
    print("PART B VERIFICATION: ALL TESTS PASSED")
    print("=" * 60)
    print("\nKey findings:")
    print("- Dynamic context builder generates guidance per-request")
    print("- Different niches produce different guidance (never preset)")
    print("- Category-specific guidance differs between categories")
    print("- Unusual niches are preserved, not substituted")
