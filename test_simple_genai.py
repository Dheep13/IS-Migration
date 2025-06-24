#!/usr/bin/env python3
"""
Simple test to verify GenAI improvements.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_prompt_improvements():
    """Test that the prompt improvements are in place."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Test the prompt creation
        test_content = "Test markdown content"
        prompt = generator._create_detailed_analysis_prompt(test_content)
        
        print("✅ Prompt created successfully")
        print(f"📄 Prompt length: {len(prompt)} characters")
        
        # Check for key improvements
        improvements = [
            "CRITICAL JSON FORMATTING RULES",
            "ALL strings must be properly escaped",
            "NO unescaped control characters",
            "Example: \"script\": \"line1\\\\nline2\\\\nline3\"",
            "error_handling",
            "exception_subprocess"
        ]
        
        found_improvements = []
        missing_improvements = []
        
        for improvement in improvements:
            if improvement in prompt:
                found_improvements.append(improvement)
                print(f"✅ Found: {improvement}")
            else:
                missing_improvements.append(improvement)
                print(f"❌ Missing: {improvement}")
        
        # Test explicit prompt
        explicit_prompt = generator._create_more_explicit_prompt(test_content, "Test error")
        print(f"\n📄 Explicit prompt length: {len(explicit_prompt)} characters")
        
        if not missing_improvements:
            print("\n🎉 All prompt improvements found!")
            return True
        else:
            print(f"\n⚠️ Missing improvements: {missing_improvements}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_max_retries():
    """Test that max_retries is increased."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Check the method signature
        import inspect
        sig = inspect.signature(generator._analyze_with_genai)
        max_retries_param = sig.parameters.get('max_retries')
        
        if max_retries_param and max_retries_param.default == 5:
            print("✅ max_retries increased to 5")
            return True
        else:
            print(f"❌ max_retries not set correctly: {max_retries_param.default if max_retries_param else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ Max retries test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing GenAI Improvements")
    print("=" * 40)
    
    success1 = test_prompt_improvements()
    print("\n" + "-" * 40)
    success2 = test_max_retries()
    
    print("\n" + "=" * 40)
    if success1 and success2:
        print("🎉 All GenAI improvement tests passed!")
        print("✅ Ready to generate proper JSON with:")
        print("   - Enhanced JSON escaping rules")
        print("   - 5 retry attempts")
        print("   - No fallback (fail if invalid)")
        print("   - Better error handling prompts")
        return 0
    else:
        print("⚠️ Some GenAI improvement tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
