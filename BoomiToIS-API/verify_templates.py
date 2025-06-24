#!/usr/bin/env python3
"""
Verify that new templates are working correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from bpmn_templates import BpmnTemplates, ComponentPositionManager
        
        print("✅ Import successful")
        
        # Test templates
        templates = BpmnTemplates()
        print("✅ BpmnTemplates instantiated")
        
        # Test position manager
        position_manager = ComponentPositionManager()
        print("✅ ComponentPositionManager instantiated")
        
        # Test a new template
        result = templates.operation_mapping_template(
            id="test", 
            name="test", 
            incoming_flow="in", 
            outgoing_flow="out"
        )
        print("✅ Operation mapping template works")
        print(f"📄 Generated {len(result['definition'])} chars of XML")
        
        # Test position calculation
        pos = position_manager.calculate_position("test_comp", "activity")
        print(f"✅ Position calculation works: {pos}")
        
        print("\n🎉 All verification tests passed!")
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
