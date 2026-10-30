"""Model Adaptation Layer - Issue #16 Solution
Different AI models have different prompt syntax and optimization patterns.

Model differences:
- Midjourney prefers concise aesthetic language
- Flux works best with technical descriptive language
- SDXL responds to specific weighted syntax
- GPT-image needs narrative structure
- Imagen benefits from safety-first phrasing

This layer adapts unified prompts to model-specific syntax.
"""

from typing import Dict, Optional, List


class ModelAdaptation:
    """Adapt prompts to specific AI model requirements."""
    
    # Model-specific syntax rules
    MODEL_PROFILES = {
        "midjourney": {
            "description": "Midjourney v6 optimization",
            "strengths": "aesthetic language, visual references, dramatic descriptors",
            "optimal_length": "50-100 tokens",
            "adjective_limit": "6-8 max adjectives",
            "syntax": "concise aesthetic language without technical jargon",
            "weighting_support": True,
            "prefer": ["stunning", "cinematic", "aesthetic", "editorial"],
            "avoid": ["ultra high definition", "realistic", "photorealistic"],
            "priority_style": "aesthetic over technical",
        },
        "flux": {
            "description": "Black Forest Labs Flux optimization",
            "strengths": "technical descriptive language, equipment terminology",
            "optimal_length": "100-150 tokens",
            "adjective_limit": "10-15 adjectives",
            "syntax": "detailed technical description",
            "weighting_support": False,
            "prefer": ["hasselblad", "cinematic", "shot on", "technical"],
            "avoid": ["aesthetic labels", "vague beauty terms"],
            "priority_style": "technical over aesthetic",
        },
        "sdxl": {
            "description": "Stable Diffusion XL optimization",
            "strengths": "weighted syntax, quality descriptors, style keywords",
            "optimal_length": "75-125 tokens",
            "adjective_limit": "8-12 adjectives",
            "syntax": "(concept:weight) parenthetical syntax",
            "weighting_support": True,
            "prefer": ["masterpiece", "(high quality:1.2)", "(professional:1.1)"],
            "avoid": ["extremely", "very"],
            "priority_style": "weighted quality focus",
        },
        "gpt_image": {
            "description": "OpenAI GPT-4V image generation",
            "strengths": "natural language narrative, story-based description",
            "optimal_length": "80-120 tokens",
            "adjective_limit": "unlimited but natural",
            "syntax": "narrative story-based description",
            "weighting_support": False,
            "prefer": ["imagine", "scene of", "depicts"],
            "avoid": ["technical jargon", "equipment names"],
            "priority_style": "narrative and contextual",
        },
        "imagen": {
            "description": "Google Imagen optimization",
            "strengths": "safety-aware phrasing, clear positive descriptions",
            "optimal_length": "60-100 tokens",
            "adjective_limit": "5-8 adjectives",
            "syntax": "positive descriptive language emphasizing beautiful aspects",
            "weighting_support": False,
            "prefer": ["beautiful", "high quality", "masterpiece"],
            "avoid": ["negative descriptors", "implied negatives"],
            "priority_style": "positive safety-first language",
        },
    }
    
    # Syntax adaptation templates
    SYNTAX_ADAPTERS = {
        "midjourney_aesthetic": "--ar 3:2 --s 750 --q 2 --niji 6",
        "midjourney_parameters": "--iw 0.5 for image weight --cw 100",
        "sdxl_quality_boost": "(masterpiece:1.3), (best quality:1.2), (excellent detail:1.1)",
        "flux_equipment": "Shot on professional equipment, technical rendering",
    }
    
    # Quality tier adaptation
    QUALITY_TIERS = {
        "web": {
            "midjourney": "Aesthetic mobile-optimized composition",
            "flux": "Optimized technical description avoiding extreme detail",
            "sdxl": "(good quality:1.0), web-friendly rendering",
        },
        "professional": {
            "midjourney": "Professional editorial aesthetic composition",
            "flux": "Complete technical specification with all equipment details",
            "sdxl": "(masterpiece:1.2), (professional quality:1.1), detailed rendering",
        },
        "exhibition": {
            "midjourney": "Museum-quality aesthetic perfection",
            "flux": "Exhaustive technical specification maximizing detail capture",
            "sdxl": "(masterpiece:1.3), (museum quality:1.2), (perfect detail:1.1)",
        },
    }
    
    @staticmethod
    def adapt_prompt(
        base_prompt: str,
        target_model: str,
        quality_tier: str = "professional",
    ) -> str:
        \"\"\"
        Adapt unified prompt to target model syntax.
        
        Args:
            base_prompt: Unified prompt from professional_structure
            target_model: 'midjourney', 'flux', 'sdxl', 'gpt_image', 'imagen'
            quality_tier: 'web', 'professional', 'exhibition'
            
        Returns:
            Model-specific adapted prompt
        \"\"\"
        
        if target_model not in ModelAdaptation.MODEL_PROFILES:
            return base_prompt
        
        profile = ModelAdaptation.MODEL_PROFILES[target_model]
        adapted = base_prompt
        
        # Apply quality tier adaptation
        if quality_tier in ModelAdaptation.QUALITY_TIERS:
            tier_prefix = ModelAdaptation.QUALITY_TIERS[quality_tier].get(
                target_model,
                \"\"
            )
            if tier_prefix:
                adapted = f\"{tier_prefix}. {adapted}\"
        
        # Apply model-specific optimizations
        adapted = ModelAdaptation._apply_model_syntax(adapted, target_model)
        
        # Apply preference/avoidance rules
        adapted = ModelAdaptation._apply_preferences(adapted, target_model)
        
        # Truncate to optimal length
        optimal_length = profile.get(\"optimal_length\", \"100 tokens\")
        token_limit = int(optimal_length.split(\"-\")[1].split()[0])
        
        if len(adapted.split()) > token_limit:
            adapted = \" \".join(adapted.split()[:token_limit])
        
        return adapted
    
    @staticmethod\n    def _apply_model_syntax(prompt: str, model: str) -> str:\n        \"\"\"Apply model-specific syntax rules.\"\"\"\n        \n        if model == \"sdxl\" and \"(\" not in prompt:\n            # Add SDXL-style weighting\n            prompt = f\"(masterpiece:1.2), {prompt}\"\n        \n        elif model == \"midjourney\":\n            # Remove ultra HD references for Midjourney\n            prompt = prompt.replace(\"ultra high definition\", \"\")\n            prompt = prompt.replace(\"8k\", \"\")\n        \n        return prompt\n    \n    @staticmethod\n    def _apply_preferences(prompt: str, model: str) -> str:\n        \"\"\"Apply model preference/avoidance lists.\"\"\"\n        \n        profile = ModelAdaptation.MODEL_PROFILES.get(model, {})\n        \n        # Apply avoidances\n        for avoid in profile.get(\"avoid\", []):\n            prompt = prompt.replace(avoid, \"\")\n        \n        # Boost preferences (simple enhancement, not weight-based)\n        for prefer in profile.get(\"prefer\", []):\n            if prefer not in prompt:\n                # Just ensure it's present in beginning\n                pass\n        \n        return prompt\n    \n    @staticmethod\n    def get_model_parameters(model: str) -> Dict:\n        \"\"\"Get model-specific parameters for generation.\"\"\"\n        \n        return ModelAdaptation.MODEL_PROFILES.get(\n            model,\n            {\"description\": \"unknown model\"}\n        )\n    \n    @staticmethod\n    def recommend_model(context: str) -> str:\n        \"\"\"Recommend best model for context.\"\"\"\n        \n        recommendations = {\n            \"luxury_portrait\": \"midjourney\",\n            \"product\": \"flux\",\n            \"cinematic\": \"sdxl\",\n            \"editorial\": \"midjourney\",\n            \"technical\": \"flux\",\n        }\n        \n        for key, model in recommendations.items():\n            if key in context.lower():\n                return model\n        \n        return \"midjourney\"  # Safe default
