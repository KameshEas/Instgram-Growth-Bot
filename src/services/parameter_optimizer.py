"""
Phase 1C: Parameter Optimization Matrix Service
Analyzes image generation parameters and their correlation with quality scores
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)


class ProductType(Enum):
    """Product types for parameter optimization"""
    TSHIRT = "t-shirt"
    MUG = "mug"
    HOODIE = "hoodie"
    PHONE_CASE = "phone_case"
    CANVAS = "canvas"
    POSTER = "poster"
    NOTEBOOK = "notebook"
    CAP = "cap"


@dataclass
class ParameterPreset:
    """A recommended parameter set for specific context"""
    name: str
    description: str
    cfg_scale: float  # 7-20 typical
    denoising_strength: float  # 0.0-1.0
    num_steps: int  # 20-100
    seed: Optional[int]  # For reproducibility
    notes: str
    ideal_for: List[str]  # Use cases this is ideal for


@dataclass
class ParameterQualityCorrelation:
    """Correlation between parameters and quality"""
    parameter: str  # e.g., "cfg_scale"
    quality_dimension: str  # e.g., "image_alignment"
    correlation_coefficient: float  # -1.0 to 1.0
    sample_count: int
    optimal_value: float
    optimal_range: Tuple[float, float]
    observations: List[str]


class ParameterOptimizationMatrix:
    """
    Analyzes parameter effectiveness by:
    1. Collecting parameter -> quality correlations
    2. Finding optimal parameter ranges per product type
    3. Building parameter presets
    4. Identifying parameter interactions
    """
    
    def __init__(self):
        self.logger = logger
        self.parameter_data: List[Dict[str, Any]] = []
        self.correlations: Dict[str, ParameterQualityCorrelation] = {}
        self.presets: List[ParameterPreset] = []
    
    def add_parameter_sample(
        self,
        cfg_scale: float,
        denoising_strength: float,
        num_steps: int,
        quality_score: float,
        image_alignment_score: float,
        product_type: str,
        notes: str = ""
    ) -> None:
        """Add a parameter sample with quality feedback"""
        sample = {
            "cfg_scale": cfg_scale,
            "denoising_strength": denoising_strength,
            "num_steps": num_steps,
            "quality_score": quality_score,
            "image_alignment_score": image_alignment_score,
            "product_type": product_type,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self.parameter_data.append(sample)
        self.logger.debug(f"Added parameter sample: {product_type} (quality: {quality_score:.1f})")
    
    def load_samples_from_evaluations(self, evaluations: List[Dict[str, Any]]) -> None:
        """Load parameter samples from evaluation records"""
        for eval_record in evaluations:
            # Extract parameter info if available
            if "parameters" in eval_record:
                params = eval_record["parameters"]
                quality = eval_record.get("overall_rating", 5.0)
                image_alignment = eval_record.get("scores", {}).get(
                    "image_alignment", {}).get("score", 5.0)
                product = eval_record.get("metadata", {}).get("product_type", "unknown")
                
                self.add_parameter_sample(
                    cfg_scale=params.get("cfg_scale", 7.5),
                    denoising_strength=params.get("denoising_strength", 0.75),
                    num_steps=params.get("num_steps", 50),
                    quality_score=quality,
                    image_alignment_score=image_alignment,
                    product_type=product
                )
    
    def analyze_parameter_correlations(self) -> Dict[str, ParameterQualityCorrelation]:
        """Analyze correlation between parameters and quality"""
        if len(self.parameter_data) < 10:
            self.logger.warning(f"Only {len(self.parameter_data)} samples, need 10+")
            return {}
        
        correlations = {}
        
        # Analyze each parameter
        for param_name in ["cfg_scale", "denoising_strength", "num_steps"]:
            # Collect values
            param_values = [s[param_name] for s in self.parameter_data]
            quality_values = [s["quality_score"] for s in self.parameter_data]
            
            # Calculate correlation
            correlation = self._calculate_correlation(param_values, quality_values)
            
            # Find optimal value
            optimal_val, optimal_range = self._find_optimal_range(
                param_values, quality_values
            )
            
            # Generate observations
            observations = self._generate_observations(
                param_name, param_values, quality_values, optimal_val
            )
            
            correlations[param_name] = ParameterQualityCorrelation(
                parameter=param_name,
                quality_dimension="overall_quality",
                correlation_coefficient=correlation,
                sample_count=len(self.parameter_data),
                optimal_value=optimal_val,
                optimal_range=optimal_range,
                observations=observations
            )
        
        self.correlations = correlations
        return correlations
    
    def build_parameter_presets(self) -> List[ParameterPreset]:
        """Build recommended parameter presets for different use cases"""
        presets = [
            # High quality, realistic
            ParameterPreset(
                name="High Quality",
                description="Maximum detail and realism",
                cfg_scale=15.0,
                denoising_strength=0.85,
                num_steps=100,
                seed=None,
                notes="Best for final output. Slower, higher quality.",
                ideal_for=["final_output", "high_quality", "showcase"]
            ),
            # Balanced
            ParameterPreset(
                name="Balanced",
                description="Good quality-speed tradeoff",
                cfg_scale=12.0,
                denoising_strength=0.75,
                num_steps=70,
                seed=None,
                notes="Recommended default. Good for most use cases.",
                ideal_for=["general_use", "default", "production"]
            ),
            # Fast preview
            ParameterPreset(
                name="Quick Preview",
                description="Fast generation for iteration",
                cfg_scale=9.0,
                denoising_strength=0.6,
                num_steps=30,
                seed=None,
                notes="Fast preview mode. Good for A/B testing.",
                ideal_for=["preview", "iteration", "draft"]
            ),
            # Image alignment focused (preserve reference)
            ParameterPreset(
                name="Reference Preservation",
                description="Maximum preservation of reference image",
                cfg_scale=10.0,
                denoising_strength=0.65,
                num_steps=50,
                seed=42,
                notes="For image-to-image. Preserves original features.",
                ideal_for=["img2img", "reference", "transformation"]
            ),
            # Subtle changes only
            ParameterPreset(
                name="Subtle Enhancement",
                description="Minor enhancement to reference",
                cfg_scale=8.0,
                denoising_strength=0.5,
                num_steps=40,
                seed=None,
                notes="For subtle style changes on existing image.",
                ideal_for=["subtle", "enhancement", "refinement"]
            ),
        ]
        
        self.presets = presets
        return presets
    
    def get_recommended_parameters(
        self,
        product_type: str,
        use_case: str,
        quality_preference: str = "balanced"
    ) -> ParameterPreset:
        """Get recommended parameters for a specific context"""
        
        # Map quality preference to preset
        quality_to_preset = {
            "high": "High Quality",
            "balanced": "Balanced",
            "fast": "Quick Preview",
            "preserve": "Reference Preservation",
            "subtle": "Subtle Enhancement"
        }
        
        preset_name = quality_to_preset.get(quality_preference, "Balanced")
        
        # Find matching preset
        matching = [p for p in self.presets if p.name == preset_name]
        if matching:
            preset = matching[0]
            
            # Fine-tune based on product type if data available
            adjusted = self._adjust_for_product_type(preset, product_type)
            return adjusted
        
        # Fallback
        return self.presets[1]  # Balanced
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Simple Pearson correlation calculation"""
        if len(x) < 2:
            return 0.0
        
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        
        std_x = (sum((xi - mean_x) ** 2 for xi in x)) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y)) ** 0.5
        
        if std_x == 0 or std_y == 0:
            return 0.0
        
        return numerator / (std_x * std_y * n)
    
    def _find_optimal_range(
        self,
        values: List[float],
        qualities: List[float]
    ) -> Tuple[float, Tuple[float, float]]:
        """Find optimal value and range for a parameter"""
        if not values or not qualities:
            return 0.0, (0.0, 1.0)
        
        # Pair values with qualities
        pairs = sorted(zip(values, qualities), key=lambda x: x[1], reverse=True)
        
        # Get top 30% best quality samples
        top_count = max(1, len(pairs) // 3)
        top_values = [v for v, q in pairs[:top_count]]
        
        if not top_values:
            return sum(values) / len(values), (min(values), max(values))
        
        optimal = sum(top_values) / len(top_values)
        value_range = (min(top_values), max(top_values))
        
        return optimal, value_range
    
    def _generate_observations(
        self,
        param_name: str,
        param_values: List[float],
        quality_values: List[float],
        optimal_val: float
    ) -> List[str]:
        """Generate human-readable observations about parameter"""
        observations = []
        
        correlation = self._calculate_correlation(param_values, quality_values)
        
        if correlation > 0.5:
            observations.append(f"Strong positive correlation ({correlation:.2f})")
            observations.append(f"Increasing {param_name} generally improves quality")
        elif correlation > 0.2:
            observations.append(f"Weak positive correlation ({correlation:.2f})")
        elif correlation < -0.5:
            observations.append(f"Strong negative correlation ({correlation:.2f})")
            observations.append(f"Increasing {param_name} generally decreases quality")
        else:
            observations.append("Weak or no correlation with quality")
        
        observations.append(f"Optimal value: {optimal_val:.2f}")
        observations.append(f"Sample count: {len(param_values)}")
        
        return observations
    
    def _adjust_for_product_type(
        self,
        preset: ParameterPreset,
        product_type: str
    ) -> ParameterPreset:
        """Adjust parameters based on product type"""
        adjusted = ParameterPreset(
            name=preset.name,
            description=preset.description,
            cfg_scale=preset.cfg_scale,
            denoising_strength=preset.denoising_strength,
            num_steps=preset.num_steps,
            seed=preset.seed,
            notes=preset.notes + f" (Adjusted for {product_type})",
            ideal_for=preset.ideal_for
        )
        
        # Product-specific adjustments
        if product_type in ["mug", "phone_case"]:
            # Smaller design areas need higher CFG for clarity
            adjusted.cfg_scale *= 1.1
        elif product_type in ["canvas", "poster"]:
            # Larger areas can use lower CFG
            adjusted.cfg_scale *= 0.9
        
        return adjusted
    
    def generate_matrix_visualization(self) -> str:
        """Generate text-based visualization of parameter matrix"""
        report = []
        report.append("=" * 80)
        report.append("PHASE 1C: PARAMETER OPTIMIZATION MATRIX")
        report.append("=" * 80)
        report.append("")
        report.append(f"Analysis Date: {datetime.now().isoformat()}")
        report.append(f"Total Samples: {len(self.parameter_data)}")
        report.append("")
        
        if self.correlations:
            report.append("PARAMETER CORRELATIONS")
            report.append("-" * 80)
            for param_name, corr in self.correlations.items():
                report.append(f"\n{param_name.upper()}")
                report.append(f"  Correlation with Quality: {corr.correlation_coefficient:.3f}")
                report.append(f"  Optimal Value: {corr.optimal_value:.2f}")
                report.append(f"  Optimal Range: {corr.optimal_range[0]:.2f} - {corr.optimal_range[1]:.2f}")
                
                if corr.observations:
                    report.append(f"  Observations:")
                    for obs in corr.observations[:3]:
                        report.append(f"    • {obs}")
        
        if self.presets:
            report.append("\n\nRECOMMENDED PARAMETER PRESETS")
            report.append("-" * 80)
            for preset in self.presets:
                report.append(f"\n{preset.name}")
                report.append(f"  Description: {preset.description}")
                report.append(f"  CFG Scale: {preset.cfg_scale}")
                report.append(f"  Denoising Strength: {preset.denoising_strength:.2f}")
                report.append(f"  Steps: {preset.num_steps}")
                report.append(f"  Ideal For: {', '.join(preset.ideal_for)}")
                if preset.notes:
                    report.append(f"  Notes: {preset.notes}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def export_matrix(self, filepath: str) -> None:
        """Export optimization matrix to JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "total_samples": len(self.parameter_data),
            "correlations": {
                name: {
                    "correlation_coefficient": corr.correlation_coefficient,
                    "optimal_value": corr.optimal_value,
                    "optimal_range": list(corr.optimal_range),
                    "observations": corr.observations
                }
                for name, corr in self.correlations.items()
            },
            "presets": [asdict(p) for p in self.presets]
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Parameter matrix exported to {filepath}")


def get_optimizer() -> ParameterOptimizationMatrix:
    """Factory function for parameter optimizer"""
    return ParameterOptimizationMatrix()
