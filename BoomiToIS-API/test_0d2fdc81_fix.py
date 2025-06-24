#!/usr/bin/env python3
"""
Test script to verify that the 0d2fdc81 case is fixed.
This script loads the actual 0d2fdc81 JSON and applies the fix.
"""

import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator

def test_0d2fdc81_case():
    """Test the actual 0d2fdc81 case that had the problem"""
    print("🧪 Testing the actual 0d2fdc81 case...")
    
    # Load the original problematic JSON
    input_file = "genai_debug/iflow_input_components_IFlow_0d2fdc81.json"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    print(f"📄 Loaded original data from {input_file}")
    
    # Check the original problem
    original_component = original_data["endpoints"][0]["components"][1]  # The odata component
    print(f"🔍 Original component type: {original_component['type']}")
    print(f"🔍 Original component name: {original_component['name']}")
    
    if original_component["type"] == "odata":
        print("✅ Confirmed: Original has standalone 'odata' component (the problem)")
    else:
        print(f"⚠️  Original component type is '{original_component['type']}', not 'odata'")
    
    # Apply the fix
    generator = EnhancedGenAIIFlowGenerator()
    fixed_data = generator.validate_and_fix_components(original_data)
    
    # Check the fixed result
    fixed_component = fixed_data["endpoints"][0]["components"][1]
    print(f"🔧 Fixed component type: {fixed_component['type']}")
    print(f"🔧 Fixed component name: {fixed_component['name']}")
    
    # Verify the fix
    assert fixed_component["type"] == "request_reply", f"Expected 'request_reply', got '{fixed_component['type']}'"
    assert "receiver_adapter" in fixed_component, "Missing receiver_adapter"
    assert fixed_component["receiver_adapter"]["type"] == "odata_adapter", "Wrong receiver_adapter type"
    
    print("✅ 0d2fdc81 case successfully fixed!")
    print(f"✅ Component now has receiver_adapter: {fixed_component['receiver_adapter']}")
    
    # Save the fixed version
    output_file = "genai_debug/iflow_input_components_IFlow_0d2fdc81_FIXED.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2)
    
    print(f"💾 Saved fixed version to {output_file}")
    
    return True

def main():
    """Run the test"""
    print("🚀 Testing the actual 0d2fdc81 case fix...")
    print("=" * 60)
    
    try:
        success = test_0d2fdc81_case()
        
        if success:
            print("=" * 60)
            print("🎉 SUCCESS! The 0d2fdc81 case has been fixed.")
            print("✅ The standalone 'odata' component is now 'request_reply' with receiver_adapter")
            print("✅ This will generate proper iFlow XML with OData receiver adapter")
        
        return success
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
