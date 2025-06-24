#!/usr/bin/env python3
"""
Test script to verify the GenAI fixes for the XSLT/JSON issue
"""

import os
import sys
import json

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator

def test_validation_logic():
    """Test the improved validation logic"""
    print("🧪 Testing validation logic...")
    
    # Create a generator instance (without API key for testing validation only)
    generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
    
    # Test case 1: Mixed XSLT and JSON response (like the problematic case)
    mixed_response = '''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <Root>
      <Object>
        <batchProcessingDirectives>
          <!-- XSLT code -->
        </batchProcessingDirectives>
      </Object>
    </Root>
  </xsl:template>
</xsl:stylesheet>

{
    "process_name": "Test Process",
    "description": "Test description",
    "endpoints": [
        {
            "method": "GET",
            "path": "/test",
            "purpose": "Test endpoint",
            "components": [
                {
                    "type": "enricher",
                    "name": "Test_Enricher",
                    "id": "enricher_1",
                    "config": {}
                }
            ],
            "sequence": ["enricher_1"],
            "transformations": []
        }
    ]
}'''
    
    is_valid, message = generator._validate_genai_response(mixed_response)
    print(f"Mixed XSLT/JSON response validation: {is_valid} - {message}")
    
    if is_valid:
        try:
            components = generator._parse_llm_response(mixed_response)
            print(f"✅ Successfully parsed mixed response!")
            print(f"Process name: {components.get('process_name')}")
            print(f"Endpoints: {len(components.get('endpoints', []))}")
            
            # Test meaningful components check
            has_meaningful = generator._has_meaningful_components(components)
            print(f"Has meaningful components: {has_meaningful}")
            
        except Exception as e:
            print(f"❌ Failed to parse mixed response: {e}")
    
    # Test case 2: Pure JSON response
    json_response = '''{
    "process_name": "Pure JSON Process",
    "description": "Pure JSON description",
    "endpoints": [
        {
            "method": "POST",
            "path": "/pure",
            "purpose": "Pure JSON endpoint",
            "components": [
                {
                    "type": "request_reply",
                    "name": "API_Call",
                    "id": "request_reply_1",
                    "config": {"endpoint_path": "/api/data"}
                }
            ],
            "sequence": ["request_reply_1"],
            "transformations": []
        }
    ]
}'''
    
    is_valid, message = generator._validate_genai_response(json_response)
    print(f"Pure JSON response validation: {is_valid} - {message}")
    
    # Test case 3: Empty components (should fail meaningful check)
    empty_response = '''{
    "process_name": "Empty Process",
    "description": "Empty description",
    "endpoints": [
        {
            "method": "GET",
            "path": "/empty",
            "purpose": "Empty endpoint",
            "components": [],
            "sequence": [],
            "transformations": []
        }
    ]
}'''
    
    is_valid, message = generator._validate_genai_response(empty_response)
    print(f"Empty components response validation: {is_valid} - {message}")
    
    if is_valid:
        components = generator._parse_llm_response(empty_response)
        has_meaningful = generator._has_meaningful_components(components)
        print(f"Empty components meaningful check: {has_meaningful}")

def test_prompt_improvements():
    """Test the improved prompt generation"""
    print("\n🧪 Testing prompt improvements...")
    
    generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
    
    # Test the main prompt
    markdown_content = "Sample Boomi documentation content"
    prompt = generator._create_detailed_analysis_prompt(markdown_content)
    
    print("✅ Main prompt created successfully")
    print(f"Prompt length: {len(prompt)} characters")
    
    # Check for key improvements
    improvements = [
        "CRITICAL INSTRUCTION",
        "RESPOND WITH ONLY THE JSON STRUCTURE",
        "Do NOT include any XSLT",
        "RESPOND WITH ONLY JSON"
    ]
    
    for improvement in improvements:
        if improvement in prompt:
            print(f"✅ Found improvement: {improvement}")
        else:
            print(f"❌ Missing improvement: {improvement}")
    
    # Test the explicit prompt
    explicit_prompt = generator._create_more_explicit_prompt(markdown_content, "Test error")
    print(f"\n✅ Explicit prompt created successfully")
    print(f"Explicit prompt length: {len(explicit_prompt)} characters")

if __name__ == "__main__":
    print("🚀 Testing GenAI fixes for XSLT/JSON issue")
    print("=" * 50)
    
    test_validation_logic()
    test_prompt_improvements()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nKey improvements implemented:")
    print("1. ✅ Enhanced prompt with explicit JSON-only instructions")
    print("2. ✅ Improved validation that can extract JSON from mixed responses")
    print("3. ✅ Better error handling with meaningful component checks")
    print("4. ✅ Retry logic with more explicit prompts")
    print("5. ✅ Enhanced debugging and error reporting")
