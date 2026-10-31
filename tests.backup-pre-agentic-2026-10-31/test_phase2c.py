"""
Phase 2C Robustness Framework - Comprehensive Test Suite

Tests for:
- InputValidator
- ConflictResolver
- EdgeCaseHandler
- ErrorRecoverySystem

Author: AI Development Agent
Date: May 2, 2026
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Assuming services are in src/services
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.input_validator import (
    InputValidator, InputValidatorFactory, ValidationStatus, ValidationSeverity
)
from src.services.conflict_resolver import (
    ConflictResolver, ConflictResolverFactory, ConflictSeverity, ResolutionStrategy
)
from src.services.edge_case_handler import (
    EdgeCaseHandler, EdgeCaseHandlerFactory, EdgeCaseType
)
from src.services.error_recovery_system import (
    ErrorRecoverySystem, ErrorRecoverySystemFactory, ErrorType, RecoveryStrategy
)


# ============================================================================
# INPUT VALIDATOR TESTS
# ============================================================================

class TestInputValidator:
    """Test InputValidator component."""
    
    @pytest.fixture
    def validator(self):
        InputValidatorFactory.reset()
        return InputValidatorFactory.get_validator()
    
    @pytest.mark.asyncio
    async def test_validator_initialization(self, validator):
        """Test validator initializes with constraints."""
        assert validator is not None
        assert len(validator.constraints) > 0
        assert len(validator.required_fields) > 0
    
    @pytest.mark.asyncio
    async def test_valid_design_input(self, validator):
        """Test validation of valid design input."""
        data = {
            "design_prompt": "Create a unique mug design",
            "product_type": "mug",
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.PASS
        assert not result.has_issues()
    
    @pytest.mark.asyncio
    async def test_missing_required_field(self, validator):
        """Test validation catches missing required field."""
        data = {
            "design_prompt": "Create a design",
            # Missing product_type
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.FAIL
        assert result.has_issues()
        assert any("product_type" in issue.field for issue in result.issues)
    
    @pytest.mark.asyncio
    async def test_invalid_product_type(self, validator):
        """Test validation catches invalid product type."""
        data = {
            "design_prompt": "Create a design",
            "product_type": "invalid_type",
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.FAIL
        assert result.has_issues()
    
    @pytest.mark.asyncio
    async def test_prompt_too_long(self, validator):
        """Test validation warns on overly long prompt."""
        data = {
            "design_prompt": "A" * 3000,  # Exceeds max
            "product_type": "t_shirt",
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.WARN
        assert result.has_warnings()
    
    @pytest.mark.asyncio
    async def test_prompt_too_short(self, validator):
        """Test validation catches too-short prompt."""
        data = {
            "design_prompt": "abc",  # Below min
            "product_type": "t_shirt",
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.FAIL
        assert result.has_issues()
    
    @pytest.mark.asyncio
    async def test_invalid_quality_preference(self, validator):
        """Test validation catches invalid quality preference."""
        data = {
            "design_prompt": "Create a design",
            "product_type": "t_shirt",
            "quality_preference": "ultra_high",
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.FAIL
    
    @pytest.mark.asyncio
    async def test_valid_quality_preference(self, validator):
        """Test validation accepts valid quality preference."""
        data = {
            "design_prompt": "Create a design",
            "product_type": "t_shirt",
            "quality_preference": "high",
        }
        result = await validator.validate_design_input(data)
        assert result.status == ValidationStatus.PASS
    
    @pytest.mark.asyncio
    async def test_default_values_added(self, validator):
        """Test validator adds default values for optional fields."""
        data = {
            "design_prompt": "Create a design",
            "product_type": "t_shirt",
        }
        result = await validator.validate_design_input(data)
        assert result.corrected_data is not None
        assert "quality_preference" in result.corrected_data
        assert result.corrected_data["quality_preference"] == "balanced"
    
    @pytest.mark.asyncio
    async def test_singleton_pattern(self, validator):
        """Test validator follows singleton pattern."""
        validator2 = InputValidatorFactory.get_validator()
        assert validator is validator2


# ============================================================================
# CONFLICT RESOLVER TESTS
# ============================================================================

class TestConflictResolver:
    """Test ConflictResolver component."""
    
    @pytest.fixture
    def resolver(self):
        ConflictResolverFactory.reset()
        return ConflictResolverFactory.get_resolver()
    
    @pytest.mark.asyncio
    async def test_resolver_initialization(self, resolver):
        """Test resolver initializes with conflict rules."""
        assert resolver is not None
        assert len(resolver.conflict_rules) > 0
    
    @pytest.mark.asyncio
    async def test_no_conflicts(self, resolver):
        """Test detection when no conflicts exist."""
        data = {
            "product_type": "t_shirt",
            "quality_preference": "high",
            "budget_level": "premium",
        }
        result = await resolver.resolve_conflicts(data)
        assert result.status == "no_conflicts"
        assert not result.has_conflicts()
    
    @pytest.mark.asyncio
    async def test_detect_quality_budget_conflict(self, resolver):
        """Test detection of quality-budget conflict."""
        data = {
            "quality_preference": "high",
            "budget_level": "budget",  # Conflict!
        }
        result = await resolver.resolve_conflicts(data)
        assert result.has_conflicts()
    
    @pytest.mark.asyncio
    async def test_detect_deadline_quality_conflict(self, resolver):
        """Test detection of deadline-quality conflict."""
        data = {
            "deadline_urgency": "critical",
            "quality_preference": "high",  # Conflict!
        }
        result = await resolver.resolve_conflicts(data)
        assert result.has_conflicts()
    
    @pytest.mark.asyncio
    async def test_detect_variations_deadline_conflict(self, resolver):
        """Test detection of variations-deadline conflict."""
        data = {
            "design_variations": 5,
            "deadline_urgency": "critical",  # Conflict!
        }
        result = await resolver.resolve_conflicts(data)
        assert result.has_conflicts()
    
    @pytest.mark.asyncio
    async def test_conflict_resolution_priority(self, resolver):
        """Test conflict is resolved with correct priority."""
        data = {
            "design_variations": 5,
            "deadline_urgency": "critical",
        }
        result = await resolver.resolve_conflicts(data)
        assert result.status == "conflicts_resolved"
        assert result.resolved_data is not None
    
    @pytest.mark.asyncio
    async def test_detect_product_design_mismatch(self, resolver):
        """Test detection of product-design mismatch."""
        data = {
            "product_type": "mug",
            "creative_direction": "full_body portrait with panoramic background",
        }
        result = await resolver.resolve_conflicts(data)
        # Should detect conflict since panoramic is incompatible with mug
        assert result.has_conflicts()
    
    @pytest.mark.asyncio
    async def test_singleton_pattern(self, resolver):
        """Test resolver follows singleton pattern."""
        resolver2 = ConflictResolverFactory.get_resolver()
        assert resolver is resolver2


# ============================================================================
# EDGE CASE HANDLER TESTS
# ============================================================================

class TestEdgeCaseHandler:
    """Test EdgeCaseHandler component."""
    
    @pytest.fixture
    def handler(self):
        EdgeCaseHandlerFactory.reset()
        return EdgeCaseHandlerFactory.get_handler()
    
    @pytest.mark.asyncio
    async def test_handler_initialization(self, handler):
        """Test handler initializes with configuration."""
        assert handler is not None
        assert len(handler.vague_keywords) > 0
    
    @pytest.mark.asyncio
    async def test_empty_input_detection(self, handler):
        """Test detection of empty input."""
        result = await handler.handle_gift_design_input({})
        assert result.has_alerts()
        assert any(a.case_type == EdgeCaseType.EMPTY_INPUT for a in result.alerts)
    
    @pytest.mark.asyncio
    async def test_extremely_long_prompt(self, handler):
        """Test detection of overly long prompt."""
        data = {
            "design_prompt": "A" * 3000,
        }
        result = await handler.handle_gift_design_input(data)
        assert result.has_alerts()
        assert any(a.case_type == EdgeCaseType.EXTREMELY_LONG for a in result.alerts)
    
    @pytest.mark.asyncio
    async def test_vague_request_detection(self, handler):
        """Test detection of vague language."""
        data = {
            "design_prompt": "Create something nice and cool that looks good",
        }
        result = await handler.handle_gift_design_input(data)
        assert result.has_alerts()
        # Should detect vague keywords
    
    @pytest.mark.asyncio
    async def test_unicode_content_detection(self, handler):
        """Test detection of unicode content."""
        data = {
            "design_prompt": "Create a design with émojis 🎨 and spëcial çharacters",
        }
        result = await handler.handle_gift_design_input(data)
        assert result.has_alerts()
        assert any(a.case_type == EdgeCaseType.UNICODE_CONTENT for a in result.alerts)
    
    @pytest.mark.asyncio
    async def test_special_characters_detection(self, handler):
        """Test detection of excessive special characters."""
        data = {
            "design_prompt": "!!!Create~~~design###with@@@many&&&special***chars!!!",
        }
        result = await handler.handle_gift_design_input(data)
        assert result.has_alerts()
    
    @pytest.mark.asyncio
    async def test_numeric_boundary_detection(self, handler):
        """Test detection of numeric boundaries."""
        data = {
            "design_variations": 10,  # Exceeds max of 5
        }
        result = await handler.handle_gift_design_input(data)
        assert result.has_alerts()
        assert any(a.case_type == EdgeCaseType.NUMERIC_BOUNDARY for a in result.alerts)
    
    @pytest.mark.asyncio
    async def test_contradictory_request_detection(self, handler):
        """Test detection of contradictory requests."""
        data = {
            "design_prompt": "Create a minimalist design",
            "creative_direction": "with lots of complex details",
        }
        result = await handler.handle_gift_design_input(data)
        assert result.has_alerts()
        assert any(a.case_type == EdgeCaseType.CONTRADICTORY_REQUEST for a in result.alerts)
    
    @pytest.mark.asyncio
    async def test_correction_application(self, handler):
        """Test that corrections are applied."""
        data = {
            "design_variations": 10,
        }
        result = await handler.handle_gift_design_input(data)
        if result.corrected_data:
            assert result.corrected_data.get("design_variations") <= 5
    
    @pytest.mark.asyncio
    async def test_singleton_pattern(self, handler):
        """Test handler follows singleton pattern."""
        handler2 = EdgeCaseHandlerFactory.get_handler()
        assert handler is handler2


# ============================================================================
# ERROR RECOVERY SYSTEM TESTS
# ============================================================================

class TestErrorRecoverySystem:
    """Test ErrorRecoverySystem component."""
    
    @pytest.fixture
    def system(self):
        ErrorRecoverySystemFactory.reset()
        return ErrorRecoverySystemFactory.get_system()
    
    @pytest.mark.asyncio
    async def test_system_initialization(self, system):
        """Test system initializes with strategies."""
        assert system is not None
        assert len(system.recovery_strategies) > 0
        assert len(system.fallback_values) > 0
    
    @pytest.mark.asyncio
    async def test_handle_api_error(self, system):
        """Test handling of API errors."""
        error = Exception("API call failed")
        result = await system.handle_error(
            error=error,
            error_type=ErrorType.API_ERROR,
            context={"endpoint": "design_api"}
        )
        assert result.error_type == ErrorType.API_ERROR
        assert result.recovery_attempted
    
    @pytest.mark.asyncio
    async def test_handle_parameter_error(self, system):
        """Test handling of parameter errors."""
        error = ValueError("Invalid parameter")
        result = await system.handle_error(
            error=error,
            error_type=ErrorType.PARAMETER_ERROR,
            context={"parameter": "quality"}
        )
        assert result.error_type == ErrorType.PARAMETER_ERROR
    
    @pytest.mark.asyncio
    async def test_handle_timeout_error(self, system):
        """Test handling of timeout errors."""
        error = TimeoutError("Operation timed out")
        result = await system.handle_error(
            error=error,
            error_type=ErrorType.TIMEOUT_ERROR,
        )
        assert result.error_type == ErrorType.TIMEOUT_ERROR
    
    @pytest.mark.asyncio
    async def test_fallback_values_available(self, system):
        """Test fallback values are available."""
        fallback_data = system.get_fallback_data()
        assert "design_prompt" in fallback_data
        assert "product_type" in fallback_data
        assert "quality_preference" in fallback_data
    
    @pytest.mark.asyncio
    async def test_selective_fallback(self, system):
        """Test retrieving specific fallback fields."""
        fallback_data = system.get_fallback_data(["design_prompt", "product_type"])
        assert "design_prompt" in fallback_data
        assert "product_type" in fallback_data
        assert len(fallback_data) == 2
    
    @pytest.mark.asyncio
    async def test_singleton_pattern(self, system):
        """Test system follows singleton pattern."""
        system2 = ErrorRecoverySystemFactory.get_system()
        assert system is system2


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestPhase2CIntegration:
    """Test Phase 2C components working together."""
    
    @pytest.fixture
    def components(self):
        InputValidatorFactory.reset()
        ConflictResolverFactory.reset()
        EdgeCaseHandlerFactory.reset()
        ErrorRecoverySystemFactory.reset()
        
        return {
            "validator": InputValidatorFactory.get_validator(),
            "resolver": ConflictResolverFactory.get_resolver(),
            "handler": EdgeCaseHandlerFactory.get_handler(),
            "recovery": ErrorRecoverySystemFactory.get_system(),
        }
    
    @pytest.mark.asyncio
    async def test_full_input_pipeline(self, components):
        """Test complete input processing pipeline."""
        raw_data = {
            "design_prompt": "Create a unique and cool mug design",
            "product_type": "mug",
            "quality_preference": "high",
            "budget_level": "budget",  # Will conflict
            "design_variations": 4,
            "deadline_urgency": "critical",  # Will conflict
        }
        
        # Step 1: Validate input
        validation = await components["validator"].validate_design_input(raw_data)
        assert validation.status != ValidationStatus.FAIL or validation.corrected_data
        
        # Step 2: Check for conflicts
        conflict_data = validation.corrected_data or raw_data
        conflicts = await components["resolver"].resolve_conflicts(conflict_data)
        resolved_data = conflicts.resolved_data or conflict_data
        
        # Step 3: Check edge cases
        edges = await components["handler"].handle_gift_design_input(resolved_data)
        final_data = edges.corrected_data or resolved_data
        
        # Final data should be usable
        assert final_data is not None
        assert "design_prompt" in final_data
        assert "product_type" in final_data
    
    @pytest.mark.asyncio
    async def test_error_recovery_integration(self, components):
        """Test error recovery with other components."""
        try:
            raise ValueError("Simulated validation error")
        except ValueError as e:
            result = await components["recovery"].handle_error(
                error=e,
                error_type=ErrorType.VALIDATION_ERROR,
                context={"field": "design_prompt"}
            )
            
            assert result.error_type == ErrorType.VALIDATION_ERROR
            # Can use fallback data
            fallback = components["recovery"].get_fallback_data(["design_prompt"])
            assert fallback["design_prompt"] is not None


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPhase2CPerformance:
    """Test Phase 2C component performance."""
    
    @pytest.mark.asyncio
    async def test_validation_performance(self):
        """Test validation completes quickly."""
        validator = InputValidatorFactory.get_validator()
        
        data = {
            "design_prompt": "Create a professional design for a t-shirt",
            "product_type": "t_shirt",
            "quality_preference": "balanced",
            "design_variations": 3,
        }
        
        import time
        start = time.time()
        result = await validator.validate_design_input(data)
        elapsed = time.time() - start
        
        assert elapsed < 0.1  # Should be very fast
        assert result.status == ValidationStatus.PASS
    
    @pytest.mark.asyncio
    async def test_conflict_detection_performance(self):
        """Test conflict detection completes quickly."""
        resolver = ConflictResolverFactory.get_resolver()
        
        data = {
            "product_type": "mug",
            "quality_preference": "high",
            "budget_level": "premium",
            "deadline_urgency": "medium",
            "design_variations": 3,
        }
        
        import time
        start = time.time()
        result = await resolver.resolve_conflicts(data)
        elapsed = time.time() - start
        
        assert elapsed < 0.1  # Should be very fast


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
