"""
Phase 1A: Deep Dimension Analysis Service
Analyzes evaluation data to identify root causes of system gaps and failure modes
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, Counter
from datetime import datetime

logger = logging.getLogger(__name__)


class DimensionType(Enum):
    """All 7 evaluation dimensions"""
    REQUIREMENT_FULFILLMENT = "requirement_fulfillment"
    PROMPT_EFFECTIVENESS = "prompt_effectiveness"
    IMAGE_ALIGNMENT = "image_alignment"
    CONSISTENCY = "consistency"
    CONTROL_PARAMETERS = "control_parameters"
    ROBUSTNESS = "robustness"
    EFFICIENCY = "efficiency"


@dataclass
class FailureMode:
    """Represents a specific failure pattern"""
    dimension: str
    pattern: str  # e.g., "long_prompt", "missing_constraint"
    frequency: int  # How often this occurs
    severity: float  # 1-10 scale
    examples: List[str]  # Example cases showing this failure
    root_cause: str  # Underlying cause
    impact: str  # How it affects users


@dataclass
class DimensionAnalysis:
    """Analysis results for a single dimension"""
    dimension: str
    average_score: float
    score_distribution: Dict[str, int]  # Score -> count
    failure_modes: List[FailureMode]
    top_issues: List[str]
    recommendations: List[str]
    critical_gaps: List[str]


class DimensionAnalyzer:
    """
    Analyzes evaluation dimensions to identify:
    1. Root causes of low scores
    2. Failure mode patterns
    3. Dimension-specific improvement opportunities
    """
    
    def __init__(self):
        self.logger = logger
        self.evaluations: List[Dict[str, Any]] = []
    
    def load_evaluations(self, filepath: str) -> None:
        """Load evaluation records from JSONL file"""
        self.evaluations = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        self.evaluations.append(json.loads(line))
            self.logger.info(f"Loaded {len(self.evaluations)} evaluations")
        except FileNotFoundError:
            self.logger.warning(f"Evaluations file not found: {filepath}")
    
    def add_evaluation(self, evaluation: Dict[str, Any]) -> None:
        """Add single evaluation record"""
        self.evaluations.append(evaluation)
    
    def analyze_dimension(self, dimension: str) -> DimensionAnalysis:
        """
        Deep analysis of a single dimension
        
        Args:
            dimension: Dimension name (e.g., "requirement_fulfillment")
        
        Returns:
            DimensionAnalysis with detailed findings
        """
        if not self.evaluations:
            self.logger.warning("No evaluations to analyze")
            return DimensionAnalysis(
                dimension=dimension,
                average_score=0.0,
                score_distribution={},
                failure_modes=[],
                top_issues=[],
                recommendations=[],
                critical_gaps=[]
            )
        
        # Extract scores for this dimension
        scores = []
        issues_by_score = defaultdict(list)
        
        for eval_record in self.evaluations:
            if "scores" in eval_record and dimension in eval_record["scores"]:
                score_data = eval_record["scores"][dimension]
                score = score_data.get("score", 0)
                scores.append(score)
                
                # Track issues by score
                if "issues" in score_data:
                    for issue in score_data["issues"]:
                        issues_by_score[score].append(issue)
        
        if not scores:
            return DimensionAnalysis(
                dimension=dimension,
                average_score=0.0,
                score_distribution={},
                failure_modes=[],
                top_issues=[],
                recommendations=[],
                critical_gaps=[]
            )
        
        # Calculate statistics
        average_score = sum(scores) / len(scores)
        score_distribution = self._get_score_distribution(scores)
        failure_modes = self._identify_failure_modes(dimension, issues_by_score)
        top_issues = self._get_top_issues(issues_by_score)
        recommendations = self._get_recommendations(dimension, failure_modes)
        critical_gaps = self._identify_critical_gaps(dimension, average_score, failure_modes)
        
        return DimensionAnalysis(
            dimension=dimension,
            average_score=average_score,
            score_distribution=score_distribution,
            failure_modes=failure_modes,
            top_issues=top_issues,
            recommendations=recommendations,
            critical_gaps=critical_gaps
        )
    
    def analyze_all_dimensions(self) -> Dict[str, DimensionAnalysis]:
        """Analyze all 7 dimensions"""
        results = {}
        for dim_type in DimensionType:
            results[dim_type.value] = self.analyze_dimension(dim_type.value)
        return results
    
    def _get_score_distribution(self, scores: List[float]) -> Dict[str, int]:
        """Get distribution of scores"""
        distribution = defaultdict(int)
        for score in scores:
            bucket = f"{int(score)}-{int(score)+1}"
            distribution[bucket] += 1
        return dict(distribution)
    
    def _identify_failure_modes(
        self, 
        dimension: str, 
        issues_by_score: Dict[float, List[str]]
    ) -> List[FailureMode]:
        """Identify recurring failure patterns"""
        issue_counter = Counter()
        for issues in issues_by_score.values():
            issue_counter.update(issues)
        
        failure_modes = []
        for pattern, frequency in issue_counter.most_common(10):
            # Calculate severity based on frequency and low scores
            low_score_occurrences = sum(
                1 for score, issues in issues_by_score.items()
                if score < 6 and pattern in issues
            )
            severity = min(10, (low_score_occurrences / max(frequency, 1)) * 10)
            
            failure_modes.append(FailureMode(
                dimension=dimension,
                pattern=pattern,
                frequency=frequency,
                severity=severity,
                examples=[],  # Would need more data to populate
                root_cause=self._infer_root_cause(dimension, pattern),
                impact=self._assess_impact(dimension, pattern)
            ))
        
        return failure_modes
    
    def _get_top_issues(self, issues_by_score: Dict[float, List[str]]) -> List[str]:
        """Get top recurring issues"""
        all_issues = []
        for issues in issues_by_score.values():
            all_issues.extend(issues)
        
        issue_counter = Counter(all_issues)
        return [issue for issue, _ in issue_counter.most_common(10)]
    
    def _infer_root_cause(self, dimension: str, pattern: str) -> str:
        """Infer root cause of a failure pattern"""
        root_causes = {
            "requirement_fulfillment": {
                "missing_requirement": "Requirements not explicitly captured or validated",
                "vague_input": "User input unclear, needs clarification",
                "conflicting_preferences": "Multiple contradictory user preferences"
            },
            "prompt_effectiveness": {
                "unclear_directive": "Prompt guidance not specific enough",
                "long_prompt": "Prompt length causes token loss or ambiguity",
                "redundant_constraint": "Repeated guidance confuses model"
            },
            "image_alignment": {
                "high_denoising": "Denoising strength too high, loses original",
                "low_denoising": "Denoising strength too low, no transformation",
                "missing_alignment_check": "No validation of output against input"
            },
            "consistency": {
                "style_mismatch": "Style descriptions inconsistent across sections",
                "color_mismatch": "Color palette contradicts tone/aesthetic",
                "font_unavailable": "Recommended font not verified as available"
            },
            "control_parameters": {
                "default_parameters": "Using fixed parameters regardless of context",
                "no_parameter_guidance": "Missing CFG/denoising recommendations",
                "untuned_defaults": "Parameters not optimized for product type"
            },
            "robustness": {
                "vague_input_failure": "System fails on unclear user concepts",
                "edge_case_unhandled": "Specific input type not anticipated",
                "no_error_recovery": "No graceful fallback for edge cases"
            },
            "efficiency": {
                "overlong_prompt": "Prompt contains unnecessary verbosity",
                "repeated_concepts": "Same constraint stated multiple ways",
                "inefficient_structure": "Prompt structure could be more concise"
            }
        }
        
        if dimension in root_causes and pattern in root_causes[dimension]:
            return root_causes[dimension][pattern]
        return f"Unknown root cause for {pattern}"
    
    def _assess_impact(self, dimension: str, pattern: str) -> str:
        """Assess impact of a failure pattern"""
        impacts = {
            "requirement_fulfillment": {
                "missing_requirement": "User gets output that doesn't meet their needs",
                "vague_input": "Generic output, wastes user time with clarifications"
            },
            "prompt_effectiveness": {
                "unclear_directive": "Model produces lower quality output",
                "long_prompt": "Increased token usage and cost"
            },
            "image_alignment": {
                "high_denoising": "Generated images don't preserve reference features",
                "low_denoising": "No visible transformation applied"
            },
            "consistency": {
                "style_mismatch": "Design brief contradicts itself, confuses user",
                "color_mismatch": "Final design feels disharmonious"
            },
            "control_parameters": {
                "default_parameters": "Suboptimal quality for specific product type",
                "no_parameter_guidance": "User can't optimize results"
            },
            "robustness": {
                "vague_input_failure": "System unusable for real-world inputs",
                "edge_case_unhandled": "Unexpected failures damage user trust"
            },
            "efficiency": {
                "overlong_prompt": "Slower processing, higher costs",
                "repeated_concepts": "Wastes tokens and model attention"
            }
        }
        
        if dimension in impacts and pattern in impacts[dimension]:
            return impacts[dimension][pattern]
        return "Moderate impact on user experience"
    
    def _get_recommendations(
        self, 
        dimension: str, 
        failure_modes: List[FailureMode]
    ) -> List[str]:
        """Generate specific improvement recommendations"""
        recommendations = []
        
        for mode in failure_modes[:5]:  # Top 5 failure modes
            if mode.dimension == "requirement_fulfillment":
                recommendations.append(
                    f"Add explicit requirement validation step before output "
                    f"({mode.pattern})"
                )
            elif mode.dimension == "prompt_effectiveness":
                recommendations.append(
                    f"Implement prompt optimization pipeline to reduce verbosity "
                    f"and clarify directives ({mode.pattern})"
                )
            elif mode.dimension == "image_alignment":
                recommendations.append(
                    f"Create denoising strength matrix per product type "
                    f"({mode.pattern})"
                )
            elif mode.dimension == "consistency":
                recommendations.append(
                    f"Add cross-section coherence validator ({mode.pattern})"
                )
            elif mode.dimension == "control_parameters":
                recommendations.append(
                    f"Build parameter recommendation engine for dynamic selection "
                    f"({mode.pattern})"
                )
            elif mode.dimension == "robustness":
                recommendations.append(
                    f"Implement input validation with helpful error messages "
                    f"({mode.pattern})"
                )
            elif mode.dimension == "efficiency":
                recommendations.append(
                    f"Consolidate prompts - remove redundancy and shorten "
                    f"({mode.pattern})"
                )
        
        return recommendations
    
    def _identify_critical_gaps(
        self,
        dimension: str,
        average_score: float,
        failure_modes: List[FailureMode]
    ) -> List[str]:
        """Identify critical gaps that block reaching 10/10"""
        gaps = []
        
        # Gap identification logic
        if average_score < 5:
            gaps.append(f"Critical: {dimension} is below 5.0 - fundamental approach needed")
        elif average_score < 7:
            gaps.append(f"Major: {dimension} is below 7.0 - significant work required")
        
        # Check for top failure modes
        for mode in failure_modes[:3]:
            if mode.severity > 7:
                gaps.append(f"High-severity failure mode: {mode.pattern} ({mode.severity:.1f}/10)")
        
        return gaps
    
    def generate_report(self, analyses: Dict[str, DimensionAnalysis]) -> str:
        """Generate human-readable analysis report"""
        report = []
        report.append("=" * 80)
        report.append("PHASE 1A: DEEP DIMENSION ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Analysis Date: {datetime.now().isoformat()}")
        report.append(f"Total Evaluations Analyzed: {len(self.evaluations)}")
        report.append("")
        
        # Summary by dimension
        report.append("DIMENSION SUMMARY")
        report.append("-" * 80)
        for dim, analysis in analyses.items():
            report.append(f"\n{dim.upper()}")
            report.append(f"  Average Score: {analysis.average_score:.2f}/10")
            report.append(f"  Distribution: {analysis.score_distribution}")
            
            if analysis.top_issues:
                report.append(f"  Top Issues:")
                for i, issue in enumerate(analysis.top_issues[:5], 1):
                    report.append(f"    {i}. {issue}")
            
            if analysis.critical_gaps:
                report.append(f"  Critical Gaps:")
                for gap in analysis.critical_gaps:
                    report.append(f"    • {gap}")
            
            if analysis.recommendations:
                report.append(f"  Recommendations:")
                for rec in analysis.recommendations[:3]:
                    report.append(f"    • {rec}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def export_analysis(self, filepath: str, analyses: Dict[str, DimensionAnalysis]) -> None:
        """Export analysis to JSON for processing"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluations": len(self.evaluations),
            "dimensions": {
                dim: {
                    "average_score": analysis.average_score,
                    "score_distribution": analysis.score_distribution,
                    "failure_modes": [
                        {
                            "pattern": fm.pattern,
                            "frequency": fm.frequency,
                            "severity": fm.severity,
                            "root_cause": fm.root_cause,
                            "impact": fm.impact
                        }
                        for fm in analysis.failure_modes
                    ],
                    "top_issues": analysis.top_issues[:10],
                    "recommendations": analysis.recommendations,
                    "critical_gaps": analysis.critical_gaps
                }
                for dim, analysis in analyses.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Analysis exported to {filepath}")


def get_analyzer() -> DimensionAnalyzer:
    """Factory function for dimension analyzer"""
    return DimensionAnalyzer()
