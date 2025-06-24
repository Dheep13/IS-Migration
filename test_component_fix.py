#!/usr/bin/env python3
"""
Test the component fix for json_to_xml_converter.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_component_generation():
    """Test generating iFlow with the exact components from the user's JSON."""
    
    try:
        from bpmn_templates import TemplateBpmnGenerator
        
        # Use the exact components from the user's JSON
        test_components = {
            "endpoints": [
                {
                    "components": [
                        {
                            "type": "enricher",
                            "name": "Set Dynamic Properties",
                            "id": "content_modifier_1"
                        },
                        {
                            "type": "json_to_xml_converter",
                            "name": "Transform Subscription to Opportunity",
                            "id": "mapping_1"
                        },
                        {
                            "type": "request_reply",
                            "name": "Create Salesforce Opportunity",
                            "id": "salesforce_adapter_1"
                        }
                    ]
                }
            ]
        }
        
        # Generate iFlow
        generator = TemplateBpmnGenerator()
        iflow_xml = generator.generate_iflow_xml(test_components, "Stripe_Salesforce_iFlow")
        
        print("✅ iFlow generation successful")
        print(f"📄 Generated XML length: {len(iflow_xml)} characters")
        
        # Check for all expected components
        expected_components = [
            "content_modifier_1",
            "mapping_1", 
            "salesforce_adapter_1",
            "JsonToXmlConverter",
            "Enricher",
            "ExternalCall"
        ]
        
        missing_components = []
        found_components = []
        
        for component in expected_components:
            if component in iflow_xml:
                found_components.append(component)
                print(f"✅ Found: {component}")
            else:
                missing_components.append(component)
                print(f"❌ Missing: {component}")
        
        # Save to file for inspection
        with open("test_fixed_iflow.xml", "w", encoding="utf-8") as f:
            f.write(iflow_xml)
        
        print(f"\n💾 Saved test iFlow to test_fixed_iflow.xml")
        
        if not missing_components:
            print("\n🎉 All components found! The fix is working!")
            return True
        else:
            print(f"\n⚠️ Missing components: {missing_components}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🧪 Testing Component Fix for json_to_xml_converter")
    print("=" * 60)
    
    success = test_component_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Component fix test passed!")
    else:
        print("⚠️ Component fix test failed!")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
