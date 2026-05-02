"""
Edge Case Handlers for Phase 2C

Handles unusual, boundary, and exceptional input conditions.
Applies specialized handling for edge cases to prevent errors and unexpected behavior.

Author: AI Development Agent
Date: May 2, 2026
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set, Tuple
from enum import Enum
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class EdgeCaseType(Enum):
    """Type of edge case detected."""
    EMPTY_INPUT = "empty_input"
    EXTREMELY_LONG = "extremely_long"
    SPECIAL_CHARACTERS = "special_characters"
    UNICODE_CONTENT = "unicode_content"
    NUMERIC_BOUNDARY = "numeric_boundary"
    INVALID_FORMAT = "invalid_format"
    MISSING_CRITICAL = "missing_critical"
    DUPLICATE_REQUEST = "duplicate_request"
    CONTRADICTORY_REQUEST = "contradictory_request"
    VAGUE_REQUEST = "vague_request"
    TEMPORAL_ANOMALY = "temporal_anomaly"


@dataclass
class EdgeCaseAlert:
    """Alert for detected edge case."""
    case_type: EdgeCaseType
    field: str
    severity: str  # "info", "warning", "critical"
    message: str
    suggested_action: str
    detected_value: Any = None
    
    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.case_type.value}: {self.message}"


@dataclass
class EdgeCaseHandling:
    """Result of edge case handling."""
    alerts: List[EdgeCaseAlert] = field(default_factory=list)
    handled: bool = False
    corrected_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def has_alerts(self) -> bool:
        """Check if any alerts were raised."""
        return len(self.alerts) > 0
    
    def has_critical(self) -> bool:
        """Check if any critical alerts."""
        return any(a.severity == "critical" for a in self.alerts)
    
    def __str__(self) -> str:
        if not self.alerts:
            return "✅ No edge cases detected"
        
        lines = [f"Edge Cases Found: {len(self.alerts)}"]
        for alert in self.alerts:
            lines.append(f"  {alert}")
        return "\n".join(lines)


class EdgeCaseHandler:
    """Detects and handles edge cases in input data."""
    
    def __init__(self):
        """Initialize edge case handler."""
        self.vague_keywords = self._get_vague_keywords()
        self.max_prompt_length = 2000
        self.min_prompt_length = 5
    
    def _get_vague_keywords(self) -> Set[str]:
        """Keywords that indicate vague requests."""
        return {
            "something", "nice", "cool", "good", "great",
            "simple", "complex", "various", "different",
            "interesting", "unique", "professional",
            "beautiful", "pretty", "awesome"
        }
    
    async def handle_gift_design_input(self, data: Dict[str, Any]) -> EdgeCaseHandling:
        """Handle edge cases in gift design input."""
        return await self._handle_input(data, "gift_design")
    
    async def handle_content_input(self, data: Dict[str, Any]) -> EdgeCaseHandling:
        """Handle edge cases in content generator input."""
        return await self._handle_input(data, "content_generator")
    
    async def _handle_input(
        self,
        data: Dict[str, Any],
        input_type: str = "general"
    ) -> EdgeCaseHandling:
        """
        Detect and handle edge cases in input.
        
        Args:
            data: Input data to check
            input_type: Type of input (gift_design, content_generator, general)
        
        Returns:
            EdgeCaseHandling with detected alerts and corrections
        """
        alerts: List[EdgeCaseAlert] = []
        corrected_data = data.copy()
        
        # Check for empty input
        if not data:
            alerts.append(EdgeCaseAlert(
                case_type=EdgeCaseType.EMPTY_INPUT,
                field="data",
                severity="critical",
                message="Input data is empty",
                suggested_action="Provide complete input data with required fields"
            ))
            return EdgeCaseHandling(
                alerts=alerts,
                handled=False,
                corrected_data=None
            )
        
        # Check each field for edge cases
        for field, value in data.items():
            field_alerts = await self._check_field_edge_cases(field, value)
            alerts.extend(field_alerts)
        
        # Check for field-level edge cases
        alerts.extend(await self._check_cross_field_edge_cases(data))
        
        # Apply corrections
        if alerts:
            corrected_data = await self._apply_edge_case_corrections(data, alerts)
        
        return EdgeCaseHandling(
            alerts=alerts,
            handled=True,
            corrected_data=corrected_data
        )
    
    async def _check_field_edge_cases(
        self,
        field: str,
        value: Any
    ) -> List[EdgeCaseAlert]:
        """Check a single field for edge cases."""
        alerts: List[EdgeCaseAlert] = []
        
        if value is None:
            return alerts
        
        # String edge cases
        if isinstance(value, str):
            # Empty string
            if len(value) == 0:
                alerts.append(EdgeCaseAlert(
                    case_type=EdgeCaseType.EMPTY_INPUT,
                    field=field,
                    severity="warning",
                    message=f"Field '{field}' is empty string",
                    suggested_action=f"Provide non-empty value for '{field}'"
                ))
            
            # Extremely long
            elif len(value) > self.max_prompt_length:
                alerts.append(EdgeCaseAlert(
                    case_type=EdgeCaseType.EXTREMELY_LONG,
                    field=field,
                    severity="warning",
                    message=f"Field '{field}' exceeds recommended length ({len(value)} > {self.max_prompt_length})",
                    suggested_action="Condense the content or split into multiple requests",
                    detected_value=len(value)
                ))
            
            # Special characters (non-ASCII)
            if not value.isascii():
                alerts.append(EdgeCaseAlert(
                    case_type=EdgeCaseType.UNICODE_CONTENT,
                    field=field,
                    severity="info",
                    message=f"Field '{field}' contains non-ASCII characters",
                    suggested_action="Unicode will be preserved in processing"
                ))
            
            # Excessive special characters
            special_char_count = sum(1 for c in value if not c.isalnum() and c not in " -_'\"")
            if special_char_count > len(value) * 0.3:  # More than 30% special chars
                alerts.append(EdgeCaseAlert(
                    case_type=EdgeCaseType.SPECIAL_CHARACTERS,
                    field=field,
                    severity="warning",
                    message=f"Field '{field}' contains excessive special characters ({special_char_count})",
                    suggested_action="Reduce special characters for clarity"
                ))
            
            # Vague request detection
            if field in ["design_prompt", "content_prompt"]:
                vague_count = sum(1 for kw in self.vague_keywords if kw.lower() in value.lower())
                if vague_count > 2:
                    alerts.append(EdgeCaseAlert(
                        case_type=EdgeCaseType.VAGUE_REQUEST,
                        field=field,
                        severity="warning",
                        message=f"Field '{field}' contains vague language ({vague_count} vague keywords)",
                        suggested_action="Use specific, descriptive terms instead of general adjectives"
                    ))
        
        # Numeric edge cases
        elif isinstance(value, (int, float)):
            # Boundary values
            if field == "design_variations":
                if value < 1:
                    alerts.append(EdgeCaseAlert(
                        case_type=EdgeCaseType.NUMERIC_BOUNDARY,
                        field=field,
                        severity="warning",
                        message=f"Field '{field}' value {value} below minimum (1)",
                        suggested_action="Set to at least 1"
                    ))
                elif value > 5:
                    alerts.append(EdgeCaseAlert(
                        case_type=EdgeCaseType.NUMERIC_BOUNDARY,
                        field=field,
                        severity="warning",
                        message=f"Field '{field}' value {value} exceeds recommended maximum (5)",
                        suggested_action="Reduce to 5 or below for efficiency"
                    ))
        
        return alerts
    
    async def _check_cross_field_edge_cases(
        self,
        data: Dict[str, Any]
    ) -> List[EdgeCaseAlert]:
        """Check for edge cases across multiple fields."""
        alerts: List[EdgeCaseAlert] = []
        
        # Check for contradictory requests
        if "design_prompt" in data and "creative_direction" in data:
            design = data["design_prompt"].lower()
            direction = data["creative_direction"].lower()
            
            # Look for contradictions
            if ("minimalist" in design and "complex" in direction) or \
               ("simple" in design and "detailed" in direction):
                alerts.append(EdgeCaseAlert(
                    case_type=EdgeCaseType.CONTRADICTORY_REQUEST,
                    field="design_prompt/creative_direction",
                    severity="warning",
                    message="Design prompt and creative direction appear contradictory",
                    suggested_action="Ensure design requirements are consistent"
                ))
        
        # Check for too many variations with too-short deadline
        if data.get("design_variations", 1) > 3 and data.get("deadline_urgency") == "critical":
            alerts.append(EdgeCaseAlert(
                case_type=EdgeCaseType.CONTRADICTORY_REQUEST,
                field="design_variations/deadline_urgency",
                severity="warning",
                message="Many variations requested with critical deadline",
                suggested_action="Reduce variations or extend deadline"
            ))
        
        # Check for duplicate requests (check prompt similarity)
        if "design_prompt" in data and len(data["design_prompt"]) > 20:
            prompt = data["design_prompt"]
            words = prompt.split()
            unique_ratio = len(set(words)) / len(words) if words else 1.0
            
            if unique_ratio < 0.4:  # Less than 40% unique words
                alerts.append(EdgeCaseAlert(
                    case_type=EdgeCaseType.DUPLICATE_REQUEST,
                    field="design_prompt",
                    severity="info",
                    message="Prompt contains many repeated words",
                    suggested_action="Vary language or remove redundant phrases"
                ))
        
        return alerts
    
    async def _apply_edge_case_corrections(
        self,
        data: Dict[str, Any],
        alerts: List[EdgeCaseAlert]
    ) -> Dict[str, Any]:
        """Apply corrections for detected edge cases."""
        corrected = data.copy()
        
        for alert in alerts:
            if alert.case_type == EdgeCaseType.EMPTY_INPUT:
                if alert.field in data and data[alert.field] == "":
                    # Remove empty fields
                    if alert.field in corrected:
                        del corrected[alert.field]
            
            elif alert.case_type == EdgeCaseType.EXTREMELY_LONG:
                if alert.field in data and isinstance(data[alert.field], str):
                    # Truncate to max length
                    corrected[alert.field] = data[alert.field][:self.max_prompt_length]
            
            elif alert.case_type == EdgeCaseType.NUMERIC_BOUNDARY:
                if alert.field == "design_variations":
                    if data.get(alert.field, 1) < 1:
                        corrected[alert.field] = 1
                    elif data.get(alert.field, 1) > 5:
                        corrected[alert.field] = 5
        
        return corrected


class EdgeCaseHandlerFactory:
    """Factory for EdgeCaseHandler singleton."""
    
    _instance: Optional[EdgeCaseHandler] = None
    
    @classmethod
    def get_handler(cls) -> EdgeCaseHandler:
        """Get or create singleton EdgeCaseHandler instance."""
        if cls._instance is None:
            cls._instance = EdgeCaseHandler()
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        cls._instance = None
