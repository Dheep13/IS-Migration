#!/usr/bin/env python3
"""
Analyze and potentially fix JSON responses from LLM attempts.
This script can identify common JSON issues and fix them programmatically.
"""

import json
import re
import os
from pathlib import Path

def analyze_json_file(file_path):
    """Analyze a JSON file and identify issues."""
    print(f"\n🔍 Analyzing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as-is
        try:
            parsed = json.loads(content)
            print("✅ JSON is already valid!")
            return True, content, parsed, []
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return False, content, None, [str(e)]
            
    except Exception as e:
        print(f"💥 File reading failed: {e}")
        return False, "", None, [str(e)]

def fix_common_json_issues(content):
    """Fix common JSON issues programmatically."""
    print("🔧 Attempting to fix common JSON issues...")
    
    fixes_applied = []
    original_content = content
    
    # Fix 1: Unescaped newlines in strings
    def fix_newlines(match):
        string_content = match.group(1)
        fixed_content = string_content.replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')
        return f'"{fixed_content}"'
    
    # Pattern to find strings with unescaped newlines
    newline_pattern = r'"([^"]*(?:\n|\t|\r)[^"]*)"'
    if re.search(newline_pattern, content, re.DOTALL):
        content = re.sub(newline_pattern, fix_newlines, content, flags=re.DOTALL)
        fixes_applied.append("Fixed unescaped newlines in strings")
    
    # Fix 2: Trailing commas
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    if content != original_content:
        fixes_applied.append("Removed trailing commas")
    
    # Fix 3: Single quotes to double quotes (for property names)
    content = re.sub(r"'([^']+)':", r'"\1":', content)
    if "Fixed single quotes" not in fixes_applied and content != original_content:
        fixes_applied.append("Fixed single quotes to double quotes")
    
    # Fix 4: Unescaped quotes in strings
    def fix_quotes(match):
        string_content = match.group(1)
        fixed_content = string_content.replace('"', '\\"')
        return f'"{fixed_content}"'
    
    # This is tricky - we need to be careful not to break valid JSON
    # For now, let's skip this as it's complex
    
    # Fix 5: Remove any non-JSON content before/after
    # Find the first { and last }
    first_brace = content.find('{')
    last_brace = content.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_only = content[first_brace:last_brace + 1]
        if json_only != content:
            content = json_only
            fixes_applied.append("Extracted JSON from mixed content")
    
    return content, fixes_applied

def test_json_fix(content):
    """Test if the fixed content is valid JSON."""
    try:
        parsed = json.loads(content)
        return True, parsed
    except json.JSONDecodeError as e:
        return False, str(e)

def create_json_fixer_function():
    """Create a reusable JSON fixer function for the main system."""
    
    fixer_code = '''
def fix_llm_json_response(response_text):
    """
    Programmatically fix common JSON issues in LLM responses.
    
    Args:
        response_text (str): Raw LLM response
        
    Returns:
        tuple: (is_fixed, fixed_json_str, parsed_json, fixes_applied)
    """
    import json
    import re
    
    fixes_applied = []
    content = response_text.strip()
    
    # Extract JSON from markdown code blocks
    json_match = re.search(r'```(?:json)?\\s*([\\s\\S]*?)\\s*```', content)
    if json_match:
        content = json_match.group(1).strip()
        fixes_applied.append("Extracted JSON from markdown code block")
    
    # Find JSON boundaries
    first_brace = content.find('{')
    last_brace = content.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        content = content[first_brace:last_brace + 1]
        if first_brace > 0 or last_brace < len(response_text.strip()) - 1:
            fixes_applied.append("Extracted JSON from mixed content")
    
    # Fix unescaped newlines in strings
    def fix_newlines(match):
        string_content = match.group(1)
        fixed_content = string_content.replace('\\n', '\\\\n').replace('\\t', '\\\\t').replace('\\r', '\\\\r')
        return f'"{fixed_content}"'
    
    newline_pattern = r'"([^"]*(?:\\n|\\t|\\r)[^"]*)"'
    if re.search(newline_pattern, content, re.DOTALL):
        content = re.sub(newline_pattern, fix_newlines, content, flags=re.DOTALL)
        fixes_applied.append("Fixed unescaped newlines in strings")
    
    # Remove trailing commas
    original_content = content
    content = re.sub(r',(\\s*[}\\]])', r'\\1', content)
    if content != original_content:
        fixes_applied.append("Removed trailing commas")
    
    # Fix single quotes to double quotes for property names
    content = re.sub(r"'([^']+)':", r'"\\1":', content)
    
    # Test if fixed
    try:
        parsed = json.loads(content)
        return True, content, parsed, fixes_applied
    except json.JSONDecodeError as e:
        return False, content, None, fixes_applied + [f"Still invalid: {e}"]
'''
    
    return fixer_code

def main():
    """Main analysis function."""
    print("🧪 Analyzing Recent LLM JSON Responses")
    print("=" * 50)
    
    # Find all attempt files
    debug_dir = Path("BoomiToIS-API/genai_debug")
    attempt_files = list(debug_dir.glob("*attempt*.txt"))
    
    if not attempt_files:
        print("❌ No attempt files found!")
        return 1
    
    print(f"📁 Found {len(attempt_files)} attempt files")
    
    valid_count = 0
    fixable_count = 0
    unfixable_count = 0
    
    for file_path in sorted(attempt_files):
        is_valid, content, parsed, errors = analyze_json_file(file_path)
        
        if is_valid:
            valid_count += 1
            print(f"   ✅ Already valid: {file_path.name}")
        else:
            # Try to fix
            fixed_content, fixes = fix_common_json_issues(content)
            is_fixed, parsed_or_error = test_json_fix(fixed_content)
            
            if is_fixed:
                fixable_count += 1
                print(f"   🔧 Fixable: {file_path.name}")
                print(f"      Fixes applied: {', '.join(fixes)}")
                
                # Save fixed version
                fixed_file = file_path.with_suffix('.fixed.json')
                with open(fixed_file, 'w', encoding='utf-8') as f:
                    json.dump(parsed_or_error, f, indent=2)
                print(f"      💾 Saved fixed version: {fixed_file.name}")
            else:
                unfixable_count += 1
                print(f"   ❌ Unfixable: {file_path.name}")
                print(f"      Error: {parsed_or_error}")
    
    print("\n" + "=" * 50)
    print(f"📊 Analysis Summary:")
    print(f"   ✅ Already valid: {valid_count}")
    print(f"   🔧 Fixable: {fixable_count}")
    print(f"   ❌ Unfixable: {unfixable_count}")
    print(f"   📁 Total analyzed: {len(attempt_files)}")
    
    # Generate the fixer function
    fixer_code = create_json_fixer_function()
    with open("json_fixer_function.py", "w", encoding="utf-8") as f:
        f.write(fixer_code)
    print(f"\n💾 Generated reusable fixer function: json_fixer_function.py")
    
    if fixable_count > 0:
        print(f"\n🎯 Recommendation: Integrate the JSON fixer into the main system")
        print(f"   This could avoid {fixable_count}/{len(attempt_files)} LLM retry attempts!")
        return 0
    elif valid_count == len(attempt_files):
        print(f"\n🎉 All JSON responses are already valid!")
        print(f"   The issue might be in the validation logic, not the JSON itself.")
        return 0
    else:
        print(f"\n⚠️ Some JSON responses have unfixable issues.")
        return 1

if __name__ == "__main__":
    exit(main())
