#!/usr/bin/env python3
"""
Test the validation logic to see why it's failing on valid JSON.
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_validation_with_actual_files():
    """Test validation logic with the actual attempt files."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Test with the actual attempt files
        attempt_files = [
            "BoomiToIS-API/genai_debug/raw_analysis_response_attempt1.txt",
            "BoomiToIS-API/genai_debug/raw_analysis_response_attempt2.txt"
        ]
        
        for file_path in attempt_files:
            if os.path.exists(file_path):
                print(f"\n🔍 Testing validation with: {file_path}")
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"📄 Content length: {len(content)} characters")
                print(f"📄 First 100 chars: {repr(content[:100])}")
                
                # Test direct JSON parsing
                try:
                    parsed = json.loads(content)
                    print("✅ Direct JSON parsing: SUCCESS")
                    print(f"📊 Parsed type: {type(parsed)}")
                    if isinstance(parsed, dict):
                        print(f"📊 Keys: {list(parsed.keys())}")
                        if "endpoints" in parsed:
                            print(f"📊 Endpoints count: {len(parsed['endpoints'])}")
                except json.JSONDecodeError as e:
                    print(f"❌ Direct JSON parsing: FAILED - {e}")
                    print(f"📍 Error at line {e.lineno}, column {e.colno}")
                    
                    # Show the problematic line
                    lines = content.split('\n')
                    if e.lineno <= len(lines):
                        problem_line = lines[e.lineno - 1]
                        print(f"📍 Problem line {e.lineno}: {repr(problem_line)}")
                        if e.colno <= len(problem_line):
                            print(f"📍 Problem character: {repr(problem_line[e.colno-1:e.colno+10])}")
                
                # Test the validation function
                is_valid, message = generator._validate_genai_response(content)
                print(f"🔍 Validation function result: {is_valid}")
                print(f"🔍 Validation message: {message}")
                
                if not is_valid:
                    print("❌ Validation failed even though JSON might be valid!")
                    
                    # Let's debug the validation function step by step
                    print("\n🔧 Debugging validation function...")
                    
                    # Step 1: Check for markdown code blocks
                    import re
                    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
                    if json_match:
                        print("📋 Found markdown code block")
                        json_str = json_match.group(1).strip()
                    else:
                        print("📋 No markdown code block found, using fallback logic")
                        
                        # Check the fallback logic
                        start_brace = content.find('{')
                        end_brace = content.rfind('}')
                        print(f"📋 First brace at: {start_brace}")
                        print(f"📋 Last brace at: {end_brace}")
                        
                        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                            json_str = content[start_brace:end_brace + 1]
                            print(f"📋 Extracted JSON length: {len(json_str)}")
                        else:
                            json_str = content.strip()
                            print("📋 Using full content as JSON")
                    
                    # Step 2: Test the cleaning logic
                    print("\n🧹 Testing JSON cleaning logic...")
                    
                    def fix_newlines(match):
                        content_part = match.group(1)
                        fixed_content = content_part.replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')
                        return f'"{fixed_content}"'
                    
                    pattern = r'"([^"]*(?:\n|\t|\r)[^"]*)"'
                    original_json_str = json_str
                    json_str = re.sub(pattern, fix_newlines, json_str, flags=re.DOTALL)
                    
                    if json_str != original_json_str:
                        print("🧹 JSON cleaning applied changes")
                        print(f"🧹 Original length: {len(original_json_str)}")
                        print(f"🧹 Cleaned length: {len(json_str)}")
                    else:
                        print("🧹 No cleaning changes needed")
                    
                    # Step 3: Test final parsing
                    try:
                        final_parsed = json.loads(json_str)
                        print("✅ Final parsing after cleaning: SUCCESS")
                        
                        # Check structure requirements
                        if not isinstance(final_parsed, dict):
                            print("❌ Not a dict")
                        elif "endpoints" not in final_parsed:
                            print("❌ Missing 'endpoints' field")
                        else:
                            print("✅ All structure checks passed")
                            print("🤔 Validation should have succeeded!")
                            
                    except json.JSONDecodeError as e2:
                        print(f"❌ Final parsing failed: {e2}")
                        print(f"📍 Error at line {e2.lineno}, column {e2.colno}")
                
                print("\n" + "="*50)
            else:
                print(f"❌ File not found: {file_path}")
                
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🧪 Testing Validation Logic")
    print("=" * 40)
    
    test_validation_with_actual_files()
    
    return 0

if __name__ == "__main__":
    exit(main())
