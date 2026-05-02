"""
Input Validation System for Phase 2C

Validates all inputs to design and content agents before processing.
Ensures type correctness, constraint satisfaction, and consistency.

Author: AI Development Agent
Date: May 2, 2026
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set, Tuple
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Validation result status."""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class ValidationSeverity(Enum):
    """Severity level of validation issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Single validation issue found."""
    field: str
    severity: ValidationSeverity
    message: str
    suggested_fix: Optional[str] = None
    
    def __str__(self) -> str:
        return f"[{self.severity.value.upper()}] {self.field}: {self.message}"


@dataclass
class ValidationResult:
    """Complete validation result."""
    status: ValidationStatus
    issues: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    corrected_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def is_valid(self) -> bool:
        """Check if validation passed (no critical/error issues)."""
        return self.status == ValidationStatus.PASS
    
    def has_issues(self) -> bool:
        """Check if there are any issues."""
        return len(self.issues) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def __str__(self) -> str:
        lines = [f"Validation Status: {self.status.value.upper()}"]
        if self.has_issues():
            lines.append(f"\n🔴 Issues ({len(self.issues)}):")
            for issue in self.issues:
                lines.append(f"  {issue}")
        if self.has_warnings():
            lines.append(f"\n🟡 Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  {warning}")
        return "\n".join(lines)


class InputValidator:
    """Validates inputs to design and content agents."""
    
    def __init__(self):
        """Initialize validator with constraint definitions."""
        self.constraints = self._define_constraints()
        self.required_fields = self._define_required_fields()
    
    def _define_constraints(self) -> Dict[str, Dict[str, Any]]:
        """Define constraints for each field type."""
        return {
            "action": {
                "type": str,
                "required": False,
                "max_length": 50,
            },
            "design_prompt": {
                "min_length": 10,
                "max_length": 2000,
                "type": str,
                "required": True,
            },
            "content_prompt": {
                "min_length": 5,
                "max_length": 2000,
                "type": str,
                "required": True,
            },
            "product_type": {
                "allowed_values": ["t_shirt", "mug", "canvas", "poster", "merchandise"],
                "type": str,
                "required": True,
            },
            "quality_preference": {
                "allowed_values": ["quick", "balanced", "high"],
                "type": str,
                "required": False,
                "default": "balanced",
            },
            "design_variations": {
                "min_value": 1,
                "max_value": 5,
                "type": int,
                "required": False,
                "default": 3,
            },
            "creative_direction": {
                "min_length": 5,
                "max_length": 500,
                "type": str,
                "required": False,
            },
            "color_preference": {
                "type": str,
                "required": False,
                "max_length": 200,
            },
            "target_audience": {
                "min_length": 3,
                "max_length": 500,
                "type": str,
                "required": False,
            },
            "budget_level": {
                "allowed_values": ["budget", "standard", "premium"],
                "type": str,
                "required": False,
                "default": "standard",
            },
            "deadline_urgency": {
                "allowed_values": ["low", "medium", "high", "critical"],
                "type": str,
                "required": False,
                "default": "medium",
            },
            "image_count": {
                "min_value": 1,
                "max_value": 10,
                "type": int,
                "required": False,
                "default": 1,
            },
        }
    
    def _define_required_fields(self) -> Dict[str, List[str]]:
        """Define required fields for each agent type."""
        return {
            "gift_design": ["design_prompt", "product_type"],
            "gift_design_list_products": [],  # No required fields for list operations
            "gift_design_list_tones": [],
            "gift_design_get_product_specs": ["product_type"],
            "gift_design_list_roles": [],
            "gift_design_get_role_info": [],
            "content_generator": ["content_prompt"],
            "content_generator_list_categories": [],
            "content_generator_search": [],
            "general": [],
        }
    
    async def validate_design_input(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate input for gift design agent."""
        # Determine the specific action to tailor requirements
        action = data.get("action", "generate_concepts")
        
        # Map known actions to agent types
        action_map = {
            "generate_concepts": "gift_design",
            "list_products": "gift_design_list_products",
            "list_tones": "gift_design_list_tones",
            "get_product_specs": "gift_design_get_product_specs",
            "list_roles": "gift_design_list_roles",
            "get_role_info": "gift_design_get_role_info",
        }
        
        # If action is not recognized, use general validation (no specific required fields)
        # This allows the agent to handle the unknown action error itself
        agent_type = action_map.get(action, "general")
        
        return await self.validate_input(data, agent_type)
    
    async def validate_content_input(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate input for content generator agent."""
        # Determine the specific action to tailor requirements
        action = data.get("action", "generate")
        
        # Map known actions to agent types
        action_map = {
            "generate": "content_generator",
            "list_categories": "content_generator_list_categories",
            "search": "content_generator_search",
        }
        
        # If action is not recognized, use general validation (no specific required fields)
        # This allows the agent to handle the unknown action error itself
        agent_type = action_map.get(action, "general")
        
        return await self.validate_input(data, agent_type)
    
    async def validate_input(
        self,
        data: Dict[str, Any],
        agent_type: str = "general",
    ) -> ValidationResult:
        """
        Validate input data against constraints.
        
        Args:
            data: Input data to validate
            agent_type: Type of agent (gift_design, content_generator, general)
        
        Returns:
            ValidationResult with status and issues
        """
        if not isinstance(data, dict):
            return ValidationResult(
                status=ValidationStatus.FAIL,
                issues=[ValidationIssue(
                    field="data",
                    severity=ValidationSeverity.CRITICAL,
                    message="Input must be a dictionary",
                    suggested_fix="Convert input to dict or use proper data structure"
                )]
            )
        
        issues: List[ValidationIssue] = []
        warnings: List[ValidationIssue] = []
        corrected_data = data.copy()
        
        # Check required fields
        required = self.required_fields.get(agent_type, [])
        for field in required:
            if field not in data or data[field] is None:
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Required field '{field}' is missing",
                    suggested_fix=f"Provide a non-empty value for '{field}'"
                ))
        
        # Check each field
        for field, value in data.items():
            if field not in self.constraints:
                # Unknown fields are warnings, not errors
                warnings.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown field '{field}'",
                    suggested_fix="Remove or use a recognized field name"
                ))
                continue
            
            constraint = self.constraints[field]
            field_issues = self._validate_field(field, value, constraint)
            issues.extend([i for i in field_issues if i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)])
            warnings.extend([i for i in field_issues if i.severity == ValidationSeverity.WARNING])
        
        # Add defaults for missing optional fields
        for field, constraint in self.constraints.items():
            if not constraint.get("required", False) and field not in data:
                if "default" in constraint:
                    corrected_data[field] = constraint["default"]
        
        # Determine overall status
        if issues and any(i.severity == ValidationSeverity.CRITICAL for i in issues):
            status = ValidationStatus.FAIL
        elif issues:
            status = ValidationStatus.FAIL
        elif warnings:
            status = ValidationStatus.WARN
        else:
            status = ValidationStatus.PASS
        
        return ValidationResult(
            status=status,
            issues=issues,
            warnings=warnings,
            corrected_data=corrected_data if status != ValidationStatus.FAIL else None,
        )
    
    def _validate_field(self, field: str, value: Any, constraint: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate a single field against its constraint."""
        issues: List[ValidationIssue] = []
        
        # Skip if None and optional
        if value is None:
            if constraint.get("required", False):
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Required field '{field}' cannot be None"
                ))
            return issues
        
        # Type validation
        expected_type = constraint.get("type")
        if expected_type and not isinstance(value, expected_type):
            issues.append(ValidationIssue(
                field=field,
                severity=ValidationSeverity.ERROR,
                message=f"Field '{field}' must be {expected_type.__name__}, got {type(value).__name__}",
                suggested_fix=f"Convert value to {expected_type.__name__}"
            ))
            return issues  # Stop further validation if type is wrong
        
        # String constraints
        if isinstance(value, str):
            if "min_length" in constraint and len(value) < constraint["min_length"]:
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Field '{field}' too short (min {constraint['min_length']} chars)",
                    suggested_fix=f"Provide at least {constraint['min_length']} characters"
                ))
            if "max_length" in constraint and len(value) > constraint["max_length"]:
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.WARNING,
                    message=f"Field '{field}' too long (max {constraint['max_length']} chars)",
                    suggested_fix=f"Reduce to {constraint['max_length']} characters or less"
                ))
            if "allowed_values" in constraint and value not in constraint["allowed_values"]:
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Field '{field}' value '{value}' not in allowed values",
                    suggested_fix=f"Use one of: {', '.join(constraint['allowed_values'])}"
                ))
        
        # Numeric constraints
        if isinstance(value, (int, float)):
            if "min_value" in constraint and value < constraint["min_value"]:
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Field '{field}' must be >= {constraint['min_value']}",
                    suggested_fix=f"Set value to {constraint['min_value']} or higher"
                ))
            if "max_value" in constraint and value > constraint["max_value"]:
                issues.append(ValidationIssue(
                    field=field,
                    severity=ValidationSeverity.WARNING,
                    message=f"Field '{field}' should be <= {constraint['max_value']}",
                    suggested_fix=f"Reduce to {constraint['max_value']} or lower"
                ))
        
        return issues


class InputValidatorFactory:
    """Factory for InputValidator singleton."""
    
    _instance: Optional[InputValidator] = None
    
    @classmethod
    def get_validator(cls) -> InputValidator:
        """Get or create singleton InputValidator instance."""
        if cls._instance is None:
            cls._instance = InputValidator()
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        cls._instance = None
