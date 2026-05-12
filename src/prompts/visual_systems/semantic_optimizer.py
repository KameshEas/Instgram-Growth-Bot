"""Semantic Optimizer - Issue #17 Solution
Prompt compression and semantic optimization.

Long prompts:
- Dilute attention on strongest tokens
- Create contradictions
- Reduce composition coherence
- Confuse model intent

Semantic optimizer:
- Removes redundancy
- Merges visual concepts
- Prioritizes strongest tokens
- Compresses while maintaining meaning
"""

from typing import List, Optional, Dict
import re


class SemanticOptimizer:
    """Compress and optimize prompts for maximum model attention."""
    
    # Redundancy patterns to remove
    REDUNDANCY_PATTERNS = [
        ("ultra high definition, high definition", "ultra high definition"),
        ("masterpiece, award-winning", "masterpiece"),
        ("cinematic, cinematic", "cinematic"),
        ("professional photography, professional", "professional photography"),
        ("realistic, realism, authentic reality", "realistic authentic"),
        ("detailed, highly detailed, very detailed", "meticulously detailed"),
        ("sharp focus, sharp, very sharp", "sharp focus"),
        ("stunning, beautiful, gorgeous", "striking beauty"),
    ]
    
    # Concept mergers (combine related concepts)
    CONCEPT_MERGERS = {
        "soft lighting, golden hour": "golden hour soft lighting",
        "shallow depth of field, bokeh": "shallow bokeh depth",
        "ultra high definition, 8k, 4k": "ultra high definition",
        "Award-winning, masterpiece, trending": "award-winning masterpiece",
        "Editorial, magazine, publication": "editorial magazine quality",
    }
    
    # Priority token boost (strengthen strongest concepts)
    PRIORITY_TOKENS = {
        "quiet luxury": 1.3,  # Boost luxury-specific language
        "medium-format": 1.2,  # Camera specificity
        "Hasselblad": 1.2,
        "editorial": 1.2,
        "bespoke": 1.1,
        "artisanal": 1.1,
    }
    
    # Weak adjective removal
    WEAK_ADJECTIVES = [
        "very", "really", "extremely", "quite", "rather",
        "somewhat", "fairly", "pretty", "nice", "good",
        "bad", "thing", "stuff",
    ]
    
    # Generic quality keywords to remove (use specific instead)
    GENERIC_QUALITY = [
        "nice quality", "good quality", "best quality",
        "professional looking", "high quality",
    ]
    
    # Semantic compression dictionary
    SEMANTIC_COMPRESSION = {
        "soft directional daylight from windows": "window-lit natural light",
        "professional three-point lighting setup": "three-point lighting",
        "shallow depth of field with smooth bokeh": "shallow bokeh focus",
        "charcoal, ivory, and warm grey tones": "charcoal + ivory palette",
    }
    
    @staticmethod
    def optimize_prompt(prompt: str, max_length: Optional[int] = None) -> str:
        \"\"\"
        Optimize prompt for maximum model attention.
        
        Args:
            prompt: Original prompt string
            max_length: Optional maximum length in characters
            
        Returns:
            Optimized compressed prompt
        \"\"\"
        
        optimized = prompt
        
        # Remove weak adjectives
        for adj in SemanticOptimizer.WEAK_ADJECTIVES:
            optimized = re.sub(r'\\b' + adj + r'\\s+', '', optimized, flags=re.IGNORECASE)
        
        # Remove redundancies
        for redundant, replacement in SemanticOptimizer.REDUNDANCY_PATTERNS:
            optimized = optimized.replace(redundant, replacement)
        
        # Merge concepts
        for original, merged in SemanticOptimizer.CONCEPT_MERGERS.items():
            optimized = optimized.replace(original, merged)
        
        # Compress semantic concepts
        for long_form, short_form in SemanticOptimizer.SEMANTIC_COMPRESSION.items():
            optimized = optimized.replace(long_form, short_form)
        
        # Remove generic quality keywords (replace with specificity)
        for generic in SemanticOptimizer.GENERIC_QUALITY:
            optimized = optimized.replace(generic, \"meticulous rendering\")
        
        # Enforce maximum length if specified
        if max_length and len(optimized) > max_length:
            optimized = SemanticOptimizer._truncate_intelligently(optimized, max_length)
        
        return optimized.strip()
    
    @staticmethod
    def _truncate_intelligently(prompt: str, max_length: int) -> str:
        \"\"\"Truncate prompt intelligently, keeping strongest concepts.\"\"\"
        
        # Find priority tokens in prompt
        parts = prompt.split(\".\")
        priority_parts = []
        regular_parts = []
        
        for part in parts:
            if any(token in part for token in SemanticOptimizer.PRIORITY_TOKENS.keys()):
                priority_parts.append(part)
            else:
                regular_parts.append(part)
        
        # Reconstruct with priority parts first
        reconstructed = \". \".join(priority_parts + regular_parts[:2])
        
        if len(reconstructed) > max_length:
            reconstructed = reconstructed[:max_length].rsplit(\" \", 1)[0] + \"...\"
        
        return reconstructed
    
    @staticmethod
    def get_compression_stats(original: str, optimized: str) -> Dict[str, int]:
        \"\"\"Get compression statistics.\"\"\"
        
        return {
            \"original_length\": len(original),
            \"optimized_length\": len(optimized),
            \"compression_percent\": int((1 - len(optimized) / len(original)) * 100),
            \"word_reduction\": len(original.split()) - len(optimized.split()),
        }
    
    @staticmethod
    def emphasize_priority_tokens(prompt: str) -> str:
        \"\"\"Emphasize priority tokens (if using model with weighting support).\"\"\"
        
        emphasized = prompt
        
        for token, weight in SemanticOptimizer.PRIORITY_TOKENS.items():
            if token in emphasized:
                # Format for models supporting weighted prompts
                emphasized = emphasized.replace(
                    token,
                    f\"({token}:{weight:.1f})\"
                )
        
        return emphasized
