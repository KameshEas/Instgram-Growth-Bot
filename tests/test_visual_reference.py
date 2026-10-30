"""Tests for the visual_systems library and its bridge into the prompt generator."""
import importlib
import re

import pytest

from src.prompts.templates import list_categories
from src.prompts.visual_reference import (
    MAX_NEGATIVE_TERMS,
    TEXT_CATEGORIES,
    TRANSFORM_CATEGORIES,
    VisualReference,
)

VISUAL_MODULES = [
    "camera_language", "color_grading", "composition_intelligence", "lighting_physics",
    "material_behavior", "model_adaptation", "negative_prompts", "optical_characteristics",
    "scene_physics", "semantic_optimizer", "style_directors",
]


@pytest.mark.parametrize("name", VISUAL_MODULES)
def test_every_visual_system_module_imports(name):
    importlib.import_module(f"src.prompts.visual_systems.{name}")


@pytest.mark.parametrize("category", sorted(set(list_categories()) - TEXT_CATEGORIES))
def test_reference_block_is_clean_for_every_image_category(category):
    block = VisualReference.build_reference_block(category, location="beach")
    if not block:
        return  # e.g. ui_ux_design has no technical reference
    assert block.startswith("Technical reference")
    assert "optional starting points" in block
    # No empty library fields such as "Focal point: ." or "Shadow tones: ."
    assert not re.search(r":\s*\.", block), block
    # No duplicated labels such as "Composition: Composition:"
    assert not re.search(r"(\w[\w ]*): \1:", block), block
    assert len(block) < 1600


@pytest.mark.parametrize("category", sorted(TEXT_CATEGORIES))
def test_text_categories_get_no_reference(category):
    assert VisualReference.build_reference_block(category) == ""


@pytest.mark.parametrize("category", sorted(TRANSFORM_CATEGORIES))
def test_transform_lighting_follows_location(category):
    outdoor = VisualReference.build_reference_block(category, location="beach")
    indoor = VisualReference.build_reference_block(category, location="office")
    assert "Outdoor lighting" in outdoor and "Scene physics" in outdoor
    assert "Professional lighting setup" in indoor and "Outdoor lighting" not in indoor


def test_merge_negatives_keeps_model_terms_first_dedupes_and_caps():
    variations = [{"negative_prompt": "blurry, watermark, Warped Product Shape"}, {"prompt": "no negatives yet"}]
    VisualReference.merge_negatives(variations, "product_3d")
    first = [t.strip() for t in variations[0]["negative_prompt"].split(",")]
    assert first[:2] == ["blurry", "watermark"]
    assert [t.lower() for t in first].count("warped product shape") == 1
    assert len(first) <= MAX_NEGATIVE_TERMS
    # product renders must not get human-anatomy negatives
    assert "bad teeth" not in variations[0]["negative_prompt"]
    assert variations[1]["negative_prompt"]  # filled even when the model gave none


def test_transform_negatives_include_identity_lock():
    variations = [{"negative_prompt": "blurry"}]
    VisualReference.merge_negatives(variations, "women_transform")
    assert "different person" in variations[0]["negative_prompt"] or "reference" in variations[0]["negative_prompt"]


def test_merge_negatives_ignores_text_categories():
    variations = [{"content": "caption", "negative_prompt": ""}]
    VisualReference.merge_negatives(variations, "captions_templates")
    assert variations[0]["negative_prompt"] == ""
