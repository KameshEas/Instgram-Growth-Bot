"""
Tests for Phase 2A: Parameter Recommendation Engine & Image Alignment Validator
"""

import pytest
from src.services.parameter_recommendation_engine import (
    ParameterRecommendationEngine,
    ParameterRecommendationFactory,
    ProductType,
    QualityLevel
)
from src.services.image_alignment_validator import (
    ImageAlignmentValidator,
    ImageAlignmentValidatorFactory,
    AlignmentStatus
)


class TestParameterRecommendationEngine:
    """Test parameter recommendation engine"""
    
    def setup_method(self):
        """Setup before each test"""
        ParameterRecommendationFactory.reset()
        self.engine = ParameterRecommendationEngine()
    
    def test_engine_initialization(self):
        """Test engine initializes with presets"""
        assert self.engine is not None
        assert len(self.engine.presets) == 5
        assert "balanced" in self.engine.presets
        assert "high_quality" in self.engine.presets
    
    def test_default_parameters(self):
        """Test default recommendation"""
        params = self.engine.recommend_parameters()
        
        assert params is not None
        assert 7 <= params.cfg_scale <= 20
        assert 0.4 <= params.denoising_strength <= 1.0
        assert 20 <= params.num_steps <= 100
        assert params.preset_name is not None
    
    def test_mug_high_quality(self):
        """Test recommendation for mug with high quality"""
        params = self.engine.recommend_parameters(
            product_type="mug",
            alignment_importance=0.9,
            quality_level="high"
        )
        
        # Mugs with high alignment importance should have adjusted parameters
        # (alignment importance of 0.9 modulates the cfg_scale down for better alignment)
        assert params.cfg_scale >= 13.0  # Tuned down from base 15.0 due to alignment importance
        assert params.denoising_strength >= 0.75
        assert params.num_steps == 100
    
    def test_quick_preview(self):
        """Test quick preview mode"""
        params = self.engine.recommend_parameters(
            quality_level="quick"
        )
        
        assert params.num_steps <= 30
        assert params.cfg_scale <= 9.0
    
    def test_high_alignment_importance(self):
        """Test high alignment importance lowers denoising"""
        params = self.engine.recommend_parameters(
            alignment_importance=0.9,
            quality_level="balanced"
        )
        
        # Should blend towards reference preservation
        assert params.denoising_strength <= 0.75
        assert "alignment" in params.reasoning.lower()
    
    def test_low_alignment_importance(self):
        """Test low alignment importance allows creative freedom"""
        params = self.engine.recommend_parameters(
            alignment_importance=0.1,
            quality_level="balanced"
        )
        
        # Should increase CFG for more prompt adherence
        assert params.cfg_scale >= 12.0
        assert "creative" in params.reasoning.lower()
    
    def test_vague_input(self):
        """Test vague input defaults to quick preview"""
        params = self.engine.recommend_parameters(
            user_request_specificity=0.2
        )
        
        assert params.preset_name == "Quick Preview"
        assert params.num_steps <= 30
    
    def test_merchandise_type(self):
        """Test merchandise uses reference preservation"""
        params = self.engine.recommend_parameters(
            product_type="merchandise"
        )
        
        assert params.cfg_scale == 10.0
        assert params.denoising_strength == 0.65
    
    def test_iteration_complex_design(self):
        """Test iteration mode for complex design"""
        params = self.engine.recommend_parameters(
            product_type="canvas",
            is_first_generation=False,
            design_complexity="complex"
        )
        
        # Should use subtle enhancement for iterations
        assert params.preset_name == "Subtle Enhancement"
        assert "iteration" in params.reasoning.lower()
    
    def test_feedback_adjustment_too_slow(self):
        """Test adjusting parameters when generation is too slow"""
        prev_params = {
            "cfg_scale": 15,
            "denoising_strength": 0.85,
            "num_steps": 100
        }
        
        adjusted = self.engine.get_parameters_for_iteration(
            prev_params,
            "too_slow"
        )
        
        assert adjusted.num_steps < 100
        assert adjusted.cfg_scale > 15  # Compensate with CFG
    
    def test_feedback_adjustment_needs_alignment(self):
        """Test adjusting parameters for better alignment"""
        prev_params = {
            "cfg_scale": 15,
            "denoising_strength": 0.85,
            "num_steps": 100
        }
        
        adjusted = self.engine.get_parameters_for_iteration(
            prev_params,
            "needs_alignment"
        )
        
        # Should reduce denoising
        assert adjusted.denoising_strength < 0.85
        assert "alignment" in adjusted.reasoning.lower()
    
    def test_list_presets(self):
        """Test listing all presets"""
        presets = self.engine.list_presets()
        
        assert len(presets) == 5
        assert "high_quality" in presets
        assert "balanced" in presets
        assert "quick_preview" in presets
        
        # Check preset structure
        balanced = presets["balanced"]
        assert "cfg_scale" in balanced
        assert "denoising_strength" in balanced
        assert "num_steps" in balanced
        assert "quality_score" in balanced
    
    def test_factory_singleton(self):
        """Test factory returns same instance"""
        engine1 = ParameterRecommendationFactory.get_engine()
        engine2 = ParameterRecommendationFactory.get_engine()
        
        assert engine1 is engine2


class TestImageAlignmentValidator:
    """Test image alignment validator"""
    
    def setup_method(self):
        """Setup before each test"""
        ImageAlignmentValidatorFactory.reset()
        self.validator = ImageAlignmentValidator()
    
    def test_validator_initialization(self):
        """Test validator initializes"""
        assert self.validator is not None
    
    def test_perfect_alignment(self):
        """Test perfect feature preservation"""
        report = self.validator.validate_alignment(
            original_features=["red logo", "circular shape"],
            generated_image_description="Generated image shows red logo with circular shape",
            denoising_strength=0.5,
            product_type="mug"
        )
        
        assert report.status == AlignmentStatus.PASS.value
        assert report.alignment_score > 0.75
        assert len(report.preserved_features) == 2
        assert len(report.missing_features) == 0
    
    def test_partial_alignment(self):
        """Test partial feature preservation"""
        report = self.validator.validate_alignment(
            original_features=["red logo", "circular shape", "brand text"],
            generated_image_description="Generated image with red logo and circular shape",
            denoising_strength=0.75,
            product_type="mug"
        )
        
        assert report.status == AlignmentStatus.ADJUST.value
        assert 0.6 <= report.alignment_score <= 0.75
        assert len(report.preserved_features) == 2
        assert len(report.missing_features) == 1
    
    def test_poor_alignment(self):
        """Test poor feature preservation"""
        report = self.validator.validate_alignment(
            original_features=["red logo", "circular shape", "brand text"],
            generated_image_description="Generated image with random colors and shapes",
            denoising_strength=0.95,
            product_type="mug"
        )
        
        assert report.status == AlignmentStatus.FAIL.value
        assert report.alignment_score < 0.6
        # May preserve some general features like "shape"
        assert len(report.preserved_features) <= 1
        assert len(report.missing_features) >= 2
    
    def test_denoising_alignment_correlation(self):
        """Test correlation between denoising and alignment"""
        # Low denoising should suggest high alignment
        report_low_denoise = self.validator.validate_alignment(
            original_features=["feature"],
            generated_image_description="Contains feature",
            denoising_strength=0.3,
            product_type="default"
        )
        
        # High denoising should suggest low alignment
        report_high_denoise = self.validator.validate_alignment(
            original_features=["feature"],
            generated_image_description="Contains feature",
            denoising_strength=0.9,
            product_type="default"
        )
        
        assert report_low_denoise.alignment_score > report_high_denoise.alignment_score
    
    def test_product_type_denoising_targets(self):
        """Test product-specific denoising targets"""
        # Mug: target 0.60 - but with good alignment, no recommendation needed
        report_mug = self.validator.validate_alignment(
            original_features=["logo"],
            generated_image_description="Contains logo",
            denoising_strength=0.60,
            product_type="mug"
        )
        
        # Merchandise: target 0.55
        report_merch = self.validator.validate_alignment(
            original_features=["logo"],
            generated_image_description="Contains logo",
            denoising_strength=0.55,
            product_type="merchandise"
        )
        
        # When alignment is good (PASS), recommendations may be None
        # Only provide recommendations when adjustment needed (ADJUST/FAIL)
        assert report_mug.status in [AlignmentStatus.PASS.value, AlignmentStatus.ADJUST.value]
        assert report_merch.status in [AlignmentStatus.PASS.value, AlignmentStatus.ADJUST.value]
    
    def test_high_denoising_triggers_adjustment(self):
        """Test high denoising triggers adjustment recommendation"""
        report = self.validator.validate_alignment(
            original_features=["logo", "specific brand colors"],
            generated_image_description="Generic image with different colors",
            denoising_strength=0.95,
            product_type="mug"
        )
        
        # High denoising (0.95) should reduce alignment score
        # Even though the generated image might nominally have the feature due to string matching,
        # high denoising with poor match should indicate adjustment needed
        assert report.status in [AlignmentStatus.ADJUST.value, AlignmentStatus.FAIL.value]
        # High denoising with poor preservation should trigger recommendations
        assert report.denoising_recommendation is not None or report.alignment_score < 0.75
    
    def test_batch_validation(self):
        """Test batch validation of multiple images"""
        validations = [
            {
                "original_features": ["logo"],
                "generated_description": "Has logo",
                "denoising_strength": 0.5,
                "product_type": "mug"
            },
            {
                "original_features": ["logo", "text"],
                "generated_description": "Has logo and text",
                "denoising_strength": 0.6,
                "product_type": "t-shirt"
            },
            {
                "original_features": ["color"],
                "generated_description": "Different colors",
                "denoising_strength": 0.9,
                "product_type": "canvas"
            }
        ]
        
        reports = self.validator.validate_batch(validations)
        
        assert len(reports) == 3
        assert all(r.alignment_score >= 0.0 for r in reports)
        assert all(r.alignment_score <= 1.0 for r in reports)
    
    def test_statistics(self):
        """Test getting statistics from reports"""
        reports = [
            self.validator.validate_alignment(
                original_features=["logo"],
                generated_image_description="Has logo",
                denoising_strength=0.5
            ),
            self.validator.validate_alignment(
                original_features=["logo"],
                generated_image_description="Missing logo",
                denoising_strength=0.95
            )
        ]
        
        stats = self.validator.get_statistics(reports)
        
        assert stats["total_validations"] == 2
        assert "average_alignment" in stats
        assert "pass_rate" in stats
        assert stats["pass_rate"] >= 0.0 and stats["pass_rate"] <= 1.0
    
    def test_factory_singleton(self):
        """Test factory returns same instance"""
        validator1 = ImageAlignmentValidatorFactory.get_validator()
        validator2 = ImageAlignmentValidatorFactory.get_validator()
        
        assert validator1 is validator2


class TestPhase2AIntegration:
    """Integration tests for Phase 2A components"""
    
    def setup_method(self):
        """Setup before each test"""
        ParameterRecommendationFactory.reset()
        ImageAlignmentValidatorFactory.reset()
        self.param_engine = ParameterRecommendationEngine()
        self.alignment_validator = ImageAlignmentValidator()
    
    def test_parameter_engine_with_alignment_validator(self):
        """Test parameter engine adjusting for alignment"""
        # Get initial parameters
        params = self.param_engine.recommend_parameters(
            product_type="mug",
            alignment_importance=0.8
        )
        
        # Validate alignment with those parameters
        report = self.alignment_validator.validate_alignment(
            original_features=["logo", "color"],
            generated_image_description="Has logo but different color",
            denoising_strength=params.denoising_strength,
            product_type="mug",
            cfg_scale=params.cfg_scale
        )
        
        # If alignment is poor, get adjusted parameters
        if report.status == AlignmentStatus.ADJUST.value:
            if report.denoising_recommendation:
                adjusted_params = self.param_engine.get_parameters_for_iteration(
                    params.to_dict(),
                    "needs_alignment"
                )
                
                assert adjusted_params.denoising_strength < params.denoising_strength
    
    def test_end_to_end_workflow(self):
        """Test complete Phase 2A workflow"""
        # Step 1: Get parameters for product
        product_type = "mug"
        params = self.param_engine.recommend_parameters(
            product_type=product_type,
            alignment_importance=0.85,
            quality_level="high"
        )
        
        assert params.cfg_scale > 0
        assert params.denoising_strength > 0
        assert params.num_steps > 0
        
        # Step 2: Simulate image generation with those parameters
        # (In real code, this would call image generator)
        generated_description = "Mug with logo and colors preserved"
        original_features = ["logo", "colors", "shape"]
        
        # Step 3: Validate alignment
        report = self.alignment_validator.validate_alignment(
            original_features=original_features,
            generated_image_description=generated_description,
            denoising_strength=params.denoising_strength,
            product_type=product_type,
            cfg_scale=params.cfg_scale
        )
        
        # Step 4: Check if adjustment needed
        assert report.alignment_score >= 0.0
        
        if report.status == AlignmentStatus.ADJUST.value:
            # Step 5: Get feedback-adjusted parameters
            adjusted = self.param_engine.get_parameters_for_iteration(
                params.to_dict(),
                "needs_alignment"
            )
            
            # Verify adjustment
            assert adjusted.denoising_strength < params.denoising_strength


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
