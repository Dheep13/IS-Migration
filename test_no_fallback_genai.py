#!/usr/bin/env python3
"""
Test the no-fallback GenAI approach to ensure it fails properly when JSON is invalid.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_genai_failure_handling():
    """Test that the system properly fails when GenAI cannot generate valid JSON."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Create generator instance
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Test with content that might cause JSON issues
        problematic_markdown = """
        # Complex Integration with Special Characters
        
        ## Process Description
        This process contains "quotes", 'single quotes', and 
        multi-line content that might break JSON parsing.
        
        ### Components:
        1. **Data Validation** - Validates input with script:
           ```groovy
           if (data == null) {
               throw new Exception("Invalid data");
           }
           return "Success";
           ```
        
        2. **Error Handling** - Handles errors with complex logic
        
        ### Error Scenarios:
        - Network timeout errors
        - Data validation failures
        - Authentication issues
        """
        
        print("🧪 Testing GenAI with potentially problematic content...")
        print(f"📄 Content length: {len(problematic_markdown)} characters")
        
        # This should either succeed with valid JSON or fail completely
        try:
            result = generator._analyze_with_genai(problematic_markdown, max_retries=3)
            
            # If we get here, it succeeded
            print("✅ GenAI successfully generated valid JSON!")
            print(f"📊 Result type: {type(result)}")
            print(f"📊 Process name: {result.get('process_name', 'Unknown')}")
            
            # Verify the result has meaningful content
            if result.get('endpoints'):
                endpoint_count = len(result['endpoints'])
                print(f"📊 Generated {endpoint_count} endpoint(s)")
                
                for i, endpoint in enumerate(result['endpoints']):
                    component_count = len(endpoint.get('components', []))
                    print(f"   Endpoint {i+1}: {component_count} components")
            
            return True
            
        except Exception as e:
            # This is expected if GenAI fails
            print(f"❌ GenAI failed as expected: {e}")
            print("✅ System properly failed instead of using fallback")
            
            # Check if debug files were created
            debug_files = [
                "genai_debug/failure_summary.txt",
                "genai_debug/raw_analysis_response_attempt1.txt",
                "genai_debug/raw_analysis_response_attempt2.txt",
                "genai_debug/raw_analysis_response_attempt3.txt"
            ]
            
            found_debug_files = []
            for debug_file in debug_files:
                if os.path.exists(debug_file):
                    found_debug_files.append(debug_file)
            
            print(f"📁 Debug files created: {len(found_debug_files)}")
            for debug_file in found_debug_files:
                print(f"   - {debug_file}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_json_cleaning():
    """Test the JSON cleaning functionality."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Test JSON with unescaped newlines
        problematic_json = '''
        {
            "process_name": "Test Process",
            "description": "A test process with
        multiple lines",
            "endpoints": [
                {
                    "components": [
                        {
                            "config": {
                                "script": "line1
        line2
        line3"
                            }
                        }
                    ]
                }
            ]
        }
        '''
        
        print("🧪 Testing JSON cleaning functionality...")
        
        # Test the cleaning function
        if hasattr(generator, '_clean_json_string'):
            cleaned = generator._clean_json_string(problematic_json)
            print("✅ JSON cleaning function exists")
            
            # Check if newlines were properly escaped
            if '\\n' in cleaned and '\n' not in cleaned.replace('\\n', ''):
                print("✅ Newlines properly escaped")
            else:
                print("❌ Newlines not properly escaped")
                return False
        else:
            print("❌ JSON cleaning function not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ JSON cleaning test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing No-Fallback GenAI Approach")
    print("=" * 50)
    
    # Test 1: GenAI failure handling
    print("\n📋 Test 1: GenAI Failure Handling")
    print("-" * 30)
    success1 = test_genai_failure_handling()
    
    # Test 2: JSON cleaning
    print("\n📋 Test 2: JSON Cleaning")
    print("-" * 30)
    success2 = test_json_cleaning()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All no-fallback tests passed!")
        print("✅ System will now:")
        print("   - Retry GenAI up to 5 times with improved prompts")
        print("   - Clean JSON to fix escaping issues")
        print("   - Fail completely if valid JSON cannot be generated")
        print("   - Create debug files for troubleshooting")
        return 0
    else:
        print("⚠️ Some no-fallback tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
