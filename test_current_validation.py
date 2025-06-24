#!/usr/bin/env python3
"""
Test the current validation logic with the actual problematic response
"""

import os
import sys
import json

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def test_with_actual_response():
    """Test with the actual problematic response"""
    print("🧪 Testing current validation with actual problematic response...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Create a generator instance
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        
        # Read the actual problematic response
        with open("BoomiToIS-API/genai_debug/raw_analysis_response.txt", "r", encoding="utf-8") as f:
            actual_response = f.read()
        
        print(f"Response length: {len(actual_response)} characters")
        print(f"Response preview: {actual_response[:100]}...")
        
        # Test validation
        is_valid, message = generator._validate_genai_response(actual_response)
        print(f"Validation result: {is_valid} - {message}")
        
        if is_valid:
            try:
                components = generator._parse_llm_response(actual_response)
                print(f"✅ Successfully parsed response!")
                print(f"Components structure: {json.dumps(components, indent=2)}")
                
                # Test meaningful components check
                has_meaningful = generator._has_meaningful_components(components)
                print(f"Has meaningful components: {has_meaningful}")
                
            except Exception as e:
                print(f"❌ Failed to parse response: {e}")
        else:
            print(f"❌ Validation failed: {message}")
            
            # Let's manually try to extract JSON
            print("\n🔍 Manual JSON extraction attempt:")
            start_brace = actual_response.find('{')
            end_brace = actual_response.rfind('}')
            
            if start_brace != -1 and end_brace != -1:
                json_part = actual_response[start_brace:end_brace + 1]
                print(f"Extracted JSON part: {json_part}")
                
                try:
                    parsed = json.loads(json_part)
                    print(f"✅ Manual parsing successful!")
                    print(f"Parsed structure: {json.dumps(parsed, indent=2)}")
                except Exception as e:
                    print(f"❌ Manual parsing failed: {e}")
            else:
                print("❌ No JSON braces found")
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the correct directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_validation_improvements():
    """Test if the validation improvements are working"""
    print("\n🧪 Testing validation improvements...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        
        # Test case 1: Pure JSON
        pure_json = '''{
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
        
        is_valid, message = generator._validate_genai_response(pure_json)
        print(f"Pure JSON validation: {is_valid} - {message}")
        
        # Test case 2: JSON with markdown blocks
        markdown_json = '''```json
{
    "process_name": "Markdown Process",
    "description": "Markdown description",
    "endpoints": [
        {
            "method": "POST",
            "path": "/markdown",
            "purpose": "Markdown endpoint",
            "components": [],
            "sequence": [],
            "transformations": []
        }
    ]
}
```'''
        
        is_valid, message = generator._validate_genai_response(markdown_json)
        print(f"Markdown JSON validation: {is_valid} - {message}")
        
        # Test case 3: Mixed content (XSLT + JSON)
        mixed_content = '''<?xml version="1.0"?>
<xsl:stylesheet>
  <xsl:template match="/">
    <root>test</root>
  </xsl:template>
</xsl:stylesheet>

{
    "process_name": "Mixed Process",
    "description": "Mixed description",
    "endpoints": [
        {
            "method": "PUT",
            "path": "/mixed",
            "purpose": "Mixed endpoint",
            "components": [
                {
                    "type": "request_reply",
                    "name": "API_Call",
                    "id": "request_reply_1",
                    "config": {}
                }
            ],
            "sequence": ["request_reply_1"],
            "transformations": []
        }
    ]
}'''
        
        is_valid, message = generator._validate_genai_response(mixed_content)
        print(f"Mixed content validation: {is_valid} - {message}")
        
        if is_valid:
            components = generator._parse_llm_response(mixed_content)
            has_meaningful = generator._has_meaningful_components(components)
            print(f"Mixed content meaningful check: {has_meaningful}")
        
    except Exception as e:
        print(f"❌ Error testing validation improvements: {e}")

if __name__ == "__main__":
    print("🚀 Testing current validation logic")
    print("=" * 50)
    
    test_with_actual_response()
    test_validation_improvements()
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")
