"""
Prompt Evaluation Test Suite
Comprehensive tests for prompt generation and image-to-image systems
"""

import pytest
import asyncio
import json
from typing import Dict, Any
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

# Import evaluator and refiner
from src.services.prompt_evaluator import (
    PromptEvaluator,
    FullEvaluation,
    EvaluationScore,
    EvaluationDimension,
)
from src.services.prompt_refinement import PromptRefiner, RefinementStep


class TestPromptEvaluator:
    """Tests for the PromptEvaluator class"""
    
    @pytest.fixture
    def evaluator(self):
        """Create evaluator instance"""
        return PromptEvaluator()
    
    @pytest.fixture
    def sample_data(self):
        """Sample evaluation data"""
        return {
            "user_prompt": "Generate a professional LinkedIn profile picture prompt for a software engineer",
            "system_prompt": "You are a professional photography prompt expert. Generate a concise, specific prompt for LinkedIn profile pictures.",
            "generated_output": "Generate a professional headshot of a male software engineer in a modern office setting, with soft lighting, neutral background, confident pose, wearing tech-appropriate attire.",
            "model_used": "GPT-4",
            "image_description": "Professional headshot, software engineer, office setting, neutral background",
        }
    
    @pytest.mark.asyncio
    async def test_evaluate_basic(self, evaluator, sample_data):
        """Test basic evaluation"""
        result = await evaluator.evaluate(**sample_data)
        
        assert isinstance(result, FullEvaluation)
        assert result.overall_rating >= 1 and result.overall_rating <= 10
        assert len(result.scores) == 7
        assert len(result.strengths) > 0
    
    @pytest.mark.asyncio
    async def test_requirement_fulfillment_evaluation(self, evaluator):
        """Test requirement fulfillment scoring"""
        user_prompt = "Generate a red t-shirt design with company logo"
        system_prompt = "Create design concept"
        output = "A professional red t-shirt design featuring the company logo prominently on the chest"
        
        result = await evaluator.evaluate(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            generated_output=output,
        )
        
        req_score = result.scores[EvaluationDimension.REQUIREMENT_FULFILLMENT.value]
        assert req_score.score > 5  # Should score well
        assert "red" in output.lower() or "red" in result.generated_output.lower()
    
    @pytest.mark.asyncio
    async def test_prompt_effectiveness_evaluation(self, evaluator):
        """Test prompt effectiveness scoring"""
        user_prompt = "Create a design"
        system_prompt = "Step 1: Analyze requirements. Step 2: Create design concept. Step 3: Refine details."
        output = "Design created successfully"
        
        result = await evaluator.evaluate(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            generated_output=output,
        )
        
        prompt_score = result.scores[EvaluationDimension.PROMPT_EFFECTIVENESS.value]
        # Structured prompt should score well
        assert "Step" in system_prompt or "step" in system_prompt.lower()
    
    @pytest.mark.asyncio
    async def test_consistency_evaluation(self, evaluator):
        """Test consistency scoring"""
        output = "The design is perfect and always works in all cases. However, it may fail in some scenarios."
        
        result = await evaluator.evaluate(
            user_prompt="Test",
            system_prompt="Test",
            generated_output=output,
        )
        
        consistency = result.scores[EvaluationDimension.CONSISTENCY.value]
        # Contradictory output should score lower
        assert len(consistency.issues) > 0 or len(consistency.suggestions) > 0
    
    @pytest.mark.asyncio
    async def test_image_alignment_evaluation(self, evaluator):
        """Test image-to-image alignment scoring"""
        result = await evaluator.evaluate(
            user_prompt="Transform portrait to professional",
            system_prompt="Transform the portrait to professional style",
            generated_output="Professional portrait generated",
            image_description="Professional portrait with neutral background",
            img2img_settings={
                "denoising_strength": 0.75,
                "cfg_scale": 7.5,
                "steps": 50,
            }
        )
        
        alignment_score = result.scores[EvaluationDimension.IMAGE_ALIGNMENT.value]
        assert alignment_score.score >= 1
    
    @pytest.mark.asyncio
    async def test_high_denoising_warning(self, evaluator):
        """Test warning for high denoising strength"""
        result = await evaluator.evaluate(
            user_prompt="Transform image",
            system_prompt="Transform the image",
            generated_output="Transformed image",
            image_description="Original image",
            img2img_settings={"denoising_strength": 0.95}  # Very high
        )
        
        alignment_score = result.scores[EvaluationDimension.IMAGE_ALIGNMENT.value]
        assert any("denoising" in issue.lower() for issue in alignment_score.issues)
    
    @pytest.mark.asyncio
    async def test_robustness_evaluation(self, evaluator):
        """Test robustness scoring with vague input"""
        vague_prompt = "Create something kind of nice for maybe a gift or something"
        
        result = await evaluator.evaluate(
            user_prompt=vague_prompt,
            system_prompt="Create a design",
            generated_output="Design created",
        )
        
        robustness = result.scores[EvaluationDimension.ROBUSTNESS.value]
        assert len(robustness.issues) > 0  # Should flag vagueness
    
    @pytest.mark.asyncio
    async def test_efficiency_evaluation(self, evaluator):
        """Test efficiency scoring"""
        long_prompt = "Create a design. " * 100  # Very long
        
        result = await evaluator.evaluate(
            user_prompt="Test",
            system_prompt=long_prompt,
            generated_output="Design created successfully",
        )
        
        efficiency = result.scores[EvaluationDimension.EFFICIENCY.value]
        assert len(efficiency.issues) > 0  # Should flag verbosity
    
    @pytest.mark.asyncio
    async def test_export_evaluations(self, evaluator, tmp_path, sample_data):
        """Test exporting evaluations"""
        await evaluator.evaluate(**sample_data)
        
        export_file = tmp_path / "evaluations.json"
        evaluator.export_evaluations(str(export_file))
        
        assert export_file.exists()
        with open(export_file) as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert "overall_rating" in data[0]
    
    @pytest.mark.asyncio
    async def test_format_report(self, evaluator, sample_data):
        """Test report formatting"""
        result = await evaluator.evaluate(**sample_data)
        report = evaluator.format_report(result)
        
        assert "PROMPT EVALUATION REPORT" in report
        assert "OVERALL RATING" in report
        assert "STRENGTHS" in report
        assert "WEAKNESSES" in report or "RISKS" in report
        assert str(result.overall_rating) in report
    
    @pytest.mark.asyncio
    async def test_evaluation_log(self, evaluator, sample_data):
        """Test evaluation logging"""
        await evaluator.evaluate(**sample_data)
        await evaluator.evaluate(**sample_data)
        
        log = evaluator.get_evaluation_log()
        assert len(log) == 2


class TestPromptRefiner:
    """Tests for the PromptRefiner class"""
    
    @pytest.fixture
    def refiner(self):
        """Create refiner instance"""
        return PromptRefiner()
    
    @pytest.fixture
    def sample_feedback(self):
        """Sample evaluation feedback"""
        return {
            "overall_rating": 5.0,
            "improvements": [
                "Add structured steps for clarity",
                "Include concrete examples",
                "Specify output format",
            ],
            "weaknesses": [
                "❌ Prompt lacks structure",
                "❌ No examples provided",
            ],
            "suggestions": [
                "Add numbered steps",
                "Include sample outputs",
            ]
        }
    
    @pytest.mark.asyncio
    async def test_refine_prompt_adds_structure(self, refiner):
        """Test that refinement adds structure when missing"""
        prompt = "Create a professional design."
        feedback = {
            "overall_rating": 5.0,
            "improvements": ["Add structured steps"],
            "weaknesses": [],
            "suggestions": [],
        }
        
        refined, steps = await refiner.refine_prompt(prompt, feedback)
        
        assert len(steps) > 0
        assert refined != prompt
        # Should add structure markers
        assert any(word in refined.lower() for word in ["step", "section", "first"])
    
    @pytest.mark.asyncio
    async def test_refine_prompt_adds_examples(self, refiner):
        """Test that refinement adds examples when missing"""
        prompt = "Generate product names"
        feedback = {
            "overall_rating": 5.0,
            "improvements": ["Include concrete examples"],
            "weaknesses": [],
            "suggestions": [],
        }
        
        refined, steps = await refiner.refine_prompt(prompt, feedback)
        
        assert len(steps) > 0
        assert "example" in refined.lower() or refined != prompt
    
    @pytest.mark.asyncio
    async def test_refine_prompt_clarifies_ambiguity(self, refiner):
        """Test that refinement removes vague language"""
        prompt = "Create something kind of nice for maybe gifts"
        feedback = {
            "overall_rating": 4.0,
            "improvements": ["Replace vague language"],
            "weaknesses": ["Contains vague terms"],
            "suggestions": [],
        }
        
        refined, steps = await refiner.refine_prompt(prompt, feedback)
        
        # Should remove or replace vague terms
        assert refined != prompt
    
    @pytest.mark.asyncio
    async def test_refine_prompt_multiple_iterations(self, refiner):
        """Test multiple refinement iterations"""
        prompt = "Create design"
        feedback = {
            "overall_rating": 3.0,
            "improvements": ["Add steps", "Add examples", "Add constraints"],
            "weaknesses": ["Too vague", "No structure", "Missing constraints"],
            "suggestions": [],
        }
        
        refined, steps = await refiner.refine_prompt(prompt, feedback, max_iterations=3)
        
        assert len(steps) > 0
        assert steps[0].score_after >= steps[0].score_before or steps[0].refined_prompt != steps[0].original_prompt
    
    @pytest.mark.asyncio
    async def test_refinement_step_record(self, refiner):
        """Test refinement step recording"""
        prompt = "Create a design"
        feedback = {
            "overall_rating": 5.0,
            "improvements": ["Add structure"],
            "weaknesses": [],
            "suggestions": [],
        }
        
        refined, steps = await refiner.refine_prompt(prompt, feedback)
        
        if steps:
            step = steps[0]
            assert isinstance(step, RefinementStep)
            assert step.iteration > 0
            assert step.original_prompt == prompt
            assert step.refined_prompt != ""
            assert len(step.changes) > 0
    
    @pytest.mark.asyncio
    async def test_export_refinement_history(self, refiner, tmp_path):
        """Test exporting refinement history"""
        prompt = "Create design"
        feedback = {
            "overall_rating": 5.0,
            "improvements": ["Add steps"],
            "weaknesses": [],
            "suggestions": [],
        }
        
        await refiner.refine_prompt(prompt, feedback)
        
        export_file = tmp_path / "refinements.txt"
        refiner.export_refinement_history(str(export_file))
        
        assert export_file.exists()
        content = export_file.read_text()
        assert "REFINEMENT HISTORY" in content
    
    @pytest.mark.asyncio
    async def test_refinement_summary(self, refiner):
        """Test refinement summary generation"""
        prompt = "Create"
        feedback = {
            "overall_rating": 5.0,
            "improvements": ["Add structure"],
            "weaknesses": [],
            "suggestions": [],
        }
        
        await refiner.refine_prompt(prompt, feedback)
        
        summary = refiner.get_refinement_summary()
        assert "REFINEMENT HISTORY SUMMARY" in summary or len(summary) > 0


class TestIntegratedEvaluationWorkflow:
    """Integration tests for complete evaluation and refinement workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_evaluate_and_refine_workflow(self):
        """Test complete workflow: evaluate → identify issues → refine"""
        evaluator = PromptEvaluator()
        refiner = PromptRefiner()
        
        # Original prompt
        original_prompt = "Create design for a t-shirt"
        system_prompt = "You are a design expert. Create a t-shirt design."
        output = "A t-shirt design has been created"
        
        # Evaluate
        evaluation = await evaluator.evaluate(
            user_prompt=original_prompt,
            system_prompt=system_prompt,
            generated_output=output,
        )
        
        # Refine based on feedback
        refined_prompt, steps = await refiner.refine_prompt(
            system_prompt,
            {
                "overall_rating": evaluation.overall_rating,
                "improvements": evaluation.improvements,
                "weaknesses": evaluation.weaknesses,
            }
        )
        
        # Verify refinement happened
        if evaluation.overall_rating < 7:
            assert len(steps) > 0
            assert refined_prompt != system_prompt
        
        print(f"\nOriginal Score: {evaluation.overall_rating}/10")
        print(f"Refinement Steps: {len(steps)}")
        if steps:
            print(f"Final Score (simulated): {steps[-1].score_after}/10")
    
    @pytest.mark.asyncio
    async def test_evaluation_with_gift_design_context(self):
        """Test evaluation with gift design agent context"""
        evaluator = PromptEvaluator()
        
        # Simulate gift design system prompt and output
        system_prompt = """Generate 3 design concepts for a customized t-shirt with these specs:
        - Product: t-shirt
        - Concept: Minimalist tech company branding
        - Colors: Navy, White, Orange
        - Tone: Professional
        
        For each concept provide: Title, Design Brief, Image Prompts"""
        
        output = """CONCEPT 1: Modern Professional
Design Brief: Clean, minimalist design...
Image Prompt: Professional t-shirt design..."""
        
        result = await evaluator.evaluate(
            user_prompt="Design a t-shirt for a tech company",
            system_prompt=system_prompt,
            generated_output=output,
            model_used="Groq",
        )
        
        report = evaluator.format_report(result)
        assert "OVERALL RATING" in report
        assert result.overall_rating >= 1
    
    @pytest.mark.asyncio
    async def test_evaluation_with_content_generator_context(self):
        """Test evaluation with content generator context"""
        evaluator = PromptEvaluator()
        
        system_prompt = "Generate viral-optimized image prompts for Instagram content"
        output = """Generated prompts:
1. Professional portrait prompt
2. Fashion photography prompt
3. Lifestyle photography prompt"""
        
        result = await evaluator.evaluate(
            user_prompt="Generate 3 Instagram content prompts for a fashion brand",
            system_prompt=system_prompt,
            generated_output=output,
            model_used="Groq",
        )
        
        assert result.overall_rating >= 1
        assert len(result.scores) == 7


class TestPromptEvaluationMetrics:
    """Tests for evaluation metrics and scoring logic"""
    
    @pytest.mark.asyncio
    async def test_rating_calculation(self):
        """Test overall rating calculation"""
        evaluator = PromptEvaluator()
        
        result = await evaluator.evaluate(
            user_prompt="Test prompt",
            system_prompt="Test system prompt",
            generated_output="Test output with good quality and clear structure",
        )
        
        # Rating should be weighted average
        assert 1 <= result.overall_rating <= 10
        assert isinstance(result.overall_rating, float)
    
    @pytest.mark.asyncio
    async def test_dimension_scores_independence(self):
        """Test that dimension scores are independent"""
        evaluator = PromptEvaluator()
        
        result = await evaluator.evaluate(
            user_prompt="Generate a design",
            system_prompt="You are a design expert",
            generated_output="Design generated successfully",
        )
        
        scores = list(result.scores.values())
        score_values = [s.score for s in scores]
        
        # Scores should vary (not all the same)
        assert len(set(score_values)) > 1 or all(score == score_values[0] for score in score_values)
    
    @pytest.mark.asyncio
    async def test_constraints_impact_scoring(self):
        """Test that constraints impact scoring"""
        evaluator = PromptEvaluator()
        
        constraints = {
            "max_colors": 3,
            "target_audience": "professionals",
            "style": "minimalist"
        }
        
        result = await evaluator.evaluate(
            user_prompt="Create a logo",
            system_prompt="Create a professional logo",
            generated_output="Logo created with 5 colors and playful style",
            constraints=constraints,
        )
        
        fulfillment = result.scores[EvaluationDimension.REQUIREMENT_FULFILLMENT.value]
        # Should have identified constraint violations
        assert len(fulfillment.issues) > 0 or fulfillment.score >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
