"""
Agent Evaluation Integration
Hooks evaluation system into existing agents for automatic quality monitoring
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from src.services.prompt_evaluator import get_evaluator, FullEvaluation
from src.services.prompt_refinement import RefinerFactory

logger = logging.getLogger(__name__)


class AgentEvaluationHook:
    """
    Wrapper that integrates evaluation into agent execution pipeline
    Provides automatic quality monitoring and improvement suggestions
    """
    
    def __init__(self, agent_name: str, metrics_dir: str = "metrics"):
        self.agent_name = agent_name
        self.evaluator = get_evaluator()
        self.refiner = RefinerFactory.get_refiner()
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(exist_ok=True)
        self.evaluation_log: List[Dict[str, Any]] = []
    
    async def evaluate_execution(
        self,
        user_request: Dict[str, Any],
        agent_output: Dict[str, Any],
        model_used: str = "Groq",
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate agent execution and return results with recommendations
        
        Args:
            user_request: Original user request
            agent_output: Agent's output
            model_used: Model name
            system_prompt: System prompt used by agent
        
        Returns:
            Evaluation result with metrics and recommendations
        """
        try:
            # Extract text for evaluation
            user_prompt = self._extract_user_prompt(user_request)
            generated_output = self._extract_output_text(agent_output)
            
            # Run evaluation
            evaluation = await self.evaluator.evaluate(
                user_prompt=user_prompt,
                system_prompt=system_prompt or "Default agent system prompt",
                generated_output=generated_output,
                model_used=model_used,
            )
            
            # Create evaluation record
            record = {
                "timestamp": datetime.now().isoformat(),
                "agent": self.agent_name,
                "user_request": user_request,
                "agent_output": agent_output,
                "evaluation": evaluation.to_dict(),
                "recommendations": self._generate_recommendations(evaluation),
            }
            
            # Log evaluation
            self.evaluation_log.append(record)
            self._save_evaluation(record)
            
            logger.info(f"[{self.agent_name}] Evaluation complete: {evaluation.overall_rating}/10")
            
            return record
        
        except Exception as e:
            logger.error(f"Evaluation failed for {self.agent_name}: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": self.agent_name,
            }
    
    def _extract_user_prompt(self, user_request: Dict[str, Any]) -> str:
        """Extract user prompt from request"""
        if isinstance(user_request, str):
            return user_request
        
        # Try common keys
        for key in ["prompt", "message", "input", "concept_idea", "request", "query"]:
            if key in user_request:
                return str(user_request[key])
        
        # Fallback: concatenate all values
        return " ".join(str(v) for v in user_request.values() if v)
    
    def _extract_output_text(self, agent_output: Dict[str, Any]) -> str:
        """Extract text from agent output"""
        if isinstance(agent_output, str):
            return agent_output
        
        if not isinstance(agent_output, dict):
            return str(agent_output)
        
        # Try common output keys
        if "generated_output" in agent_output:
            return str(agent_output["generated_output"])
        
        if "output" in agent_output:
            return str(agent_output["output"])
        
        if "text" in agent_output:
            return str(agent_output["text"])
        
        # For gift design output, extract briefs
        if "concepts" in agent_output:
            briefs = []
            for concept in agent_output["concepts"]:
                if isinstance(concept, dict):
                    if "design_brief" in concept:
                        briefs.append(json.dumps(concept["design_brief"], indent=2))
            if briefs:
                return "\n".join(briefs)
        
        # Fallback: stringify
        return json.dumps(agent_output, indent=2)[:1000]  # First 1000 chars
    
    def _generate_recommendations(self, evaluation: FullEvaluation) -> Dict[str, Any]:
        """Generate actionable recommendations from evaluation"""
        return {
            "overall_rating": evaluation.overall_rating,
            "quality_level": self._get_quality_level(evaluation.overall_rating),
            "strengths": evaluation.strengths,
            "weaknesses": evaluation.weaknesses,
            "critical_issues": evaluation.weaknesses[:2] if evaluation.weaknesses else [],
            "action_items": evaluation.improvements[:5],
            "priority_focus": self._determine_priority_focus(evaluation),
            "suggested_improvements": evaluation.suggested_prompt[:200] if evaluation.suggested_prompt else "",
        }
    
    def _get_quality_level(self, rating: float) -> str:
        """Determine quality level from rating"""
        if rating >= 8.5:
            return "EXCELLENT"
        elif rating >= 7.0:
            return "GOOD"
        elif rating >= 5.0:
            return "ACCEPTABLE"
        elif rating >= 3.0:
            return "POOR"
        else:
            return "CRITICAL"
    
    def _determine_priority_focus(self, evaluation: FullEvaluation) -> str:
        """Determine what dimension needs focus"""
        lowest_score_dim = min(
            evaluation.scores.items(),
            key=lambda x: x[1].score
        )
        return f"Focus on: {lowest_score_dim[0]} (Score: {lowest_score_dim[1].score:.1f}/10)"
    
    def _save_evaluation(self, record: Dict[str, Any]) -> None:
        """Save evaluation record to file"""
        try:
            # Create agent-specific log file
            log_file = self.metrics_dir / f"{self.agent_name}_evaluations.jsonl"
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(record, default=str) + "\n")
            
            # Also save summary stats
            self._update_summary_stats()
        
        except Exception as e:
            logger.error(f"Failed to save evaluation: {str(e)}")
    
    def _update_summary_stats(self) -> None:
        """Update summary statistics file"""
        try:
            stats_file = self.metrics_dir / f"{self.agent_name}_stats.json"
            
            # Calculate averages
            if not self.evaluation_log:
                return
            
            ratings = [e["evaluation"]["overall_rating"] for e in self.evaluation_log]
            
            stats = {
                "agent": self.agent_name,
                "total_evaluations": len(self.evaluation_log),
                "average_rating": sum(ratings) / len(ratings),
                "highest_rating": max(ratings),
                "lowest_rating": min(ratings),
                "last_updated": datetime.now().isoformat(),
            }
            
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        
        except Exception as e:
            logger.error(f"Failed to update stats: {str(e)}")
    
    async def get_improvement_suggestions(self, max_iterations: int = 2) -> Dict[str, Any]:
        """
        Get improvement suggestions by analyzing recent evaluations
        
        Args:
            max_iterations: Maximum refinement iterations
        
        Returns:
            Improvement recommendations
        """
        if not self.evaluation_log:
            return {"status": "no_data", "message": "No evaluations to analyze"}
        
        # Analyze recent evaluations
        recent_evals = self.evaluation_log[-5:]  # Last 5 evaluations
        
        # Calculate average scores
        avg_scores = {}
        for eval_log in recent_evals:
            eval_data = eval_log["evaluation"]
            for dim, score in eval_data["scores"].items():
                if dim not in avg_scores:
                    avg_scores[dim] = []
                avg_scores[dim].append(score["score"])
        
        avg_scores = {dim: sum(scores)/len(scores) for dim, scores in avg_scores.items()}
        
        # Identify weakest dimensions
        weakest_dims = sorted(avg_scores.items(), key=lambda x: x[1])[:3]
        
        return {
            "agent": self.agent_name,
            "evaluated_runs": len(recent_evals),
            "dimension_averages": avg_scores,
            "priority_improvements": [f"{dim}: {score:.1f}/10" for dim, score in weakest_dims],
            "suggested_next_steps": [
                "Implement parameter optimization",
                "Add edge case handling",
                "Improve prompt clarity",
            ],
        }
    
    def get_evaluation_history(self) -> List[Dict[str, Any]]:
        """Get evaluation history"""
        return self.evaluation_log.copy()
    
    def generate_report(self) -> str:
        """Generate comprehensive evaluation report"""
        if not self.evaluation_log:
            return f"No evaluations for {self.agent_name}"
        
        recent = self.evaluation_log[-10:]  # Last 10 evaluations
        ratings = [e["evaluation"]["overall_rating"] for e in recent]
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║        AGENT EVALUATION REPORT - {self.agent_name:30s}    ║
╚════════════════════════════════════════════════════════════╝

📊 EVALUATION SUMMARY (Last 10 runs):
   • Total Evaluations: {len(self.evaluation_log)}
   • Average Rating: {sum(ratings)/len(ratings):.1f}/10
   • Highest Rating: {max(ratings):.1f}/10
   • Lowest Rating: {min(ratings):.1f}/10
   • Trend: {"↑ Improving" if ratings[-1] > ratings[0] else "↓ Declining" if ratings[-1] < ratings[0] else "→ Stable"}

📈 RECENT RATINGS:
"""
        for i, rating in enumerate(ratings, 1):
            bar = "█" * int(rating) + "░" * (10 - int(rating))
            report += f"   Run {i:2d}: [{bar}] {rating:.1f}/10\n"
        
        # Get latest detailed evaluation
        if recent:
            latest_eval = recent[-1]["evaluation"]
            report += f"""

🎯 LATEST DETAILED EVALUATION:
   Model: {latest_eval['model_used']}
   
   Dimension Scores:
"""
            for dim, score in latest_eval["scores"].items():
                bar = "█" * int(score["score"]) + "░" * (10 - int(score["score"]))
                report += f"      {dim:35s} [{bar}] {score['score']:.1f}/10\n"
            
            if latest_eval["strengths"]:
                report += f"\n   Strengths:\n"
                for strength in latest_eval["strengths"][:3]:
                    report += f"      {strength}\n"
            
            if latest_eval["improvements"]:
                report += f"\n   Action Items:\n"
                for imp in latest_eval["improvements"][:3]:
                    report += f"      • {imp}\n"
        
        return report


class GiftDesignEvaluationHook(AgentEvaluationHook):
    """Specialized evaluation hook for Gift Design Agent"""
    
    def __init__(self):
        super().__init__("GiftDesignAgent")
    
    async def evaluate_gift_design_output(
        self,
        user_request: Dict[str, Any],
        concepts: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Evaluate gift design output"""
        # Extract design briefs for evaluation
        briefs_text = self._extract_design_briefs(concepts)
        
        system_prompt = """You are an expert gift design evaluator.
Assess the design concepts for:
1. Requirement fulfillment
2. Creative variation
3. Feasibility
4. Brand alignment"""
        
        return await self.evaluate_execution(
            user_request=user_request,
            agent_output={"concepts": concepts},
            system_prompt=system_prompt,
        )
    
    def _extract_design_briefs(self, concepts: List[Dict[str, Any]]) -> str:
        """Extract design briefs from concepts"""
        briefs = []
        for concept in concepts:
            if "design_brief" in concept:
                brief_data = concept["design_brief"]
                summary = f"Concept: {concept.get('title', 'Untitled')}\n"
                summary += f"  Visual Style: {brief_data.get('visual_style', 'N/A')}\n"
                summary += f"  Colors: {brief_data.get('color_palette', [])}\n"
                briefs.append(summary)
        return "\n".join(briefs)


class ContentGeneratorEvaluationHook(AgentEvaluationHook):
    """Specialized evaluation hook for Content Generator Agent"""
    
    def __init__(self):
        super().__init__("ContentGeneratorAgent")
    
    async def evaluate_prompt_generation(
        self,
        user_request: Dict[str, Any],
        generated_prompts: List[str],
    ) -> Dict[str, Any]:
        """Evaluate generated content prompts"""
        prompts_text = "\n---\n".join(generated_prompts[:5])  # First 5 prompts
        
        system_prompt = """You are a prompt quality evaluator.
Assess the generated image prompts for:
1. Specificity and detail
2. Virality potential
3. Technical implementability
4. Diversity from each other"""
        
        return await self.evaluate_execution(
            user_request=user_request,
            agent_output={"prompts": generated_prompts, "count": len(generated_prompts)},
            system_prompt=system_prompt,
        )


# Factory for creating evaluation hooks
class EvaluationHookFactory:
    """Factory for creating agent-specific evaluation hooks"""
    
    _hooks = {}
    
    @staticmethod
    def get_hook(agent_name: str) -> AgentEvaluationHook:
        """Get or create evaluation hook for agent"""
        if agent_name not in EvaluationHookFactory._hooks:
            if agent_name == "GiftDesignAgent":
                EvaluationHookFactory._hooks[agent_name] = GiftDesignEvaluationHook()
            elif agent_name == "ContentGeneratorAgent":
                EvaluationHookFactory._hooks[agent_name] = ContentGeneratorEvaluationHook()
            else:
                EvaluationHookFactory._hooks[agent_name] = AgentEvaluationHook(agent_name)
        
        return EvaluationHookFactory._hooks[agent_name]
    
    @staticmethod
    def get_all_hooks() -> Dict[str, AgentEvaluationHook]:
        """Get all registered evaluation hooks"""
        return EvaluationHookFactory._hooks.copy()


async def evaluate_all_agents() -> Dict[str, Any]:
    """
    Generate comprehensive evaluation report for all agents
    Useful for scheduled evaluation runs
    """
    hooks = EvaluationHookFactory.get_all_hooks()
    
    report = "╔═══════════════════════════════════════════════════════════╗\n"
    report += "║          COMPREHENSIVE AGENT EVALUATION REPORT             ║\n"
    report += "╚═══════════════════════════════════════════════════════════╝\n\n"
    
    all_data = {}
    
    for agent_name, hook in hooks.items():
        report += hook.generate_report()
        report += "\n" + "=" * 60 + "\n\n"
        
        suggestions = await hook.get_improvement_suggestions()
        all_data[agent_name] = suggestions
    
    return {
        "report": report,
        "data": all_data,
        "timestamp": datetime.now().isoformat(),
    }
