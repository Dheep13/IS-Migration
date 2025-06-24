#!/usr/bin/env python3
"""
Test the actual problematic response with proper handling
"""

import os
import sys
import json
import re

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def analyze_actual_response():
    """Analyze the actual problematic response"""
    print("🔍 Analyzing actual problematic response...")
    
    # Read the actual problematic response
    with open("BoomiToIS-API/genai_debug/raw_analysis_response.txt", "r", encoding="utf-8") as f:
        actual_response = f.read()
    
    print(f"Response length: {len(actual_response)} characters")
    print(f"Response preview: {actual_response[:100]}...")
    print(f"Response ending: ...{actual_response[-100:]}")
    
    # Check for JSON braces
    start_brace = actual_response.find('{')
    end_brace = actual_response.rfind('}')
    
    print(f"First {{ at position: {start_brace}")
    print(f"Last }} at position: {end_brace}")
    
    if start_brace != -1 and end_brace != -1:
        json_part = actual_response[start_brace:end_brace + 1]
        print(f"Extracted JSON part length: {len(json_part)}")
        print(f"JSON part: {json_part}")
        
        try:
            parsed = json.loads(json_part)
            print(f"✅ Successfully parsed JSON!")
            print(f"Parsed structure: {json.dumps(parsed, indent=2)}")
        except Exception as e:
            print(f"❌ Failed to parse JSON: {e}")
            
            # Try to clean up the JSON
            print("\n🧹 Attempting to clean JSON...")
            
            # Remove escaped characters
            cleaned_json = json_part.replace('\\"', '"').replace('\\n', '\n')
            print(f"Cleaned JSON: {cleaned_json}")
            
            try:
                parsed = json.loads(cleaned_json)
                print(f"✅ Successfully parsed cleaned JSON!")
                print(f"Parsed structure: {json.dumps(parsed, indent=2)}")
            except Exception as e2:
                print(f"❌ Still failed to parse cleaned JSON: {e2}")
    else:
        print("❌ No JSON braces found")
        
        # Look for markdown code blocks
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', actual_response)
        if json_match:
            json_str = json_match.group(1).strip()
            print(f"Found JSON in markdown block: {json_str}")
            
            try:
                parsed = json.loads(json_str)
                print(f"✅ Successfully parsed markdown JSON!")
                print(f"Parsed structure: {json.dumps(parsed, indent=2)}")
            except Exception as e:
                print(f"❌ Failed to parse markdown JSON: {e}")
        else:
            print("❌ No markdown JSON blocks found")

def test_improved_validation():
    """Test an improved validation function"""
    print("\n🧪 Testing improved validation...")
    
    def improved_validate_response(response):
        """Improved validation that handles escaped characters"""
        try:
            import re, json
            
            # First, try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                # If no code blocks, look for JSON structure in the response
                # Find content between first { and last }
                start_brace = response.find('{')
                end_brace = response.rfind('}')
                
                if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                    json_str = response[start_brace:end_brace + 1]
                    
                    # Clean up escaped characters
                    json_str = json_str.replace('\\"', '"').replace('\\n', '\n')
                else:
                    json_str = response.strip()
            
            # Validate the JSON
            parsed_json = json.loads(json_str)
            
            # Check if it has the expected structure
            if not isinstance(parsed_json, dict):
                return False, "Response is not a valid JSON object"
                
            if "endpoints" not in parsed_json:
                return False, "JSON missing required 'endpoints' field"
                
            return True, "Valid JSON response"
            
        except Exception as e:
            return False, f"Invalid JSON format: {e}"
    
    # Test with the actual response
    with open("BoomiToIS-API/genai_debug/raw_analysis_response.txt", "r", encoding="utf-8") as f:
        actual_response = f.read()
    
    is_valid, message = improved_validate_response(actual_response)
    print(f"Improved validation result: {is_valid} - {message}")

if __name__ == "__main__":
    print("🚀 Analyzing actual problematic response")
    print("=" * 50)
    
    analyze_actual_response()
    test_improved_validation()
    
    print("\n" + "=" * 50)
    print("✅ Analysis completed!")
