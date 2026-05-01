"""
Prompt Evaluation Service
Comprehensive evaluation of prompt-generation and image-to-image systems
Based on meta-prompt framework for system quality assurance
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class EvaluationDimension(Enum):
    """Evaluation criteria dimensions"""
    REQUIREMENT_FULFILLMENT = "requirement_fulfillment"
    PROMPT_EFFECTIVENESS = "prompt_effectiveness"
    IMAGE_ALIGNMENT = "image_alignment"
    CONSISTENCY = "consistency"
    CONTROL_PARAMETERS = "control_parameters"
    ROBUSTNESS = "robustness"
    EFFICIENCY = "efficiency"


@dataclass
class EvaluationScore:
    """Single dimension evaluation score"""
    dimension: str
    score: float  # 1-10
    details: str
    issues: List[str]
    suggestions: List[str]


@dataclass
class FullEvaluation:
    """Complete system evaluation result"""
    timestamp: str
    user_prompt: str
    system_prompt: str
    generated_output: str
    image_description: Optional[str]
    model_used: str
    
    scores: Dict[str, EvaluationScore]
    strengths: List[str]
    weaknesses: List[str]
    risks: List[str]
    improvements: List[str]
    suggested_prompt: str
    overall_rating: float  # 1-10
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp,
            "user_prompt": self.user_prompt,
            "system_prompt": self.system_prompt,
            "generated_output": self.generated_output,
            "image_description": self.image_description,
            "model_used": self.model_used,
            "scores": {k: asdict(v) for k, v in self.scores.items()},
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "risks": self.risks,
            "improvements": self.improvements,
            "suggested_prompt": self.suggested_prompt,
            "overall_rating": self.overall_rating,
        }


class PromptEvaluator:
    """
    Main evaluator class implementing the meta-prompt framework
    Provides multi-dimensional evaluation of prompt generation systems
    """
    
    def __init__(self):
        self.logger = logger
        self.evaluations_log: List[FullEvaluation] = []
    
    async def evaluate(
        self,
        user_prompt: str,
        system_prompt: str,
        generated_output: str,
        model_used: str = "unknown",
        image_description: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None,
        img2img_settings: Optional[Dict[str, Any]] = None,
    ) -> FullEvaluation:
        """
        Comprehensive evaluation of system output
        
        Args:
            user_prompt: Original user request
            system_prompt: Prompt given to the model
            generated_output: Model's generated output
            model_used: Name of model used
            image_description: Description or path to generated image
            constraints: User-specified constraints/preferences
            img2img_settings: Image-to-image parameters if applicable
        
        Returns:
            FullEvaluation with detailed analysis
        """
        try:
            # Initialize scores dictionary
            scores = {}
            
            # Evaluate each dimension
            scores[EvaluationDimension.REQUIREMENT_FULFILLMENT.value] = \
                self._evaluate_requirement_fulfillment(user_prompt, generated_output, constraints)
            
            scores[EvaluationDimension.PROMPT_EFFECTIVENESS.value] = \
                self._evaluate_prompt_effectiveness(system_prompt, generated_output)
            
            scores[EvaluationDimension.IMAGE_ALIGNMENT.value] = \
                self._evaluate_image_alignment(image_description, system_prompt, img2img_settings)
            
            scores[EvaluationDimension.CONSISTENCY.value] = \
                self._evaluate_consistency(generated_output, system_prompt)
            
            scores[EvaluationDimension.CONTROL_PARAMETERS.value] = \
                self._evaluate_control_parameters(img2img_settings, generated_output)
            
            scores[EvaluationDimension.ROBUSTNESS.value] = \
                self._evaluate_robustness(user_prompt, system_prompt)
            
            scores[EvaluationDimension.EFFICIENCY.value] = \
                self._evaluate_efficiency(system_prompt, generated_output)
            
            # Extract strengths, weaknesses, risks, improvements
            strengths = self._extract_strengths(scores)
            weaknesses = self._extract_weaknesses(scores)
            risks = self._extract_risks(scores, user_prompt)
            improvements = self._extract_improvements(scores)
            
            # Generate improved prompt
            suggested_prompt = self._generate_improved_prompt(
                user_prompt,
                system_prompt,
                generated_output,
                weaknesses
            )
            
            # Calculate overall rating
            overall_rating = self._calculate_overall_rating(scores)
            
            # Create evaluation object
            evaluation = FullEvaluation(
                timestamp=datetime.now().isoformat(),
                user_prompt=user_prompt,
                system_prompt=system_prompt,
                generated_output=generated_output,
                image_description=image_description,
                model_used=model_used,
                scores=scores,
                strengths=strengths,
                weaknesses=weaknesses,
                risks=risks,
                improvements=improvements,
                suggested_prompt=suggested_prompt,
                overall_rating=overall_rating,
            )
            
            # Log evaluation
            self.evaluations_log.append(evaluation)
            self.logger.info(f"Evaluation complete: {overall_rating}/10")
            
            return evaluation
            
        except Exception as e:
            self.logger.error(f"Evaluation failed: {str(e)}")
            raise
    
    def _evaluate_requirement_fulfillment(
        self,
        user_prompt: str,
        output: str,
        constraints: Optional[Dict[str, Any]] = None
    ) -> EvaluationScore:
        """Evaluate if output satisfies user requirements"""
        issues = []
        suggestions = []
        details = ""
        
        # Check if output length is reasonable
        if not output or len(output.strip()) < 10:
            issues.append("Output too brief or missing")
            suggestions.append("Ensure output is substantive and detailed")
        
        # Check for key requirement indicators
        requirements = user_prompt.lower().split()
        matched = 0
        for req in requirements:
            if len(req) > 3 and req in output.lower():
                matched += 1
        
        requirement_match_ratio = matched / len([r for r in requirements if len(r) > 3]) if requirements else 0
        
        if requirement_match_ratio < 0.3:
            issues.append("Low alignment with user requirements")
            suggestions.append("Ensure key user requirements are explicitly addressed")
        
        if constraints:
            for constraint_key, constraint_val in constraints.items():
                if str(constraint_val).lower() not in output.lower():
                    issues.append(f"Constraint not met: {constraint_key}")
                    suggestions.append(f"Include explicit handling of {constraint_key}")
        
        # Determine implicit needs
        if "must" in user_prompt.lower() or "should" in user_prompt.lower():
            if not any(word in output.lower() for word in ["ensure", "must", "required"]):
                suggestions.append("Include explicit statements about mandatory requirements")
        
        score = 10 - (len(issues) * 1.5)
        score = max(1, min(10, score))
        details = f"Requirement match: {requirement_match_ratio*100:.1f}%. Issues: {len(issues)}"
        
        return EvaluationScore(
            dimension=EvaluationDimension.REQUIREMENT_FULFILLMENT.value,
            score=score,
            details=details,
            issues=issues,
            suggestions=suggestions,
        )
    
    def _evaluate_prompt_effectiveness(self, prompt: str, output: str) -> EvaluationScore:
        """Evaluate prompt clarity, specificity, and guidance"""
        issues = []
        suggestions = []
        
        # Check prompt clarity
        prompt_words = prompt.split()
        if len(prompt_words) < 5:
            issues.append("Prompt is too brief (lacks specificity)")
            suggestions.append("Expand with specific examples and constraints")
        
        if len(prompt_words) > 500:
            issues.append("Prompt is excessively long (potential ambiguity)")
            suggestions.append("Condense to essential guidance only")
        
        # Check for clear structure
        has_structure = any(phrase in prompt.lower() for phrase in 
                           ["step", "section", "first", "then", "finally", "requirement"])
        
        if not has_structure:
            suggestions.append("Add structural markers (steps, sections) for clarity")
        
        # Check for contradictions in prompt
        negative_markers = ["not", "avoid", "don't", "without"]
        positive_markers = ["ensure", "include", "add", "must"]
        
        if any(marker in prompt.lower() for marker in negative_markers):
            if not any(marker in prompt.lower() for marker in positive_markers):
                suggestions.append("Balance negative constraints with positive guidance")
        
        # Check if output aligns with prompt specificity
        output_words = len(output.split())
        prompt_to_output_ratio = len(prompt_words) / max(1, output_words)
        
        if prompt_to_output_ratio > 0.5:
            issues.append("Prompt is verbose relative to output")
        elif prompt_to_output_ratio < 0.05:
            suggestions.append("Consider if prompt is too minimal for the output")
        
        score = 10 - (len(issues) * 1.5) - (len(suggestions) * 0.5)
        score = max(1, min(10, score))
        
        return EvaluationScore(
            dimension=EvaluationDimension.PROMPT_EFFECTIVENESS.value,
            score=score,
            details=f"Prompt length: {len(prompt_words)} words. Structure clarity: {'good' if has_structure else 'poor'}",
            issues=issues,
            suggestions=suggestions,
        )
    
    def _evaluate_image_alignment(
        self,
        image_desc: Optional[str],
        prompt: str,
        img2img_settings: Optional[Dict[str, Any]] = None
    ) -> EvaluationScore:
        """Evaluate image-to-image transformation alignment"""
        issues = []
        suggestions = []
        
        # Only evaluate if image provided
        if not image_desc:
            return EvaluationScore(
                dimension=EvaluationDimension.IMAGE_ALIGNMENT.value,
                score=10,  # N/A
                details="No image provided for evaluation",
                issues=[],
                suggestions=["Provide image descriptions for image-to-image evaluation"],
            )
        
        # Check denoising strength if provided
        if img2img_settings:
            denoising = img2img_settings.get("denoising_strength", 0.5)
            
            if denoising > 0.8:
                issues.append("High denoising strength may destroy original image features")
                suggestions.append("Reduce denoising strength to 0.5-0.7 to preserve identity")
            
            if denoising < 0.2:
                issues.append("Low denoising strength may not apply requested changes")
                suggestions.append("Increase denoising strength to 0.4-0.6 for visible transformation")
            
            cfg_scale = img2img_settings.get("cfg_scale", 7.5)
            if cfg_scale < 3:
                issues.append("Low CFG scale may ignore prompt instructions")
                suggestions.append("Increase CFG scale to 7-15 for stronger alignment")
            
            if cfg_scale > 20:
                issues.append("Excessive CFG scale may cause artifacts")
                suggestions.append("Reduce CFG scale to 7-15 for balanced results")
        
        # Check prompt-image description consistency
        if image_desc and prompt:
            image_words = set(image_desc.lower().split())
            prompt_words = set(prompt.lower().split())
            
            # Find alignment
            aligned_words = image_words & prompt_words
            if len(aligned_words) < 3:
                suggestions.append("Ensure image description and prompt share key concepts")
        
        score = 10 - (len(issues) * 2)
        score = max(1, min(10, score))
        
        return EvaluationScore(
            dimension=EvaluationDimension.IMAGE_ALIGNMENT.value,
            score=score,
            details=f"Parameters configured: {bool(img2img_settings)}. Alignment issues: {len(issues)}",
            issues=issues,
            suggestions=suggestions,
        )
    
    def _evaluate_consistency(self, output: str, prompt: str) -> EvaluationScore:
        """Evaluate logical consistency and coherence"""
        issues = []
        suggestions = []
        
        # Check for contradictions in output
        output_lower = output.lower()
        
        # Common contradiction patterns
        contradictions = [
            (["should", "shouldn't"], "logical contradiction"),
            (["required", "optional"], "requirement contradiction"),
            (["always", "never"], "absolute contradiction"),
            (["impossible", "must be done"], "feasibility contradiction"),
        ]
        
        for word_pair, desc in contradictions:
            if all(word in output_lower for word in word_pair):
                issues.append(f"Detected {desc}")
                suggestions.append(f"Clarify conflicting guidance around: {', '.join(word_pair)}")
        
        # Check for hallucinations (generic or unrealistic statements)
        hallucination_markers = ["infinite", "100% guaranteed", "perfect", "always works", "never fails"]
        if any(marker in output_lower for marker in hallucination_markers):
            issues.append("Output contains unrealistic guarantees")
            suggestions.append("Use qualified language ('may', 'can', 'likely')")
        
        # Check narrative flow
        sentences = output.split(".")
        if len(sentences) > 1:
            # Check if later sentences contradict earlier ones
            first_half = " ".join(sentences[:len(sentences)//2]).lower()
            second_half = " ".join(sentences[len(sentences)//2:]).lower()
            
            # Simple check: count matching key terms
            first_terms = set(first_half.split())
            second_terms = set(second_half.split())
            
            if len(first_terms & second_terms) < len(first_terms) * 0.3:
                suggestions.append("Ensure consistent terminology and themes throughout")
        
        score = 10 - (len(issues) * 2) - (len(suggestions) * 0.3)
        score = max(1, min(10, score))
        
        return EvaluationScore(
            dimension=EvaluationDimension.CONSISTENCY.value,
            score=score,
            details=f"Output length: {len(output.split())} words. Contradictions detected: {len(issues)}",
            issues=issues,
            suggestions=suggestions,
        )
    
    def _evaluate_control_parameters(
        self,
        parameters: Optional[Dict[str, Any]],
        output: str
    ) -> EvaluationScore:
        """Evaluate parameter usage effectiveness"""
        issues = []
        suggestions = []
        
        if not parameters:
            return EvaluationScore(
                dimension=EvaluationDimension.CONTROL_PARAMETERS.value,
                score=7,  # Neutral - no parameters to evaluate
                details="No parameters provided",
                issues=[],
                suggestions=["Specify parameters for more effective evaluation"],
            )
        
        # Validate common parameters
        valid_ranges = {
            "denoising_strength": (0, 1),
            "cfg_scale": (1, 20),
            "steps": (20, 150),
            "temperature": (0, 2),
            "top_p": (0, 1),
        }
        
        for param, value in parameters.items():
            if param in valid_ranges:
                min_val, max_val = valid_ranges[param]
                if not (min_val <= value <= max_val):
                    issues.append(f"{param}={value} outside recommended range [{min_val}, {max_val}]")
                    suggestions.append(f"Set {param} to {(min_val + max_val) / 2:.1f} as default")
        
        # Check if parameters are tuned for the task
        if parameters.get("steps", 50) < 30:
            suggestions.append("Increase steps (>30) for better quality")
        
        if parameters.get("cfg_scale", 7.5) == 7.5:  # Default
            suggestions.append("Consider tuning CFG scale based on desired adherence to prompt")
        
        score = 10 - (len(issues) * 1.5) - (len(suggestions) * 0.5)
        score = max(1, min(10, score))
        
        return EvaluationScore(
            dimension=EvaluationDimension.CONTROL_PARAMETERS.value,
            score=score,
            details=f"Parameters provided: {len(parameters)}. Parameter issues: {len(issues)}",
            issues=issues,
            suggestions=suggestions,
        )
    
    def _evaluate_robustness(self, user_input: str, system_prompt: str) -> EvaluationScore:
        """Evaluate system's handling of vague/complex inputs"""
        issues = []
        suggestions = []
        
        # Check for vague language in user input
        vague_terms = ["something", "some", "maybe", "kind of", "sort of", "probably", "kinda"]
        vagueness_count = sum(1 for term in vague_terms if term in user_input.lower())
        
        if vagueness_count > 2:
            issues.append("User input contains vague language")
            suggestions.append("Request clarification for ambiguous terms")
        
        # Check if system prompt handles edge cases
        edge_case_handlers = ["if", "unless", "except", "handle", "error", "fallback"]
        has_edge_case_handling = sum(1 for phrase in edge_case_handlers if phrase in system_prompt.lower())
        
        if has_edge_case_handling < 2:
            issues.append("System prompt lacks edge case handling")
            suggestions.append("Add explicit instructions for handling ambiguous inputs")
        
        # Check for complexity
        input_words = len(user_input.split())
        prompt_words = len(system_prompt.split())
        
        if input_words > 100 and prompt_words < 50:
            issues.append("Complex input with minimal system guidance")
            suggestions.append("Expand system prompt to handle complex requirements")
        
        score = 10 - (len(issues) * 2) - (len(suggestions) * 0.5)
        score = max(1, min(10, score))
        
        return EvaluationScore(
            dimension=EvaluationDimension.ROBUSTNESS.value,
            score=score,
            details=f"Vagueness indicators: {vagueness_count}. Edge case handlers: {has_edge_case_handling}",
            issues=issues,
            suggestions=suggestions,
        )
    
    def _evaluate_efficiency(self, prompt: str, output: str) -> EvaluationScore:
        """Evaluate prompt efficiency (brevity without losing clarity)"""
        issues = []
        suggestions = []
        
        prompt_words = len(prompt.split())
        output_words = len(output.split())
        
        # Calculate redundancy
        prompt_lower = prompt.lower()
        repeated_words = {}
        
        for word in prompt_lower.split():
            if len(word) > 4:  # Only check significant words
                repeated_words[word] = repeated_words.get(word, 0) + 1
        
        highly_repeated = sum(1 for count in repeated_words.values() if count > 3)
        
        if highly_repeated > 0:
            issues.append("Prompt contains repeated concepts")
            suggestions.append("Consolidate repeated guidance into single clear instruction")
        
        # Check for unnecessary sections
        if prompt_words > 300:
            issues.append("Prompt is verbose (>300 words)")
            suggestions.append("Aim for 100-200 word prompts for clarity and cost efficiency")
        
        if prompt_words < 20 and output_words > 200:
            suggestions.append("Consider expanding prompt for better control")
        
        # Calculate efficiency ratio
        efficiency_ratio = prompt_words / max(1, output_words)
        
        score = 10
        if efficiency_ratio > 0.5:
            score -= 2  # Too verbose
        if efficiency_ratio < 0.02 and output_words > 100:
            score -= 1  # Too minimal
        
        score = max(1, min(10, score))
        
        return EvaluationScore(
            dimension=EvaluationDimension.EFFICIENCY.value,
            score=score,
            details=f"Prompt: {prompt_words} words, Output: {output_words} words. Ratio: {efficiency_ratio:.3f}",
            issues=issues,
            suggestions=suggestions,
        )
    
    def _extract_strengths(self, scores: Dict[str, EvaluationScore]) -> List[str]:
        """Extract high-scoring dimensions as strengths"""
        strengths = []
        for dimension, score in scores.items():
            if score.score >= 8:
                if dimension == EvaluationDimension.REQUIREMENT_FULFILLMENT.value:
                    strengths.append("✅ Output clearly fulfills user requirements")
                elif dimension == EvaluationDimension.PROMPT_EFFECTIVENESS.value:
                    strengths.append("✅ Prompt is clear, specific, and well-structured")
                elif dimension == EvaluationDimension.IMAGE_ALIGNMENT.value:
                    strengths.append("✅ Image transformation well-aligned with instructions")
                elif dimension == EvaluationDimension.CONSISTENCY.value:
                    strengths.append("✅ Output is logically consistent with no contradictions")
                elif dimension == EvaluationDimension.CONTROL_PARAMETERS.value:
                    strengths.append("✅ Parameters are well-tuned for the task")
                elif dimension == EvaluationDimension.ROBUSTNESS.value:
                    strengths.append("✅ System handles varied/complex inputs gracefully")
                elif dimension == EvaluationDimension.EFFICIENCY.value:
                    strengths.append("✅ Prompt is concise and efficient")
        
        return strengths if strengths else ["Output meets basic requirements"]
    
    def _extract_weaknesses(self, scores: Dict[str, EvaluationScore]) -> List[str]:
        """Extract low-scoring dimensions and issues as weaknesses"""
        weaknesses = []
        for dimension, score in scores.items():
            if score.score < 5:
                weaknesses.extend([f"❌ {issue}" for issue in score.issues[:2]])  # Top 2 issues
        
        return weaknesses if weaknesses else []
    
    def _extract_risks(self, scores: Dict[str, EvaluationScore], user_prompt: str) -> List[str]:
        """Extract potential failure modes and edge cases"""
        risks = []
        
        # Risk 1: Low robustness
        if scores[EvaluationDimension.ROBUSTNESS.value].score < 5:
            risks.append("⚠️ System may fail on vague or ambiguous inputs")
        
        # Risk 2: Low consistency
        if scores[EvaluationDimension.CONSISTENCY.value].score < 5:
            risks.append("⚠️ Output may contain contradictions on repeated runs")
        
        # Risk 3: Poor requirement fulfillment
        if scores[EvaluationDimension.REQUIREMENT_FULFILLMENT.value].score < 4:
            risks.append("⚠️ System may not reliably meet core user requirements")
        
        # Risk 4: Complex input risk
        if len(user_prompt.split()) > 150:
            risks.append("⚠️ Complex input may overwhelm model; consider breaking into smaller tasks")
        
        # Risk 5: Image alignment risk
        if scores[EvaluationDimension.IMAGE_ALIGNMENT.value].score < 5:
            risks.append("⚠️ Image transformations may not preserve original features")
        
        return risks if risks else []
    
    def _extract_improvements(self, scores: Dict[str, EvaluationScore]) -> List[str]:
        """Extract actionable improvement suggestions"""
        improvements = []
        
        for dimension, score in scores.items():
            improvements.extend(score.suggestions[:2])  # Top 2 suggestions per dimension
        
        return improvements[:7]  # Top 7 improvements
    
    def _generate_improved_prompt(
        self,
        user_prompt: str,
        original_prompt: str,
        output: str,
        weaknesses: List[str]
    ) -> str:
        """Generate improved version of the prompt"""
        improved = original_prompt
        
        # Add structure markers if missing
        if "step" not in improved.lower() and "section" not in improved.lower():
            improved = f"Follow these steps:\n1. {improved}"
        
        # Add clarity to ambiguous parts
        if "something" in user_prompt.lower() or "some" in user_prompt.lower():
            improved += "\n\nBe specific in your response; avoid vague language."
        
        # Add error handling if missing
        if "if" not in improved.lower() or "error" not in improved.lower():
            improved += "\n\nHandle edge cases gracefully with fallback options."
        
        # Add quality gates
        if "quality" not in improved.lower():
            improved += "\n\nEnsure output is high-quality and actionable."
        
        # Trim if too long
        if len(improved.split()) > 300:
            sentences = improved.split(".")
            improved = ". ".join(sentences[:15]) + "."  # Keep first 15 sentences
        
        return improved
    
    def _calculate_overall_rating(self, scores: Dict[str, EvaluationScore]) -> float:
        """Calculate weighted overall rating"""
        if not scores:
            return 5.0
        
        # Weight different dimensions
        weights = {
            EvaluationDimension.REQUIREMENT_FULFILLMENT.value: 0.25,
            EvaluationDimension.PROMPT_EFFECTIVENESS.value: 0.20,
            EvaluationDimension.CONSISTENCY.value: 0.20,
            EvaluationDimension.IMAGE_ALIGNMENT.value: 0.15,
            EvaluationDimension.ROBUSTNESS.value: 0.10,
            EvaluationDimension.CONTROL_PARAMETERS.value: 0.05,
            EvaluationDimension.EFFICIENCY.value: 0.05,
        }
        
        weighted_sum = 0
        weight_sum = 0
        
        for dimension, weight in weights.items():
            if dimension in scores:
                weighted_sum += scores[dimension].score * weight
                weight_sum += weight
        
        overall = weighted_sum / weight_sum if weight_sum > 0 else 5.0
        return round(overall, 1)
    
    def get_evaluation_log(self) -> List[FullEvaluation]:
        """Get all evaluations performed"""
        return self.evaluations_log.copy()
    
    def export_evaluations(self, filepath: str) -> None:
        """Export evaluation log to JSON"""
        try:
            data = [eval.to_dict() for eval in self.evaluations_log]
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Evaluations exported to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to export evaluations: {str(e)}")
    
    def format_report(self, evaluation: FullEvaluation) -> str:
        """Format evaluation as readable report"""
        report = f"""
╔════════════════════════════════════════════════════════════╗
║                    PROMPT EVALUATION REPORT                 ║
╚════════════════════════════════════════════════════════════╝

📊 OVERALL RATING: {evaluation.overall_rating}/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ STRENGTHS ({len(evaluation.strengths)}):
{chr(10).join(f'   {s}' for s in evaluation.strengths)}

❌ WEAKNESSES ({len(evaluation.weaknesses)}):
{chr(10).join(f'   {w}' for w in evaluation.weaknesses) if evaluation.weaknesses else '   None identified'}

⚠️  RISKS & EDGE CASES ({len(evaluation.risks)}):
{chr(10).join(f'   {r}' for r in evaluation.risks) if evaluation.risks else '   No major risks'}

🔧 ACTIONABLE IMPROVEMENTS ({len(evaluation.improvements)}):
{chr(10).join(f'   • {imp}' for imp in evaluation.improvements)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 DIMENSION SCORES:
"""
        for dimension, score in evaluation.scores.items():
            bar_length = int(score.score)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            report += f"\n   {dimension:30s} [{bar}] {score.score:.1f}/10"
            report += f"\n      {score.details}"
        
        report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 SUGGESTED IMPROVED PROMPT:

{evaluation.suggested_prompt}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 EVALUATION DETAILS:
   Model: {evaluation.model_used}
   Timestamp: {evaluation.timestamp}
   User Prompt Length: {len(evaluation.user_prompt.split())} words
   Generated Output Length: {len(evaluation.generated_output.split())} words
"""
        return report


# Singleton instance
_evaluator_instance: Optional[PromptEvaluator] = None


def get_evaluator() -> PromptEvaluator:
    """Get or create the evaluator singleton"""
    global _evaluator_instance
    if _evaluator_instance is None:
        _evaluator_instance = PromptEvaluator()
    return _evaluator_instance
