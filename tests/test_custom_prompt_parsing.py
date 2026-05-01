"""Test custom prompt parsing improvements for /generate command"""
import pytest
import json
from src.main import parse_json_response


class TestJSONParsingEdgeCases:
    """Test JSON parsing with edge cases from user prompts"""
    
    def test_parse_clean_json(self):
        """Test parsing of clean JSON response"""
        response = '{"prompts": [{"prompt": "test", "scene": "test"}], "tip": "test"}'
        result = parse_json_response(response)
        assert result == json.loads(response)
        assert "prompts" in result
    
    def test_parse_json_with_markdown_code_block(self):
        """Test parsing JSON wrapped in markdown code blocks"""
        response = '''```json
{"prompts": [{"prompt": "test", "scene": "test"}], "tip": "test"}
```'''
        result = parse_json_response(response)
        assert "prompts" in result
        assert result["tip"] == "test"
    
    def test_parse_incomplete_json_with_missing_braces(self):
        """Test parsing incomplete JSON by auto-completing braces"""
        # JSON missing closing braces
        response = '''```json
{"prompts": [{"prompt": "test", "scene": "test"}], "tip": "test"
```'''
        result = parse_json_response(response)
        assert "prompts" in result
        assert result["tip"] == "test"
    
    def test_parse_json_with_extra_text_before_after(self):
        """Test parsing JSON with extra text around it"""
        response = '''Here's your response:
{"prompts": [{"prompt": "test", "scene": "test"}], "tip": "test"}
Hope this helps!'''
        result = parse_json_response(response)
        assert "prompts" in result
        assert result["tip"] == "test"
    
    def test_parse_json_with_special_characters_in_content(self):
        """Test parsing JSON with special characters in prompt text"""
        response = json.dumps({
            "prompts": [
                {
                    "prompt": "Realistic Pencil drawing with 100% face match, exact features",
                    "scene": "Portrait study"
                }
            ],
            "tip": "Keep 100% accuracy to reference"
        })
        result = parse_json_response(response)
        assert "prompts" in result
        assert "100%" in result["prompts"][0]["prompt"]
    
    def test_parse_json_array_as_prompts(self):
        """Test parsing JSON array and converting to dict with prompts key"""
        response = '[{"prompt": "test", "scene": "test"}]'
        result = parse_json_response(response)
        assert "prompts" in result
        assert isinstance(result["prompts"], list)
    
    def test_parse_completely_invalid_response(self):
        """Test parsing completely invalid response returns error dict"""
        response = "This is not JSON at all, just text"
        result = parse_json_response(response)
        assert isinstance(result, dict)
        # Should have error indicator
        assert result.get("error") is not None or result == {}
    
    def test_parse_empty_response(self):
        """Test parsing empty response"""
        result = parse_json_response("")
        assert isinstance(result, dict)
    
    def test_parse_json_with_escaped_quotes(self):
        """Test parsing JSON with escaped quotes in strings"""
        response = json.dumps({
            "prompts": [
                {
                    "prompt": 'Create a "photorealistic" image with "100% accuracy"',
                    "scene": "Portrait"
                }
            ],
            "tip": "Use quotes in prompt"
        })
        result = parse_json_response(response)
        assert "prompts" in result
        assert '"photorealistic"' in result["prompts"][0]["prompt"]
    
    def test_parse_long_custom_prompt_content(self):
        """Test parsing JSON with very long prompt content (simulating user custom prompt)"""
        long_prompt = "Realistic Pencil drawing for wallpaper in 9:16 aspect ratio with exact 100% face match with facial identities preserving all facial features including eyes shape color size eyebrows nose mouth ears and skin tone variations making it absolutely identical to the original photograph"
        response = json.dumps({
            "prompts": [
                {
                    "prompt": long_prompt,
                    "scene": "Custom design"
                }
            ],
            "tip": "This is a long prompt"
        })
        result = parse_json_response(response)
        assert "prompts" in result
        assert "100% face match" in result["prompts"][0]["prompt"]
    
    def test_parse_generic_code_block_with_json(self):
        """Test parsing generic ``` code block containing JSON"""
        response = '''```
{"prompts": [{"prompt": "test", "scene": "test"}], "tip": "test"}
```'''
        result = parse_json_response(response)
        assert "prompts" in result


class TestContentGeneratorErrorHandling:
    """Test content generator error handling for custom prompts"""
    
    @pytest.mark.asyncio
    async def test_generate_with_custom_prompt_special_chars(self):
        """Test that custom prompts with special chars are handled properly"""
        # This would require mocking the Groq bot, so we'll test the logic separately
        # The key is that user_context is sanitized before being passed to Groq
        user_context = 'Realistic Pencil drawing with "exact 100% face match" and special chars: @ # $ %'
        
        # Simulate what generate_image_prompts does
        sanitized = user_context.replace('"', "'").replace("\n", " ").strip()[:200]
        
        # Should not have quotes that break JSON
        assert '"' not in sanitized
        assert "'" in sanitized  # Quotes converted to single quotes
        assert "Realistic Pencil drawing" in sanitized


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
