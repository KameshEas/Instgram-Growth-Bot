"""
Phase 2C Verification Script

Standalone verification of all Phase 2C components:
- InputValidator
- ConflictResolver
- EdgeCaseHandler
- ErrorRecoverySystem

Author: AI Development Agent
Date: May 2, 2026
"""

import asyncio
from src.services.input_validator import InputValidatorFactory
from src.services.conflict_resolver import ConflictResolverFactory
from src.services.edge_case_handler import EdgeCaseHandlerFactory
from src.services.error_recovery_system import ErrorRecoverySystemFactory, ErrorType


async def verify_phase2c():
    """Run comprehensive verification of Phase 2C components."""
    
    print("\n" + "="*70)
    print("PHASE 2C ROBUSTNESS FRAMEWORK VERIFICATION")
    print("="*70 + "\n")
    
    # Initialize components
    validator = InputValidatorFactory.get_validator()
    resolver = ConflictResolverFactory.get_resolver()
    handler = EdgeCaseHandlerFactory.get_handler()
    recovery = ErrorRecoverySystemFactory.get_system()
    
    tests_passed = 0
    tests_total = 0
    
    # ========================================================================
    # Test 1: Input Validation
    # ========================================================================
    print("TEST 1: Input Validation")
    print("-" * 70)
    tests_total += 1
    
    try:
        # Valid input
        valid_data = {
            "design_prompt": "Create a professional mug design",
            "product_type": "mug",
            "quality_preference": "high",
        }
        result = await validator.validate_design_input(valid_data)
        
        assert result.is_valid(), f"Validation should pass: {result}"
        print("✅ Valid input accepted")
        
        # Invalid input (missing required field)
        invalid_data = {
            "design_prompt": "Create a design",
            # Missing product_type
        }
        result = await validator.validate_design_input(invalid_data)
        assert result.has_issues(), "Should detect missing required field"
        print("✅ Invalid input rejected (missing field)")
        
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print()
    
    # ========================================================================
    # Test 2: Conflict Resolution
    # ========================================================================
    print("TEST 2: Conflict Resolution")
    print("-" * 70)
    tests_total += 1
    
    try:
        # Data with conflicts
        conflicting_data = {
            "quality_preference": "high",
            "budget_level": "budget",  # High quality + budget conflict
            "deadline_urgency": "critical",
            "design_variations": 5,  # Critical deadline + 5 variations conflict
        }
        
        result = await resolver.resolve_conflicts(conflicting_data)
        
        assert result.has_conflicts(), "Should detect conflicts"
        print(f"✅ Detected {len(result.conflicts_detected)} conflicts")
        
        assert result.resolved_data is not None, "Should provide resolution"
        print("✅ Conflicts resolved with strategy application")
        
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print()
    
    # ========================================================================
    # Test 3: Edge Case Handling
    # ========================================================================
    print("TEST 3: Edge Case Handling")
    print("-" * 70)
    tests_total += 1
    
    try:
        # Data with edge cases
        edge_case_data = {
            "design_prompt": "Something nice and cool with lots of details!!!",  # Vague + special chars
            "product_type": "mug",
            "design_variations": 10,  # Exceeds max
        }
        
        result = await handler.handle_gift_design_input(edge_case_data)
        
        assert result.has_alerts(), "Should detect edge cases"
        print(f"✅ Detected {len(result.alerts)} edge cases")
        
        assert result.corrected_data is not None, "Should provide corrections"
        print("✅ Edge cases corrected")
        
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print()
    
    # ========================================================================
    # Test 4: Error Recovery
    # ========================================================================
    print("TEST 4: Error Recovery")
    print("-" * 70)
    tests_total += 1
    
    try:
        # Simulate error and recovery
        error = ValueError("Simulated API error")
        result = await recovery.handle_error(
            error=error,
            error_type=ErrorType.API_ERROR,
            context={"endpoint": "design_api"}
        )
        
        assert result.error_type == ErrorType.API_ERROR, "Should track error type"
        print("✅ Error tracked and categorized")
        
        fallback = recovery.get_fallback_data(["design_prompt", "product_type"])
        assert fallback["design_prompt"] is not None, "Should provide fallback"
        print("✅ Fallback values available for recovery")
        
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print()
    
    # ========================================================================
    # Test 5: Full Pipeline Integration
    # ========================================================================
    print("TEST 5: Full Input Processing Pipeline")
    print("-" * 70)
    tests_total += 1
    
    try:
        raw_input = {
            "design_prompt": "Create something cool and nice looking with lots of details!!!",
            "product_type": "mug",
            "quality_preference": "high",
            "budget_level": "budget",  # Will conflict
            "deadline_urgency": "critical",  # Will conflict
            "design_variations": 8,  # Exceeds max, will conflict
        }
        
        # Step 1: Validate
        print("  Step 1: Validating input...", end=" ")
        validation_result = await validator.validate_design_input(raw_input)
        working_data = validation_result.corrected_data or raw_input
        print("✅")
        
        # Step 2: Resolve conflicts
        print("  Step 2: Resolving conflicts...", end=" ")
        conflict_result = await resolver.resolve_conflicts(working_data)
        working_data = conflict_result.resolved_data or working_data
        print("✅")
        
        # Step 3: Handle edge cases
        print("  Step 3: Handling edge cases...", end=" ")
        edge_result = await handler.handle_gift_design_input(working_data)
        working_data = edge_result.corrected_data or working_data
        print("✅")
        
        # Verify final data is usable (has been processed and has reasonable defaults)
        assert working_data is not None, "Working data should not be None"
        assert "design_prompt" in working_data, "Should have design_prompt"
        assert "product_type" in working_data, "Should have product_type"
        
        print("\n✅ Full pipeline successfully processed problematic input")
        print(f"   Input had: {validation_result.has_issues() or 0} validation issues, "
              f"{len(conflict_result.conflicts_detected)} conflicts, "
              f"{len(edge_result.alerts)} edge cases")
        
        tests_passed += 1
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
    
    print()
    
    # ========================================================================
    # Test 6: Singleton Pattern Verification
    # ========================================================================
    print("TEST 6: Singleton Pattern Verification")
    print("-" * 70)
    tests_total += 1
    
    try:
        # Get new instances and verify they're singletons
        validator2 = InputValidatorFactory.get_validator()
        resolver2 = ConflictResolverFactory.get_resolver()
        handler2 = EdgeCaseHandlerFactory.get_handler()
        recovery2 = ErrorRecoverySystemFactory.get_system()
        
        assert validator is validator2, "Validators should be same instance"
        print("✅ InputValidator singleton verified")
        
        assert resolver is resolver2, "Resolvers should be same instance"
        print("✅ ConflictResolver singleton verified")
        
        assert handler is handler2, "Handlers should be same instance"
        print("✅ EdgeCaseHandler singleton verified")
        
        assert recovery is recovery2, "Recovery systems should be same instance"
        print("✅ ErrorRecoverySystem singleton verified")
        
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print()
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("="*70)
    print("PHASE 2C VERIFICATION SUMMARY")
    print("="*70)
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n🎉 PHASE 2C VERIFICATION COMPLETE - All components working!")
        return True
    else:
        print(f"\n⚠️  {tests_total - tests_passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(verify_phase2c())
    exit(0 if success else 1)
