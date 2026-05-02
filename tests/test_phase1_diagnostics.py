"""
Phase 1 Test Suite - Validates all diagnostics components
Tests dimension analysis, prompt auditing, and parameter optimization
"""

import pytest
import asyncio
from typing import Dict, List

# Import Phase 1 services
from src.services.dimension_analyzer import DimensionAnalyzer, DimensionType
from src.services.prompt_quality_auditor import PromptQualityAuditor
from src.services.parameter_optimizer import ParameterOptimizationMatrix, ParameterPreset


class TestDimensionAnalyzer:
    """Test dimension analysis functionality"""
    
    def test_analyzer_creation(self):
        """Test creating dimension analyzer"""
        analyzer = DimensionAnalyzer()
        assert analyzer is not None
        assert len(analyzer.evaluations) == 0
    
    def test_add_evaluation(self):
        """Test adding evaluation records"""
        analyzer = DimensionAnalyzer()
        
        eval_record = {
            "scores": {
                "requirement_fulfillment": {
                    "score": 7.0,
                    "issues": ["missing_requirement"]
                }
            }
        }
        
        analyzer.add_evaluation(eval_record)
        assert len(analyzer.evaluations) == 1
    
    def test_analyze_dimension_empty(self):
        """Test analyzing with no data"""
        analyzer = DimensionAnalyzer()
        result = analyzer.analyze_dimension("requirement_fulfillment")
        
        assert result.average_score == 0.0
        assert len(result.failure_modes) == 0
    
    def test_analyze_dimension_with_data(self):
        """Test analyzing with sample data"""
        analyzer = DimensionAnalyzer()
        
        # Add multiple evaluations
        for score in [7.0, 8.0, 6.0, 7.5]:
            analyzer.add_evaluation({
                "scores": {
                    "requirement_fulfillment": {
                        "score": score,
                        "issues": ["vague_input", "missing_requirement"]
                    }
                }
            })
        
        result = analyzer.analyze_dimension("requirement_fulfillment")
        assert result.average_score == 7.125
        assert len(result.top_issues) > 0
    
    def test_analyze_all_dimensions(self):
        """Test analyzing all 7 dimensions"""
        analyzer = DimensionAnalyzer()
        
        # Add evaluations with all dimensions
        analyzer.add_evaluation({
            "scores": {
                "requirement_fulfillment": {"score": 7.0, "issues": []},
                "prompt_effectiveness": {"score": 7.5, "issues": []},
                "image_alignment": {"score": 5.0, "issues": []},
                "consistency": {"score": 7.0, "issues": []},
                "control_parameters": {"score": 4.0, "issues": []},
                "robustness": {"score": 6.0, "issues": []},
                "efficiency": {"score": 6.5, "issues": []}
            }
        })
        
        results = analyzer.analyze_all_dimensions()
        assert len(results) == 7
        assert all(dim in results for dim in [t.value for t in DimensionType])


class TestPromptQualityAuditor:
    """Test prompt quality auditing"""
    
    def test_auditor_creation(self):
        """Test creating auditor"""
        auditor = PromptQualityAuditor()
        assert auditor is not None
    
    def test_audit_short_prompt(self):
        """Test auditing short prompt"""
        auditor = PromptQualityAuditor()
        prompt = "Generate a design."
        
        metrics = auditor.audit_prompt(prompt, "short_prompt")
        
        assert metrics.overall_quality > 0
        assert metrics.word_count == 3
        assert len(metrics.issues) > 0  # Should flag as too short
    
    def test_audit_long_prompt(self):
        """Test auditing overly long prompt"""
        auditor = PromptQualityAuditor()
        prompt = " ".join(["Generate a beautiful design for a t-shirt that looks amazing"] * 20)
        
        metrics = auditor.audit_prompt(prompt, "long_prompt")
        
        assert metrics.overall_quality > 0
        assert metrics.word_count > 100
        # Should flag as too long
        assert any("too long" in issue.lower() for issue in metrics.issues)
    
    def test_audit_well_structured_prompt(self):
        """Test auditing well-structured prompt"""
        auditor = PromptQualityAuditor()
        prompt = """You are a design expert.

1. Analyze the user's request
2. Create 3 design variations
3. Format output as JSON with: title, brief, image_prompt

Constraints:
- Keep designs professional
- Ensure brand consistency
- Output must be valid JSON"""
        
        metrics = auditor.audit_prompt(prompt, "well_structured")
        
        assert metrics.clarity_score > 6.0
        assert metrics.structure_score > 7.0
        assert len(metrics.issues) < 3
    
    def test_audit_vague_prompt(self):
        """Test auditing vague prompt"""
        auditor = PromptQualityAuditor()
        prompt = "Try to maybe create something good. Good design is important. Do your best."
        
        metrics = auditor.audit_prompt(prompt, "vague_prompt")
        
        # Should flag vague language
        assert any("uncertain" in issue.lower() for issue in metrics.issues)
        assert any("vague" in issue.lower() for issue in metrics.issues)
    
    def test_token_estimation(self):
        """Test token count estimation"""
        auditor = PromptQualityAuditor()
        prompt = "This is a test prompt with ten words in it for testing purposes."
        
        metrics = auditor.audit_prompt(prompt)
        
        # Should be rough approximation
        assert metrics.token_estimate > 0
        assert metrics.token_estimate < 50


class TestParameterOptimizer:
    """Test parameter optimization"""
    
    def test_optimizer_creation(self):
        """Test creating optimizer"""
        optimizer = ParameterOptimizationMatrix()
        assert optimizer is not None
        assert len(optimizer.parameter_data) == 0
    
    def test_add_parameter_sample(self):
        """Test adding parameter samples"""
        optimizer = ParameterOptimizationMatrix()
        
        optimizer.add_parameter_sample(
            cfg_scale=12.0,
            denoising_strength=0.75,
            num_steps=50,
            quality_score=8.0,
            image_alignment_score=7.5,
            product_type="t-shirt"
        )
        
        assert len(optimizer.parameter_data) == 1
        assert optimizer.parameter_data[0]["cfg_scale"] == 12.0
    
    def test_analyze_correlations(self):
        """Test parameter correlation analysis"""
        optimizer = ParameterOptimizationMatrix()
        
        # Add samples with varying parameters
        samples = [
            (10.0, 0.6, 30, 5.0),  # Low quality
            (12.0, 0.75, 50, 7.5),  # Medium quality
            (15.0, 0.85, 100, 9.0),  # High quality
            (12.5, 0.7, 60, 7.8),  # Medium-high quality
        ]
        
        for cfg, denoise, steps, quality in samples:
            optimizer.add_parameter_sample(
                cfg_scale=cfg,
                denoising_strength=denoise,
                num_steps=steps,
                quality_score=quality,
                image_alignment_score=quality - 0.5,
                product_type="mug"
            )
        
        correlations = optimizer.analyze_parameter_correlations()
        
        assert len(correlations) == 3  # cfg_scale, denoising_strength, num_steps
        assert all(c in correlations for c in ["cfg_scale", "denoising_strength", "num_steps"])
    
    def test_build_presets(self):
        """Test building parameter presets"""
        optimizer = ParameterOptimizationMatrix()
        presets = optimizer.build_parameter_presets()
        
        assert len(presets) >= 5
        assert all(isinstance(p, ParameterPreset) for p in presets)
        
        # Check specific presets exist
        names = [p.name for p in presets]
        assert "High Quality" in names
        assert "Balanced" in names
        assert "Quick Preview" in names
    
    def test_get_recommended_parameters(self):
        """Test getting recommended parameters"""
        optimizer = ParameterOptimizationMatrix()
        optimizer.build_parameter_presets()
        
        # Test different quality preferences
        high_quality = optimizer.get_recommended_parameters("t-shirt", "final", "high")
        assert high_quality.cfg_scale > 12.0
        
        fast = optimizer.get_recommended_parameters("t-shirt", "preview", "fast")
        assert fast.num_steps < 50


class TestPhase1Integration:
    """Integration tests for all Phase 1 components"""
    
    def test_full_analysis_workflow(self):
        """Test full diagnostic workflow"""
        # Create sample evaluation data
        evaluations = []
        for i in range(20):
            eval_record = {
                "scores": {
                    "requirement_fulfillment": {
                        "score": 6 + (i % 3),
                        "issues": ["vague_input", "missing_requirement"]
                    },
                    "prompt_effectiveness": {
                        "score": 7 + (i % 2),
                        "issues": ["long_prompt"]
                    },
                    "image_alignment": {
                        "score": 4 + (i % 2),
                        "issues": ["high_denoising"]
                    },
                    "consistency": {
                        "score": 7,
                        "issues": []
                    },
                    "control_parameters": {
                        "score": 4,
                        "issues": ["default_parameters"]
                    },
                    "robustness": {
                        "score": 6,
                        "issues": ["edge_case_unhandled"]
                    },
                    "efficiency": {
                        "score": 6.5,
                        "issues": ["overlong_prompt"]
                    }
                }
            }
            evaluations.append(eval_record)
        
        # Run analysis
        analyzer = DimensionAnalyzer()
        for eval in evaluations:
            analyzer.add_evaluation(eval)
        
        analyses = analyzer.analyze_all_dimensions()
        
        # Verify results
        assert len(analyses) == 7
        assert analyses["requirement_fulfillment"].average_score > 0
        assert analyses["control_parameters"].average_score < 5  # Known low area
        assert analyses["image_alignment"].average_score < 6  # Known low area
    
    def test_prompt_audit_all_system_prompts(self):
        """Test auditing multiple system prompts"""
        auditor = PromptQualityAuditor()
        
        prompts = {
            "gift_design_prompt": "You are a gift design expert. " * 50,  # Long
            "content_generator_prompt": "Generate viral image prompts.",  # Short
            "balanced_prompt": "You are an AI assistant.\n\n1. Analyze input\n2. Generate output\n\nFormat: JSON",
        }
        
        audits = auditor.audit_all_system_prompts(prompts)
        
        assert len(audits) == 3
        assert audits["gift_design_prompt"].conciseness_score < 7  # Too long
        assert audits["content_generator_prompt"].clarity_score < 7  # Too short
        assert audits["balanced_prompt"].overall_quality > 6  # Balanced
    
    def test_export_functionality(self):
        """Test exporting analysis results"""
        import tempfile
        import json
        import os
        
        # Create analyzer with data
        analyzer = DimensionAnalyzer()
        analyzer.add_evaluation({
            "scores": {
                "requirement_fulfillment": {"score": 7.0, "issues": []}
            }
        })
        
        analyses = analyzer.analyze_all_dimensions()
        
        # Export to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            analyzer.export_analysis(temp_path, analyses)
            
            # Verify file exists and is valid JSON
            assert os.path.exists(temp_path)
            with open(temp_path) as f:
                data = json.load(f)
            
            assert "timestamp" in data
            assert "dimensions" in data
            assert len(data["dimensions"]) == 7
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


# Test execution
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
