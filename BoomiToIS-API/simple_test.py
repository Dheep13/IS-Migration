#!/usr/bin/env python3
"""
Simple test for new templates.
"""

import sys
import os
import xml.etree.ElementTree as ET

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bpmn_templates import BpmnTemplates, ComponentPositionManager
    print("✅ Successfully imported templates")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_basic_template():
    """Test a basic template."""
    print("🧪 Testing basic template...")
    
    templates = BpmnTemplates()
    
    try:
        # Test operation mapping
        result = templates.operation_mapping_template(
            id="OpMapping_1",
            name="Test Operation Mapping",
            incoming_flow="Flow_In",
            outgoing_flow="Flow_Out"
        )
        
        print(f"✅ Operation mapping template generated")
        print(f"📄 Definition length: {len(result['definition'])} characters")
        print(f"🎨 Shape length: {len(result['shape'])} characters")
        
        # Test XML validity
        try:
            ET.fromstring(result["definition"])
            print("✅ Generated XML is valid")
        except ET.ParseError as e:
            print(f"❌ Generated XML is invalid: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Template generation failed: {e}")
        return False

def test_position_manager():
    """Test position manager."""
    print("🧪 Testing position manager...")
    
    try:
        position_manager = ComponentPositionManager()
        
        # Test basic positioning
        pos1 = position_manager.calculate_position("test_1", "activity")
        pos2 = position_manager.calculate_position("test_2", "activity")
        
        print(f"✅ Position 1: {pos1}")
        print(f"✅ Position 2: {pos2}")
        
        # Check spacing
        spacing = pos2["x"] - pos1["x"]
        expected_spacing = position_manager.component_spacing_x
        
        if spacing == expected_spacing:
            print(f"✅ Spacing is correct: {spacing}")
        else:
            print(f"❌ Spacing is incorrect: {spacing} != {expected_spacing}")
            
        return True
        
    except Exception as e:
        print(f"❌ Position manager test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Starting Simple Template Tests...")
    
    success = True
    
    # Test basic template
    if not test_basic_template():
        success = False
    
    # Test position manager
    if not test_position_manager():
        success = False
    
    if success:
        print("\n🎉 All simple tests passed!")
        return 0
    else:
        print("\n⚠️ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
