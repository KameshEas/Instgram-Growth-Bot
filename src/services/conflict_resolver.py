"""
Conflict Resolution Framework for Phase 2C

Resolves conflicts between input parameters, design directives, and system constraints.
Applies resolution strategies based on severity and context.

Author: AI Development Agent
Date: May 2, 2026
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable, Set, Tuple
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConflictSeverity(Enum):
    """Severity of detected conflict."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResolutionStrategy(Enum):
    """Strategy for resolving conflict."""
    PRIORITIZE_FIRST = "prioritize_first"
    PRIORITIZE_SECOND = "prioritize_second"
    MERGE = "merge"
    CLARIFY = "clarify"
    USE_DEFAULT = "use_default"
    WARN_USER = "warn_user"


@dataclass
class Conflict:
    """Single detected conflict."""
    field1: str
    field2: str
    severity: ConflictSeverity
    description: str
    suggested_resolution: str
    conflicting_values: Dict[str, Any]
    resolution_strategy: Optional[ResolutionStrategy] = None
    
    def __str__(self) -> str:
        return f"[{self.severity.value.upper()}] {self.field1} ↔ {self.field2}: {self.description}"


@dataclass
class ConflictResolution:
    """Result of conflict resolution."""
    status: str  # "no_conflicts", "conflicts_resolved", "conflicts_remain"
    conflicts_detected: List[Conflict] = field(default_factory=list)
    conflicts_resolved: List[Conflict] = field(default_factory=list)
    resolved_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def has_conflicts(self) -> bool:
        """Check if unresolved conflicts remain."""
        return len(self.conflicts_detected) > 0
    
    def all_resolved(self) -> bool:
        """Check if all conflicts were resolved."""
        return self.status == "conflicts_resolved" or not self.has_conflicts()
    
    def __str__(self) -> str:
        lines = [f"Conflict Status: {self.status.upper()}"]
        if self.conflicts_detected:
            lines.append(f"\n🔴 Detected Conflicts ({len(self.conflicts_detected)}):")
            for conflict in self.conflicts_detected:
                lines.append(f"  {conflict}")
        if self.conflicts_resolved:
            lines.append(f"\n✅ Resolved Conflicts ({len(self.conflicts_resolved)}):")
            for conflict in self.conflicts_resolved:
                lines.append(f"  {conflict}")
        return "\n".join(lines)


class ConflictResolver:
    """Detects and resolves conflicts in input data and system state."""
    
    def __init__(self):
        """Initialize conflict resolver with conflict rules."""
        self.conflict_rules = self._define_conflict_rules()
        self.resolution_strategies = self._define_resolution_strategies()
    
    def _define_conflict_rules(self) -> List[Dict[str, Any]]:
        """Define rules for detecting conflicts."""
        return [
            # Product type conflicts with design direction
            {
                "name": "product_design_mismatch",
                "field1": "product_type",
                "field2": "creative_direction",
                "check": self._check_product_design_mismatch,
                "severity": ConflictSeverity.MEDIUM,
                "resolution": ResolutionStrategy.MERGE,
            },
            # Quality/budget conflicts
            {
                "name": "quality_budget_mismatch",
                "field1": "quality_preference",
                "field2": "budget_level",
                "check": self._check_quality_budget_mismatch,
                "severity": ConflictSeverity.MEDIUM,
                "resolution": ResolutionStrategy.CLARIFY,
            },
            # Deadline vs quality
            {
                "name": "deadline_quality_conflict",
                "field1": "deadline_urgency",
                "field2": "quality_preference",
                "check": self._check_deadline_quality_conflict,
                "severity": ConflictSeverity.HIGH,
                "resolution": ResolutionStrategy.WARN_USER,
            },
            # Variations vs deadline
            {
                "name": "variations_deadline_conflict",
                "field1": "design_variations",
                "field2": "deadline_urgency",
                "check": self._check_variations_deadline_conflict,
                "severity": ConflictSeverity.MEDIUM,
                "resolution": ResolutionStrategy.PRIORITIZE_FIRST,
            },
            # Target audience vs budget
            {
                "name": "audience_budget_mismatch",
                "field1": "target_audience",
                "field2": "budget_level",
                "check": self._check_audience_budget_mismatch,
                "severity": ConflictSeverity.LOW,
                "resolution": ResolutionStrategy.MERGE,
            },
        ]
    
    def _define_resolution_strategies(self) -> Dict[ResolutionStrategy, Callable]:
        """Define functions for each resolution strategy."""
        return {
            ResolutionStrategy.PRIORITIZE_FIRST: self._resolve_prioritize_first,
            ResolutionStrategy.PRIORITIZE_SECOND: self._resolve_prioritize_second,
            ResolutionStrategy.MERGE: self._resolve_merge,
            ResolutionStrategy.CLARIFY: self._resolve_clarify,
            ResolutionStrategy.USE_DEFAULT: self._resolve_use_default,
            ResolutionStrategy.WARN_USER: self._resolve_warn_user,
        }
    
    async def detect_conflicts(self, data: Dict[str, Any]) -> List[Conflict]:
        """Detect all conflicts in input data."""
        conflicts: List[Conflict] = []
        
        for rule in self.conflict_rules:
            field1 = rule["field1"]
            field2 = rule["field2"]
            
            # Skip if either field is missing
            if field1 not in data or field2 not in data:
                continue
            
            if rule["check"](data[field1], data[field2]):
                conflict = Conflict(
                    field1=field1,
                    field2=field2,
                    severity=rule["severity"],
                    description=f"Conflict between {field1} and {field2}",
                    suggested_resolution=rule.get("resolution_hint", "Review and adjust values"),
                    conflicting_values={field1: data[field1], field2: data[field2]},
                    resolution_strategy=rule.get("resolution"),
                )
                conflicts.append(conflict)
        
        return conflicts
    
    async def resolve_conflicts(self, data: Dict[str, Any]) -> ConflictResolution:
        """
        Detect and resolve all conflicts in input data.
        
        Args:
            data: Input data with potential conflicts
        
        Returns:
            ConflictResolution with detected/resolved conflicts and corrected data
        """
        detected = await self.detect_conflicts(data)
        
        if not detected:
            return ConflictResolution(
                status="no_conflicts",
                conflicts_detected=[],
                resolved_data=data.copy(),
            )
        
        resolved_data = data.copy()
        resolved_conflicts: List[Conflict] = []
        
        for conflict in detected:
            strategy = conflict.resolution_strategy or ResolutionStrategy.WARN_USER
            resolver = self.resolution_strategies.get(strategy)
            
            if resolver:
                resolved_data = resolver(resolved_data, conflict)
                conflict.resolution_strategy = strategy
                resolved_conflicts.append(conflict)
        
        return ConflictResolution(
            status="conflicts_resolved",
            conflicts_detected=detected,
            conflicts_resolved=resolved_conflicts,
            resolved_data=resolved_data,
        )
    
    # Conflict detection methods
    
    def _check_product_design_mismatch(self, product_type: str, creative_direction: str) -> bool:
        """Check if product type and creative direction are incompatible."""
        incompatible_pairs = {
            "mug": ["full_body", "panoramic", "large_landscape"],
            "poster": ["tiny", "minimal", "small_accent"],
            "t_shirt": ["intricate_detail_heavy", "photo_realistic_portrait"],
            "canvas": ["simple_flat", "minimal_line"],
        }
        
        if product_type in incompatible_pairs:
            for direction_keyword in incompatible_pairs[product_type]:
                if direction_keyword.lower() in creative_direction.lower():
                    return True
        
        return False
    
    def _check_quality_budget_mismatch(self, quality: str, budget: str) -> bool:
        """Check if quality preference conflicts with budget level."""
        conflicts = {
            ("high", "budget"): True,
            ("high", "standard"): False,
            ("balanced", "budget"): False,
            ("quick", "budget"): False,
        }
        
        key = (quality, budget)
        return conflicts.get(key, False)
    
    def _check_deadline_quality_conflict(self, deadline: str, quality: str) -> bool:
        """Check if deadline conflicts with quality expectations."""
        conflicts = {
            ("critical", "high"): True,
            ("high", "high"): False,
            ("medium", "high"): False,
            ("low", "high"): False,
        }
        
        key = (deadline, quality)
        return conflicts.get(key, False)
    
    def _check_variations_deadline_conflict(self, variations: int, deadline: str) -> bool:
        """Check if number of variations is unrealistic for deadline."""
        if deadline == "critical" and variations > 2:
            return True
        if deadline == "high" and variations > 3:
            return True
        return False
    
    def _check_audience_budget_mismatch(self, audience: str, budget: str) -> bool:
        """Check if target audience requires higher budget than allocated."""
        premium_audiences = ["luxury", "professional", "enterprise", "high-end"]
        budget_levels = ["budget", "standard", "premium"]
        
        audience_lower = audience.lower()
        is_premium_audience = any(aud in audience_lower for aud in premium_audiences)
        
        if is_premium_audience and budget in ["budget", "standard"]:
            return True
        
        return False
    
    # Resolution strategies
    
    def _resolve_prioritize_first(self, data: Dict[str, Any], conflict: Conflict) -> Dict[str, Any]:
        """Resolve by prioritizing the first field."""
        data[conflict.field2] = self._get_compatible_value(conflict.field1, data[conflict.field1])
        logger.warning(f"Resolved conflict: prioritized {conflict.field1}, adjusted {conflict.field2}")
        return data
    
    def _resolve_prioritize_second(self, data: Dict[str, Any], conflict: Conflict) -> Dict[str, Any]:
        """Resolve by prioritizing the second field."""
        data[conflict.field1] = self._get_compatible_value(conflict.field2, data[conflict.field2])
        logger.warning(f"Resolved conflict: prioritized {conflict.field2}, adjusted {conflict.field1}")
        return data
    
    def _resolve_merge(self, data: Dict[str, Any], conflict: Conflict) -> Dict[str, Any]:
        """Resolve by merging both values."""
        # Create combined value
        combined = f"{data[conflict.field1]}_with_{data[conflict.field2]}"
        data[conflict.field1] = combined
        logger.info(f"Resolved conflict: merged {conflict.field1} and {conflict.field2}")
        return data
    
    def _resolve_clarify(self, data: Dict[str, Any], conflict: Conflict) -> Dict[str, Any]:
        """Resolve by clarification (log and continue)."""
        logger.warning(f"Conflict requires clarification: {conflict.description}")
        logger.warning(f"  {conflict.field1}: {data[conflict.field1]}")
        logger.warning(f"  {conflict.field2}: {data[conflict.field2]}")
        return data
    
    def _resolve_use_default(self, data: Dict[str, Any], conflict: Conflict) -> Dict[str, Any]:
        """Resolve by using default values."""
        defaults = {
            "quality_preference": "balanced",
            "budget_level": "standard",
            "deadline_urgency": "medium",
        }
        
        if conflict.field1 in defaults:
            data[conflict.field1] = defaults[conflict.field1]
        elif conflict.field2 in defaults:
            data[conflict.field2] = defaults[conflict.field2]
        
        return data
    
    def _resolve_warn_user(self, data: Dict[str, Any], conflict: Conflict) -> Dict[str, Any]:
        """Resolve by warning user and continuing."""
        logger.warning(f"⚠️ CONFLICT WARNING: {conflict.description}")
        logger.warning(f"   This may result in suboptimal output")
        return data
    
    def _get_compatible_value(self, field: str, value: Any) -> Any:
        """Get a compatible value for field based on conflict resolution."""
        compatibility_map = {
            "deadline_urgency": {
                "critical": "quick",
                "high": "balanced",
                "medium": "balanced",
                "low": "high",
            }
        }
        
        if field in compatibility_map and value in compatibility_map[field]:
            return compatibility_map[field][value]
        
        return value


class ConflictResolverFactory:
    """Factory for ConflictResolver singleton."""
    
    _instance: Optional[ConflictResolver] = None
    
    @classmethod
    def get_resolver(cls) -> ConflictResolver:
        """Get or create singleton ConflictResolver instance."""
        if cls._instance is None:
            cls._instance = ConflictResolver()
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        cls._instance = None
