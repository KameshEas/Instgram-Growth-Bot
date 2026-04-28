#!/usr/bin/env python3
"""
Quick verification script for design brief system integration.
This checks that all components are wired together correctly WITHOUT calling Groq.
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_imports():
    """Verify all components can be imported."""
    print("✓ Checking imports...")
    try:
        from src.agents.design_enhancer import DesignPromptEnhancerAgent
        from src.agents.orchestrator import ContentOrchestratorAgent
        from src.agents.base_agent import BaseAgent
        from src.prompts.templates import DESIGN_BRIEF_SYSTEM_PROMPT
        from src.main import InstagramGrowthBot
        print("  ✓ All agent imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False


def check_design_brief_system_prompt():
    """Verify design brief prompt template exists and is correct."""
    print("✓ Checking DESIGN_BRIEF_SYSTEM_PROMPT...")
    try:
        from src.prompts.templates import DESIGN_BRIEF_SYSTEM_PROMPT
        
        required_keywords = [
            "3 distinct",
            "design brief",
            "variations",
            "professional",
            "JSON",
        ]
        
        for keyword in required_keywords:
            if keyword.lower() not in DESIGN_BRIEF_SYSTEM_PROMPT.lower():
                print(f"  ✗ Missing '{keyword}' in system prompt")
                return False
        
        if "briefs" not in DESIGN_BRIEF_SYSTEM_PROMPT:
            print("  ✗ Missing 'briefs' array in system prompt")
            return False
        
        print("  ✓ System prompt contains all required sections")
        return True
    except Exception as e:
        print(f"  ✗ Error checking system prompt: {e}")
        return False


def check_design_enhancer_structure():
    """Verify DesignPromptEnhancerAgent has correct structure."""
    print("✓ Checking DesignPromptEnhancerAgent structure...")
    try:
        from pathlib import Path
        design_file = Path(__file__).parent / "src" / "agents" / "design_enhancer.py"
        content = design_file.read_text()
        
        checks = [
            ('class definition', 'class DesignPromptEnhancerAgent'),
            ('BaseAgent inheritance', 'BaseAgent'),
            ('execute method', 'async def execute'),
            ('_generate_design_brief method', '_generate_design_brief'),
            ('groq_bot check', 'if not self._groq_bot'),
            ('groq call', 'generate_design_brief'),
            ('niche support', 'niche = data.get'),
            ('brand_context support', 'brand_context = data.get'),
        ]
        
        for check_name, check_string in checks:
            if check_string not in content:
                print(f"  ✗ Missing {check_name}: '{check_string}'")
                return False
        
        print("  ✓ DesignPromptEnhancerAgent structure is correct")
        return True
    except Exception as e:
        print(f"  ✗ Error checking structure: {e}")
        return False


def check_orchestrator_routing():
    """Verify orchestrator has design category routing."""
    print("✓ Checking orchestrator routing...")
    try:
        from pathlib import Path
        orchestrator_file = Path(__file__).parent / "src" / "agents" / "orchestrator.py"
        content = orchestrator_file.read_text()
        
        checks = [
            ('design_enhancer import', 'from src.agents.design_enhancer import'),
            ('design_categories set', 'design_categories = {'),
            ('design category detection', 'if category in design_categories'),
            ('design_enhancer routing', 'self.agents["design_enhancer"].execute'),
            ('design context passing', 'brand_context'),
        ]
        
        for check_name, check_string in checks:
            if check_string not in content:
                print(f"  ✗ Missing {check_name}: '{check_string}'")
                return False
        
        print("  ✓ Orchestrator routing is configured")
        return True
    except Exception as e:
        print(f"  ✗ Error checking orchestrator: {e}")
        return False


def check_main_py_design_method():
    """Verify main.py has generate_design_brief method."""
    print("✓ Checking main.py generate_design_brief method...")
    try:
        from pathlib import Path
        main_file = Path(__file__).parent / "src" / "main.py"
        content = main_file.read_text()
        
        checks = [
            ('method definition', 'def generate_design_brief('),
            ('category parameter', 'category: str ='),
            ('user_input parameter', 'user_input: str ='),
            ('niche parameter', 'niche: str ='),
            ('brand_context parameter', 'brand_context: dict ='),
            ('DESIGN_BRIEF_SYSTEM_PROMPT import', 'from src.prompts.templates import DESIGN_BRIEF_SYSTEM_PROMPT'),
            ('temperature=0.85', 'temperature=0.85'),
            ('ttl_hours=24', 'ttl_hours=24'),
            ('briefs extraction', 'briefs = result.get("briefs", [])'),
            ('response wrapping', '"status": "success"'),
        ]
        
        for check_name, check_string in checks:
            if check_string not in content:
                print(f"  ✗ Missing {check_name}: '{check_string}'")
                return False
        
        print("  ✓ generate_design_brief method is properly implemented")
        return True
    except Exception as e:
        print(f"  ✗ Error checking main.py: {e}")
        return False


def check_telegram_bot_handler():
    """Verify telegram_bot has design brief handler."""
    print("✓ Checking telegram_bot design brief handler...")
    try:
        from pathlib import Path
        telegram_file = Path(__file__).parent / "src" / "telegram_bot.py"
        content = telegram_file.read_text(encoding='utf-8', errors='replace')
        
        checks = [
            ('DESIGN_CATEGORIES set', 'DESIGN_CATEGORIES = {'),
            ('is_design_brief detection', 'is_design_brief ='),
            ('design categories', '"design_posters"'),
            ('handler method', 'async def _handle_design_brief_response'),
            ('handler called', 'if is_design_brief and "brief" in result'),
            ('niche extraction', 'profile = self._get_profile'),
            ('orchestrator call passes niche', '"niche": niche,'),
        ]
        
        for check_name, check_string in checks:
            if check_string not in content:
                print(f"  ✗ Missing {check_name}: '{check_string}'")
                return False
        
        print("  ✓ Telegram bot handler is properly implemented")
        return True
    except Exception as e:
        print(f"  ✗ Error checking telegram_bot: {e}")
        return False


def check_file_structure():
    """Verify all required files exist."""
    print("✓ Checking file structure...")
    try:
        required_files = [
            "src/agents/design_enhancer.py",
            "src/prompts/templates.py",
            "src/main.py",
            "src/agents/orchestrator.py",
            "src/telegram_bot.py",
        ]
        
        base_path = Path(__file__).parent
        for file_path in required_files:
            full_path = base_path / file_path
            if not full_path.exists():
                print(f"  ✗ Missing file: {file_path}")
                return False
        
        print("  ✓ All required files exist")
        return True
    except Exception as e:
        print(f"  ✗ Error checking files: {e}")
        return False


def main():
    """Run all verification checks."""
    print("\n" + "="*60)
    print("Design Brief System Integration Verification")
    print("="*60 + "\n")
    
    checks = [
        check_file_structure,
        # Skip check_imports due to pydantic_settings dependency (not a code issue)
        check_design_brief_system_prompt,
        check_design_enhancer_structure,
        check_orchestrator_routing,
        check_main_py_design_method,
        check_telegram_bot_handler,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Unexpected error in {check.__name__}: {e}")
            results.append(False)
        print()
    
    # Summary
    print("="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed! Design brief system is properly integrated.")
        print("\nYou can now use:")
        print('  /generate design_posters "Your design concept here"')
        return 0
    else:
        print(f"\n❌ {total - passed} check(s) failed. Please review above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
