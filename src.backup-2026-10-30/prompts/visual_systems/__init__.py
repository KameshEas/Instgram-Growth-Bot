"""Visual Systems Module
Modular architecture for state-of-the-art cinematic prompt engineering.

This module breaks down the monolithic template system into reusable, composable components
that each focus on a specific aspect of visual generation quality.

Core Systems:
- lighting_physics: Realistic light behavior and interaction
- camera_language: Professional equipment terminology and rendering
- color_grading: Cinematic color profiles and grading systems
- material_behavior: Fabric, skin, glass, metal, wood responses
- composition_intelligence: Focal hierarchy, visual flow, balance
- optical_characteristics: Lens imperfections, film effects, optical realism
- scene_physics: Physical interaction, shadows, reflections, atmosphere
- style_directors: Coherent visual language systems (A24, Apple, Nike, etc.)
- negative_prompts: Quality guardrails and error prevention
- semantic_optimizer: Prompt compression and attention prioritization

Architecture Pattern:
Each system exports reusable modules that combine deterministically,
allowing flexible composition while maintaining visual coherence.
"""

from .lighting_physics import LightingPhysics
from .camera_language import CameraLanguage
from .color_grading import ColorGrading
from .material_behavior import MaterialBehavior
from .composition_intelligence import CompositionIntelligence
from .optical_characteristics import OpticalCharacteristics
from .scene_physics import ScenePhysics
from .style_directors import StyleDirectors
from .negative_prompts import NegativePrompts
from .semantic_optimizer import SemanticOptimizer
from .model_adaptation import ModelAdaptation

__all__ = [
    'LightingPhysics',
    'CameraLanguage',
    'ColorGrading',
    'MaterialBehavior',
    'CompositionIntelligence',
    'OpticalCharacteristics',
    'ScenePhysics',
    'StyleDirectors',
    'NegativePrompts',
    'SemanticOptimizer',
    'ModelAdaptation',
]
