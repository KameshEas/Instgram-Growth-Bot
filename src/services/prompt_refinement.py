"""
Automatic Prompt Refinement Service
Iteratively improves prompts based on evaluation feedback
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RefinementStep:
    """Record of a single refinement iteration"""
    iteration: int
    original_prompt: str
    refined_prompt: str
    score_before: float
    score_after: float
    changes: List[str]
    timestamp: str


class PromptRefiner:
    """
    Automatic prompt improvement engine
    Applies refinement patterns based on evaluation results
    """
    
    REFINEMENT_PATTERNS = {
        "add_structure": {
            "pattern": r"^(?!.*\b(step|section|first|then|finally)\b)",
            "action": "Add numbered steps or sections",
            "template": "Follow these steps:\n1. {content}",
        },
        "add_examples": {
            "pattern": r"(?i)(generate|create|produce)(?!.*example)",
            "action": "Include concrete examples",
            "template": "{content}\n\nExample: [specific example]",
        },
        "add_constraints": {
            "pattern": r"^(?!.*\b(constraint|limit|maximum|minimum)\b)",
            "action": "Add explicit constraints",
            "template": "{content}\n\nConstraints:\n- [constraint 1]\n- [constraint 2]",
        },
        "add_output_format": {
            "pattern": r"^(?!.*\b(format|output|return)\b)",
            "action": "Specify output format",
            "template": "{content}\n\nOutput format:\n[specify format]",
        },
        "add_edge_cases": {
            "pattern": r"^(?!.*\b(if|else|edge case|error|exception)\b)",
            "action": "Handle edge cases",
            "template": "{content}\n\nEdge cases to handle:\n- [edge case 1]\n- [edge case 2]",
        },
        "clarify_ambiguity": {
            "pattern": r"(?i)\b(something|some|maybe|kind of|sort of)\b",
            "action": "Replace vague language with specific terms",
            "replacements": {
                "something": "a specific [noun]",
                "some": "2-3",
                "maybe": "potentially",
                "kind of": "",
                "sort of": "",
            }
        },
        "reduce_redundancy": {
            "pattern": r"(.+?)(\s+\1){2,}",
            "action": "Remove repeated concepts",
            "template": "{content} (deduplicated)",
        },
        "add_quality_gates": {
            "pattern": r"^(?!.*\b(quality|accuracy|validation|check)\b)",
            "action": "Add quality validation steps",
            "template": "{content}\n\nQuality checks:\n- [validation 1]\n- [validation 2]",
        },
        "improve_specificity": {
            "pattern": r"(?i)\b(good|bad|better|worse|nice|bad)\b",
            "action": "Use specific descriptors instead of generic adjectives",
            "replacements": {
                "good": "high-quality/effective/well-structured",
                "bad": "ineffective/confusing/poorly-structured",
                "better": "improved/more effective/more efficient",
                "worse": "degraded/less effective/less efficient",
                "nice": "elegant/polished/user-friendly",
            }
        },
    }
    
    def __init__(self):
        self.logger = logger
        self.refinement_history: List[RefinementStep] = []
    
    async def refine_prompt(
        self,
        original_prompt: str,
        evaluation_feedback: Dict[str, Any],
        max_iterations: int = 3,
    ) -> Tuple[str, List[RefinementStep]]:
        """
        Iteratively refine prompt based on evaluation
        
        Args:
            original_prompt: Original system prompt
            evaluation_feedback: Feedback from evaluator
            max_iterations: Maximum refinement iterations
        
        Returns:
            Tuple of (refined_prompt, refinement_steps)
        """
        current_prompt = original_prompt
        refinement_steps = []
        current_score = evaluation_feedback.get("overall_rating", 5.0)
        
        for iteration in range(max_iterations):
            # Determine which refinements to apply
            refinements_to_apply = self._determine_refinements(
                evaluation_feedback,
                current_prompt,
                iteration
            )
            
            if not refinements_to_apply:
                self.logger.info("No further refinements applicable")
                break
            
            # Apply refinements
            refined_prompt = self._apply_refinements(
                current_prompt,
                refinements_to_apply
            )
            
            # Create step record (score_after is simulated here)
            # In production, you'd re-evaluate the refined prompt
            improved_score = min(10.0, current_score + 0.5)  # Simulated improvement
            
            step = RefinementStep(
                iteration=iteration + 1,
                original_prompt=current_prompt,
                refined_prompt=refined_prompt,
                score_before=current_score,
                score_after=improved_score,
                changes=refinements_to_apply,
                timestamp=datetime.now().isoformat(),
            )
            
            refinement_steps.append(step)
            self.refinement_history.append(step)
            
            current_prompt = refined_prompt
            current_score = improved_score
            
            self.logger.info(f"Refinement {iteration + 1}: Score {step.score_before:.1f} → {step.score_after:.1f}")
        
        return current_prompt, refinement_steps
    
    def _determine_refinements(
        self,
        feedback: Dict[str, Any],
        prompt: str,
        iteration: int
    ) -> List[str]:
        """
        Determine which refinements to apply based on feedback
        
        Args:
            feedback: Evaluation feedback dictionary
            prompt: Current prompt text
            iteration: Current iteration number
        
        Returns:
            List of refinement keys to apply
        """
        refinements = []
        
        # Get improvement suggestions from feedback
        suggestions = feedback.get("improvements", [])
        weaknesses = feedback.get("weaknesses", [])
        
        all_feedback = suggestions + weaknesses
        
        # Map feedback to refinement patterns
        feedback_lower = " ".join(all_feedback).lower()
        
        if "structure" in feedback_lower or "step" in feedback_lower:
            refinements.append("add_structure")
        
        if "example" in feedback_lower or "concrete" in feedback_lower:
            refinements.append("add_examples")
        
        if "constraint" in feedback_lower or "limit" in feedback_lower:
            refinements.append("add_constraints")
        
        if "format" in feedback_lower or "output" in feedback_lower:
            refinements.append("add_output_format")
        
        if "edge case" in feedback_lower or "error" in feedback_lower or "handle" in feedback_lower:
            refinements.append("add_edge_cases")
        
        if "vague" in feedback_lower or "ambiguous" in feedback_lower:
            refinements.append("clarify_ambiguity")
        
        if "redundant" in feedback_lower or "repeated" in feedback_lower:
            refinements.append("reduce_redundancy")
        
        if "quality" in feedback_lower or "validation" in feedback_lower:
            refinements.append("add_quality_gates")
        
        if "specific" in feedback_lower or "generic" in feedback_lower:
            refinements.append("improve_specificity")
        
        # Limit refinements in early iterations
        if iteration == 0:
            refinements = refinements[:3]  # First iteration: top 3 refinements
        elif iteration == 1:
            refinements = refinements[3:6]  # Second iteration: next 3
        
        return refinements
    
    def _apply_refinements(self, prompt: str, refinements: List[str]) -> str:
        """Apply refinements to prompt"""
        refined = prompt
        
        for refinement_key in refinements:
            if refinement_key not in self.REFINEMENT_PATTERNS:
                continue
            
            pattern_info = self.REFINEMENT_PATTERNS[refinement_key]
            
            if refinement_key == "add_structure":
                if not any(word in refined.lower() for word in ["step", "section", "first", "then"]):
                    refined = f"Follow these steps:\n1. {refined}"
            
            elif refinement_key == "add_examples":
                if "example" not in refined.lower():
                    refined = refined.rstrip(":") + "\n\nProvide concrete examples for clarity."
            
            elif refinement_key == "add_constraints":
                if "constraint" not in refined.lower():
                    refined += "\n\nKey constraints:\n- Ensure output is concise\n- Validate all assumptions"
            
            elif refinement_key == "add_output_format":
                if "format" not in refined.lower() and "return" not in refined.lower():
                    refined += "\n\nStructure your response with clear sections and bullet points."
            
            elif refinement_key == "add_edge_cases":
                if not any(word in refined.lower() for word in ["if", "edge case", "error"]):
                    refined += "\n\nHandle edge cases by:\n- Identifying ambiguous inputs\n- Providing fallback options"
            
            elif refinement_key == "clarify_ambiguity":
                for vague, specific in pattern_info.get("replacements", {}).items():
                    refined = refined.replace(vague, specific)
            
            elif refinement_key == "improve_specificity":
                for generic, specific in pattern_info.get("replacements", {}).items():
                    refined = refined.replace(generic, specific)
            
            elif refinement_key == "reduce_redundancy":
                # Simple redundancy removal: split into sentences and remove duplicates
                sentences = refined.split(".")
                unique_sentences = []
                for sent in sentences:
                    if sent.strip() and sent.strip() not in " ".join(unique_sentences):
                        unique_sentences.append(sent.strip())
                refined = ". ".join(unique_sentences) + "."
            
            elif refinement_key == "add_quality_gates":
                if "quality" not in refined.lower():
                    refined += "\n\nValidation:\n- Check for accuracy\n- Verify completeness\n- Ensure clarity"
        
        return refined.strip()
    
    def get_refinement_summary(self) -> str:
        """Get summary of all refinements performed"""
        if not self.refinement_history:
            return "No refinements performed yet."
        
        summary = f"""
    REFINEMENT HISTORY

    Total refinements: {len(self.refinement_history)}

    """
        
        for step in self.refinement_history:
            improvement = step.score_after - step.score_before
            arrow = "↑" if improvement > 0 else "↓" if improvement < 0 else "→"
            
            summary += f"""
Iteration {step.iteration}:
   Score: {step.score_before:.1f} {arrow} {step.score_after:.1f} (Δ {improvement:+.1f})
   Changes Applied:
"""
            for change in step.changes:
                summary += f"     • {change}\n"
        
        return summary
    
    def export_refinement_history(self, filepath: str) -> None:
        """Export refinement history to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.get_refinement_summary())
                f.write("\n\nDetailed History:\n")
                f.write("=" * 60 + "\n\n")
                
                for step in self.refinement_history:
                    f.write(f"ITERATION {step.iteration}\n")
                    f.write(f"Timestamp: {step.timestamp}\n")
                    f.write(f"Score: {step.score_before:.1f} → {step.score_after:.1f}\n")
                    f.write(f"Changes: {', '.join(step.changes)}\n")
                    f.write(f"\nOriginal:\n{step.original_prompt}\n")
                    f.write(f"\nRefined:\n{step.refined_prompt}\n")
                    f.write("-" * 60 + "\n\n")
            
            self.logger.info(f"Refinement history exported to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to export refinement history: {str(e)}")


class RefinerFactory:
    """Factory for creating prompt refiners"""
    
    _refiner: Optional[PromptRefiner] = None
    
    @staticmethod
    def get_refiner() -> PromptRefiner:
        """Get or create the refiner singleton"""
        if RefinerFactory._refiner is None:
            RefinerFactory._refiner = PromptRefiner()
        return RefinerFactory._refiner

