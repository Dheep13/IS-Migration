#!/usr/bin/env python3
"""
Debug JSON extraction step by step
"""

import re
import json

def debug_json_extraction():
    """Debug the JSON extraction process"""
    print("🔍 Debugging JSON extraction...")
    
    # Read the actual problematic response
    with open("BoomiToIS-API/genai_debug/raw_analysis_response.txt", "r", encoding="utf-8") as f:
        response = f.read()
    
    print(f"Response length: {len(response)} characters")
    print(f"Response type: {type(response)}")
    
    # Step 1: Check for markdown code blocks
    print("\n📝 Step 1: Checking for markdown code blocks...")
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
    if json_match:
        json_str = json_match.group(1).strip()
        print(f"Found markdown JSON block: {len(json_str)} characters")
        print(f"JSON content: {json_str[:200]}...")
    else:
        print("No markdown code blocks found")
        
        # Step 2: Look for JSON end pattern
        print("\n🔚 Step 2: Looking for JSON end pattern...")
        json_end_pattern = r'}\s*]\s*}\s*```?$'
        json_end_match = re.search(json_end_pattern, response)
        
        if json_end_match:
            print(f"Found JSON end pattern at position {json_end_match.start()}-{json_end_match.end()}")
            print(f"End pattern: {repr(json_end_match.group())}")
            
            # Step 3: Work backwards to find JSON start
            print("\n⬅️ Step 3: Working backwards to find JSON start...")
            end_pos = json_end_match.start() + len(json_end_match.group().rstrip('`').rstrip())
            print(f"End position: {end_pos}")
            
            # Get the content up to the end position
            content_to_end = response[:end_pos]
            print(f"Content to end length: {len(content_to_end)}")
            print(f"Last 200 chars: ...{content_to_end[-200:]}")
            
            # Look for the opening brace that starts the JSON structure
            lines = content_to_end.split('\n')
            print(f"Number of lines: {len(lines)}")
            
            json_lines = []
            brace_count = 0
            found_closing = False
            
            for i, line in enumerate(reversed(lines)):
                json_lines.insert(0, line)
                line_num = len(lines) - i - 1
                
                # Count braces to find the matching opening brace
                for char_pos, char in enumerate(reversed(line)):
                    if char == '}':
                        brace_count += 1
                        found_closing = True
                        print(f"Found '}}' at line {line_num}, char {len(line) - char_pos - 1}, brace_count: {brace_count}")
                    elif char == '{':
                        brace_count -= 1
                        print(f"Found '{{' at line {line_num}, char {len(line) - char_pos - 1}, brace_count: {brace_count}")
                        if found_closing and brace_count == 0:
                            # Found the matching opening brace
                            json_str = '\n'.join(json_lines)
                            print(f"✅ Found complete JSON structure! Length: {len(json_str)}")
                            print(f"JSON start: {json_str[:100]}...")
                            print(f"JSON end: ...{json_str[-100:]}")
                            break
                
                if found_closing and brace_count == 0:
                    break
                    
                # Safety check - don't process too many lines
                if i > 50:
                    print("⚠️ Processed 50 lines, stopping to avoid infinite loop")
                    break
            
            if found_closing and brace_count == 0:
                # Step 4: Clean up and parse JSON
                print("\n🧹 Step 4: Cleaning up and parsing JSON...")
                
                # Clean up any escaped characters
                cleaned_json = json_str.replace('\\"', '"').replace('\\n', '\n')
                print(f"Cleaned JSON length: {len(cleaned_json)}")
                print(f"Cleaned JSON start: {cleaned_json[:100]}...")
                
                try:
                    parsed_json = json.loads(cleaned_json)
                    print(f"✅ Successfully parsed JSON!")
                    print(f"JSON keys: {list(parsed_json.keys())}")
                    
                    if isinstance(parsed_json, dict) and "endpoints" in parsed_json:
                        print(f"✅ Valid structure with endpoints!")
                        print(f"Number of endpoints: {len(parsed_json['endpoints'])}")
                    else:
                        print(f"❌ Invalid structure or missing endpoints")
                        
                except Exception as e:
                    print(f"❌ Failed to parse cleaned JSON: {e}")
                    print(f"JSON content that failed: {repr(cleaned_json[:500])}")
            else:
                print(f"❌ Could not find matching braces. Final brace_count: {brace_count}")
        else:
            print("No JSON end pattern found")
            
            # Step 5: Fallback - simple brace search
            print("\n🔍 Step 5: Fallback - simple brace search...")
            start_brace = response.find('{')
            end_brace = response.rfind('}')
            
            print(f"First '{{' at position: {start_brace}")
            print(f"Last '}}' at position: {end_brace}")
            
            if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                json_str = response[start_brace:end_brace + 1]
                print(f"Extracted JSON length: {len(json_str)}")
                print(f"JSON start: {json_str[:100]}...")
                print(f"JSON end: ...{json_str[-100:]}")
                
                # Clean and try to parse
                cleaned_json = json_str.replace('\\"', '"').replace('\\n', '\n')
                try:
                    parsed_json = json.loads(cleaned_json)
                    print(f"✅ Successfully parsed fallback JSON!")
                    print(f"JSON keys: {list(parsed_json.keys())}")
                except Exception as e:
                    print(f"❌ Failed to parse fallback JSON: {e}")
            else:
                print("❌ No valid brace positions found")

if __name__ == "__main__":
    print("🚀 Debugging JSON extraction")
    print("=" * 50)
    
    debug_json_extraction()
    
    print("\n" + "=" * 50)
    print("✅ Debug completed!")
