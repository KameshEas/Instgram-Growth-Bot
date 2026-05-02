"""
Image Alignment Validator
Validates whether generated image preserves features from reference input
"""

import logging
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class AlignmentStatus(Enum):
    """Alignment validation status"""
    PASS = "PASS"           # Good alignment
    ADJUST = "ADJUST"       # Marginal, suggest adjustment
    FAIL = "FAIL"           # Poor alignment


@dataclass
class AlignmentReport:
    """Result of alignment validation"""
    alignment_score: float  # 0.0-1.0
    status: str  # PASS, ADJUST, FAIL
    preserved_features: List[str]
    missing_features: List[str]
    denoising_recommendation: Optional[float] = None
    cfg_recommendation: Optional[float] = None
    reasoning: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


class ImageAlignmentValidator:
    """
    Validates image-to-reference alignment.
    
    Checks whether generated image preserves key features from the reference input.
    Uses denoising strength correlation analysis from Phase 1C:
    - Correlation: High denoising = Low alignment
    - Correlation: Low denoising = High alignment
    """
    
    # Product type → ideal denoising range for alignment
    DENOISING_TARGETS = {
        "t-shirt": {"min": 0.65, "ideal": 0.70, "max": 0.75},
        "mug": {"min": 0.50, "ideal": 0.60, "max": 0.70},
        "canvas": {"min": 0.70, "ideal": 0.78, "max": 0.85},
        "poster": {"min": 0.70, "ideal": 0.78, "max": 0.85},
        "merchandise": {"min": 0.40, "ideal": 0.55, "max": 0.65},
        "default": {"min": 0.60, "ideal": 0.70, "max": 0.80},
    }
    
    # Denoising → expected alignment score correlation
    # From Phase 1C: -0.45 correlation (higher denoise = lower alignment)
    DENOISING_ALIGNMENT_MAP = {
        0.3: 0.95,  # Very low denoise, very high alignment
        0.4: 0.92,
        0.5: 0.88,
        0.6: 0.82,
        0.7: 0.75,
        0.8: 0.62,
        0.9: 0.48,
        1.0: 0.30,  # Max denoise, low alignment
    }
    
    def __init__(self):
        """Initialize validator"""
        logger.info("ImageAlignmentValidator initialized")
    
    def validate_alignment(
        self,
        original_features: List[str],
        generated_image_description: str,
        denoising_strength: float,
        product_type: str = "default",
        cfg_scale: float = 12.0
    ) -> AlignmentReport:
        """
        Validate alignment between original and generated image.
        
        Args:
            original_features: Features to preserve from reference
                e.g., ["red logo", "circular shape", "brand name"]
            generated_image_description: Description/analysis of generated image
            denoising_strength: Denoising strength used (0.0-1.0)
            product_type: Type of product (for denoising target)
            cfg_scale: CFG scale used (for recommendation)
        
        Returns:
            AlignmentReport with validation result
        
        Example:
            >>> validator.validate_alignment(
            ...     original_features=["red logo", "circular"],
            ...     generated_image_description="Generated image with red circle but text missing",
            ...     denoising_strength=0.85,
            ...     product_type="mug"
            ... )
            AlignmentReport(alignment_score=0.65, status="ADJUST", ...)
        """
        
        # Normalize product type
        product_type = product_type.lower()
        
        # Step 1: Detect preserved features (simplified text matching)
        preserved = self._detect_preserved_features(
            original_features,
            generated_image_description
        )
        
        # Step 2: Calculate feature preservation ratio
        feature_preservation_score = len(preserved) / max(len(original_features), 1)
        
        # Step 3: Get expected alignment from denoising level
        expected_alignment = self._get_alignment_from_denoising(denoising_strength)
        
        # Step 4: Calculate combined alignment score
        alignment_score = (feature_preservation_score * 0.6) + (expected_alignment * 0.4)
        alignment_score = max(0.0, min(1.0, alignment_score))
        
        # Step 5: Determine status
        if alignment_score >= 0.75:
            status = AlignmentStatus.PASS.value
            message = f"Good alignment ({alignment_score:.2f})"
        elif alignment_score >= 0.60:
            status = AlignmentStatus.ADJUST.value
            message = f"Marginal alignment ({alignment_score:.2f}) - consider adjustment"
        else:
            status = AlignmentStatus.FAIL.value
            message = f"Poor alignment ({alignment_score:.2f}) - adjustment recommended"
        
        # Step 6: Get recommendations
        denoise_rec = None
        cfg_rec = None
        
        if status in [AlignmentStatus.ADJUST.value, AlignmentStatus.FAIL.value]:
            denoise_rec, cfg_rec = self._get_parameter_recommendations(
                alignment_score,
                denoising_strength,
                cfg_scale,
                product_type
            )
        
        # Step 7: Build report
        missing_features = [f for f in original_features if f not in preserved]
        
        report = AlignmentReport(
            alignment_score=alignment_score,
            status=status,
            preserved_features=preserved,
            missing_features=missing_features,
            denoising_recommendation=denoise_rec,
            cfg_recommendation=cfg_rec,
            reasoning=message
        )
        
        logger.info(
            f"Alignment validation: Score={alignment_score:.2f}, "
            f"Status={status}, Preserved={len(preserved)}/{len(original_features)}"
        )
        
        return report
    
    def _detect_preserved_features(
        self,
        original_features: List[str],
        generated_description: str
    ) -> List[str]:
        """
        Detect which original features appear in generated image description.
        Uses simple substring matching.
        """
        preserved = []
        
        for feature in original_features:
            # Simple substring matching (could be enhanced with fuzzy matching)
            if feature.lower() in generated_description.lower():
                preserved.append(feature)
            # Also try matching parts of the feature
            elif self._partial_match(feature, generated_description):
                preserved.append(feature)
        
        return preserved
    
    def _partial_match(self, feature: str, description: str) -> bool:
        """Check if parts of feature appear in description"""
        words = feature.lower().split()
        description_lower = description.lower()
        
        # If 2+ words in feature, require 50%+ match
        if len(words) >= 2:
            matching_words = sum(1 for word in words if word in description_lower)
            return matching_words >= len(words) / 2
        
        return False
    
    def _get_alignment_from_denoising(self, denoising_strength: float) -> float:
        """
        Get expected alignment score from denoising strength.
        Based on Phase 1C correlation: -0.45
        """
        
        # Find closest denoising value in map
        closest_denoise = min(
            self.DENOISING_ALIGNMENT_MAP.keys(),
            key=lambda x: abs(x - denoising_strength)
        )
        
        # Linear interpolation between closest values
        denoise_values = sorted(self.DENOISING_ALIGNMENT_MAP.keys())
        
        for i in range(len(denoise_values) - 1):
            d1, d2 = denoise_values[i], denoise_values[i + 1]
            if d1 <= denoising_strength <= d2:
                a1 = self.DENOISING_ALIGNMENT_MAP[d1]
                a2 = self.DENOISING_ALIGNMENT_MAP[d2]
                
                # Linear interpolation
                t = (denoising_strength - d1) / (d2 - d1)
                return a1 + t * (a2 - a1)
        
        # Out of range, return edge value
        if denoising_strength < min(denoise_values):
            return self.DENOISING_ALIGNMENT_MAP[min(denoise_values)]
        else:
            return self.DENOISING_ALIGNMENT_MAP[max(denoise_values)]
    
    def _get_parameter_recommendations(
        self,
        alignment_score: float,
        current_denoising: float,
        current_cfg: float,
        product_type: str
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Get parameter recommendations to improve alignment.
        
        Returns:
            (recommended_denoising, recommended_cfg)
        """
        
        targets = self.DENOISING_TARGETS.get(product_type, self.DENOISING_TARGETS["default"])
        ideal_denoise = targets["ideal"]
        
        # Recommendation 1: Adjust denoising
        denoise_rec = None
        if current_denoising > ideal_denoise + 0.05:
            # Too much denoising, reduce it
            denoise_rec = ideal_denoise * 0.95
            logger.info(f"Recommendation: Reduce denoising from {current_denoising} to {denoise_rec}")
        elif current_denoising < ideal_denoise - 0.1:
            # Too little denoising (rare), increase slightly
            denoise_rec = ideal_denoise * 1.05
            logger.info(f"Recommendation: Increase denoising from {current_denoising} to {denoise_rec}")
        
        # Recommendation 2: Adjust CFG
        cfg_rec = None
        if alignment_score < 0.5:
            # Very poor alignment, reduce CFG to allow more prompt flexibility
            cfg_rec = max(8.0, current_cfg - 2)
            logger.info(f"Recommendation: Reduce CFG from {current_cfg} to {cfg_rec}")
        elif alignment_score < 0.65:
            # Marginal alignment, slightly reduce CFG
            cfg_rec = max(10.0, current_cfg - 1)
            logger.info(f"Recommendation: Slightly reduce CFG from {current_cfg} to {cfg_rec}")
        
        return denoise_rec, cfg_rec
    
    def validate_batch(
        self,
        validations: List[Dict]
    ) -> List[AlignmentReport]:
        """
        Validate multiple image-reference pairs.
        
        Args:
            validations: List of dicts with:
                - original_features: List[str]
                - generated_description: str
                - denoising_strength: float
                - product_type: str (optional)
                - cfg_scale: float (optional)
        
        Returns:
            List of AlignmentReport objects
        """
        
        results = []
        for validation in validations:
            report = self.validate_alignment(
                original_features=validation["original_features"],
                generated_image_description=validation["generated_description"],
                denoising_strength=validation["denoising_strength"],
                product_type=validation.get("product_type", "default"),
                cfg_scale=validation.get("cfg_scale", 12.0)
            )
            results.append(report)
        
        return results
    
    def get_statistics(self, reports: List[AlignmentReport]) -> Dict:
        """
        Get statistics from multiple alignment reports.
        
        Returns:
            Stats including average alignment, pass rate, etc.
        """
        
        if not reports:
            return {}
        
        scores = [r.alignment_score for r in reports]
        statuses = [r.status for r in reports]
        
        return {
            "total_validations": len(reports),
            "average_alignment": sum(scores) / len(scores),
            "min_alignment": min(scores),
            "max_alignment": max(scores),
            "pass_count": sum(1 for s in statuses if s == AlignmentStatus.PASS.value),
            "adjust_count": sum(1 for s in statuses if s == AlignmentStatus.ADJUST.value),
            "fail_count": sum(1 for s in statuses if s == AlignmentStatus.FAIL.value),
            "pass_rate": sum(1 for s in statuses if s == AlignmentStatus.PASS.value) / len(reports)
        }


class ImageAlignmentValidatorFactory:
    """Factory for singleton instance"""
    
    _instance: Optional[ImageAlignmentValidator] = None
    
    @classmethod
    def get_validator(cls) -> ImageAlignmentValidator:
        """Get or create singleton instance"""
        if cls._instance is None:
            cls._instance = ImageAlignmentValidator()
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset singleton (for testing)"""
        cls._instance = None
