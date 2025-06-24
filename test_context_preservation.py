#!/usr/bin/env python3
"""
Test that context is preserved across retry attempts.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_context_preservation():
    """Test that retry attempts include full context."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Test markdown content
        test_markdown = """
        # SAP SuccessFactors to SFTP Integration
        
        ## Process Flow
        1. **Query SuccessFactors** - OData call to get employee data
        2. **Transform Data** - Map to canonical format
        3. **Upload to SFTP** - Transfer files
        
        ## Error Handling
        - Email notifications on failure
        - Retry logic for SFTP uploads
        """
        
        # Test first attempt prompt
        detailed_prompt = generator._create_detailed_analysis_prompt(test_markdown)
        print("✅ Detailed prompt created")
        print(f"📄 Detailed prompt length: {len(detailed_prompt)} characters")
        
        # Test retry attempt prompt
        retry_prompt = generator._create_more_explicit_prompt(test_markdown, "Invalid JSON format: control character")
        print("✅ Retry prompt created")
        print(f"📄 Retry prompt length: {len(retry_prompt)} characters")
        
        # Check that retry prompt includes critical context
        critical_context_checks = [
            "CRITICAL REQUIREMENTS FOR BOOMI TO SAP CONVERSION",
            "BOOMI ERROR HANDLING AND BRANCHING PATTERNS",
            "error_handling",
            "exception_subprocess",
            "EXAMPLE BOOMI TO SAP CONVERSION",
            "OData components in SAP Integration Suite",
            "Boomi Connector",  # More flexible match
            "Boomi Map"         # More flexible match
        ]
        
        found_in_detailed = []
        found_in_retry = []
        missing_in_retry = []
        
        for check in critical_context_checks:
            if check in detailed_prompt:
                found_in_detailed.append(check)
            
            if check in retry_prompt:
                found_in_retry.append(check)
            else:
                missing_in_retry.append(check)
        
        print(f"\n📊 Context Analysis:")
        print(f"   Detailed prompt has {len(found_in_detailed)}/{len(critical_context_checks)} context elements")
        print(f"   Retry prompt has {len(found_in_retry)}/{len(critical_context_checks)} context elements")
        
        if missing_in_retry:
            print(f"\n❌ Missing context in retry prompt:")
            for missing in missing_in_retry:
                print(f"   - {missing}")
            return False
        else:
            print(f"\n✅ All critical context preserved in retry prompt!")
            
        # Check that error context is added
        error_context_checks = [
            "The previous attempt failed with error",
            "THIS IS A RETRY ATTEMPT",
            "MANDATORY JSON ESCAPING RULES",
            "Fix the JSON escaping issue"
        ]
        
        found_error_context = []
        for check in error_context_checks:
            if check in retry_prompt:
                found_error_context.append(check)
        
        print(f"\n📊 Error Context Analysis:")
        print(f"   Found {len(found_error_context)}/{len(error_context_checks)} error context elements")
        
        if len(found_error_context) == len(error_context_checks):
            print("✅ All error context properly added!")
            return True
        else:
            print("❌ Some error context missing!")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_size_comparison():
    """Test that retry prompts are similar in size to detailed prompts."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        test_markdown = "Test content"
        
        detailed_prompt = generator._create_detailed_analysis_prompt(test_markdown)
        retry_prompt = generator._create_more_explicit_prompt(test_markdown, "Test error")
        
        detailed_size = len(detailed_prompt)
        retry_size = len(retry_prompt)
        
        print(f"📊 Prompt Size Comparison:")
        print(f"   Detailed prompt: {detailed_size:,} characters")
        print(f"   Retry prompt: {retry_size:,} characters")
        print(f"   Ratio: {retry_size/detailed_size:.2f}")
        
        # Retry prompt should be larger (detailed + error context)
        if retry_size > detailed_size:
            print("✅ Retry prompt is larger (includes error context)")
            return True
        else:
            print("❌ Retry prompt is smaller (context may be missing)")
            return False
            
    except Exception as e:
        print(f"❌ Size comparison test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing Context Preservation in Retry Attempts")
    print("=" * 60)
    
    success1 = test_context_preservation()
    print("\n" + "-" * 40)
    success2 = test_prompt_size_comparison()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All context preservation tests passed!")
        print("✅ Retry attempts now include:")
        print("   - Full Boomi conversion rules")
        print("   - Complete error handling patterns")
        print("   - All OData and Salesforce examples")
        print("   - Previous error context for fixing")
        print("   - Enhanced JSON escaping instructions")
        return 0
    else:
        print("⚠️ Some context preservation tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
