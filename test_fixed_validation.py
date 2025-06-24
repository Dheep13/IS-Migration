#!/usr/bin/env python3
"""
Test the fixed validation logic
"""

import os
import sys
import json

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def test_fixed_validation():
    """Test the fixed validation with the actual problematic response"""
    print("🧪 Testing fixed validation logic...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Create a generator instance
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        
        # Read the actual problematic response
        with open("BoomiToIS-API/genai_debug/raw_analysis_response.txt", "r", encoding="utf-8") as f:
            actual_response = f.read()
        
        print(f"Response length: {len(actual_response)} characters")
        
        # Test validation
        is_valid, message = generator._validate_genai_response(actual_response)
        print(f"Validation result: {is_valid} - {message}")
        
        if is_valid:
            try:
                components = generator._parse_llm_response(actual_response)
                print(f"✅ Successfully parsed response!")
                print(f"Components keys: {list(components.keys())}")
                
                if "endpoints" in components:
                    print(f"Number of endpoints: {len(components['endpoints'])}")
                    for i, endpoint in enumerate(components['endpoints']):
                        print(f"Endpoint {i}: {endpoint.get('method', 'N/A')} {endpoint.get('path', 'N/A')}")
                        print(f"  Components: {len(endpoint.get('components', []))}")
                        print(f"  Transformations: {len(endpoint.get('transformations', []))}")
                
                # Test meaningful components check
                has_meaningful = generator._has_meaningful_components(components)
                print(f"Has meaningful components: {has_meaningful}")
                
            except Exception as e:
                print(f"❌ Failed to parse response: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"❌ Validation failed: {message}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Testing fixed validation logic")
    print("=" * 50)
    
    test_fixed_validation()
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")
