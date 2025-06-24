#!/usr/bin/env python3
"""
Test the improved GenAI prompt for proper error handling and branching.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_improved_prompt():
    """Test the improved GenAI prompt structure."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Create generator instance
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Test markdown content that includes error handling
        test_markdown = """
        # SAP SuccessFactors to SFTP Integration with Error Handling
        
        ## Process Flow
        
        ### Main Process Steps:
        1. **Set Process Properties** - Sets dynamic process properties
           - Error Path: Send error notification email if properties fail to set
        2. **Query SuccessFactors** - Retrieves employee data
        3. **Transform Data** - Maps employee data to canonical format
        4. **Upload to SFTP** - Transfers data to SFTP server
        
        ### Error Handling:
        - **Error Notification**: Sends email when errors occur
        - **Retry Logic**: Retries SFTP upload up to 3 times
        - **Success Logging**: Logs successful transfers
        
        ### Branching Logic:
        - **Branch 1**: Active employees → SFTP upload
        - **Branch 2**: Terminated employees → Kafka notification
        - **Branch 3**: Contractors → Different SFTP directory
        """
        
        # Test the prompt creation
        prompt = generator._create_detailed_analysis_prompt(test_markdown)
        
        print("✅ Prompt created successfully")
        print(f"📄 Prompt length: {len(prompt)} characters")
        
        # Check if the prompt contains the new error handling instructions
        error_handling_checks = [
            "error_handling",
            "exception_subprocess", 
            "branching",
            "CRITICAL ERROR HANDLING RULES",
            "error-path",
            "try-path",
            "Main \"sequence\" array = happy path components only"
        ]
        
        found_instructions = []
        missing_instructions = []
        
        for check in error_handling_checks:
            if check in prompt:
                found_instructions.append(check)
                print(f"✅ Found: {check}")
            else:
                missing_instructions.append(check)
                print(f"❌ Missing: {check}")
        
        # Test the more explicit prompt as well
        explicit_prompt = generator._create_more_explicit_prompt(test_markdown, "Test error")
        
        print(f"\n📄 Explicit prompt length: {len(explicit_prompt)} characters")
        
        if not missing_instructions:
            print("\n🎉 All error handling instructions found in prompt!")
            return True
        else:
            print(f"\n⚠️ Missing instructions: {missing_instructions}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_structure():
    """Test that the prompt has the correct JSON structure."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        prompt = generator._create_detailed_analysis_prompt("Test content")
        
        # Check for the new JSON structure elements
        structure_checks = [
            '"error_handling": {',
            '"exception_subprocess": [',
            '"branching": {',
            '"type": "parallel or exclusive',  # Partial match
            '"trigger": "What triggers this error handler'  # Partial match
        ]
        
        found_structures = []
        missing_structures = []
        
        for check in structure_checks:
            if check in prompt:
                found_structures.append(check)
                print(f"✅ Found structure: {check}")
            else:
                missing_structures.append(check)
                print(f"❌ Missing structure: {check}")
        
        if not missing_structures:
            print("\n🎉 All JSON structure elements found!")
            return True
        else:
            print(f"\n⚠️ Missing structures: {missing_structures}")
            return False
            
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing Improved GenAI Prompt for Error Handling")
    print("=" * 60)
    
    success1 = test_improved_prompt()
    print("\n" + "-" * 40)
    success2 = test_prompt_structure()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All prompt improvement tests passed!")
        print("✅ GenAI should now properly handle:")
        print("   - Boomi error paths → Exception subprocesses")
        print("   - Boomi try-catch → Main sequence + error handling")
        print("   - Boomi branching → Parallel/Exclusive gateways")
        print("   - Proper separation of happy path vs error components")
        return 0
    else:
        print("⚠️ Some prompt improvement tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
