#!/usr/bin/env python3
"""
Test iFlow generation with new templates.
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_iflow_generation():
    """Test generating an iFlow with new components."""
    
    try:
        from bpmn_templates import TemplateBpmnGenerator
        
        # Create test components
        test_components = {
            "endpoints": [
                {
                    "components": [
                        {
                            "type": "json_to_xml",
                            "name": "Convert JSON to XML",
                            "id": "json_converter_1"
                        },
                        {
                            "type": "content_enricher", 
                            "name": "Enrich Content",
                            "id": "enricher_1"
                        }
                    ]
                }
            ]
        }
        
        # Generate iFlow
        generator = TemplateBpmnGenerator()
        iflow_xml = generator.generate_iflow_xml(test_components, "Test_iFlow")
        
        print("✅ iFlow generation successful")
        print(f"📄 Generated XML length: {len(iflow_xml)} characters")
        
        # Save to file for inspection
        with open("test_generated_iflow.xml", "w", encoding="utf-8") as f:
            f.write(iflow_xml)
        
        print("💾 Saved test iFlow to test_generated_iflow.xml")
        
        # Basic validation - check if it contains expected elements
        if "<bpmn2:definitions" in iflow_xml and "</bpmn2:definitions>" in iflow_xml:
            print("✅ iFlow has proper BPMN structure")
        else:
            print("❌ iFlow missing BPMN structure")
            
        if "json_converter_1" in iflow_xml:
            print("✅ Custom component ID found in iFlow")
        else:
            print("❌ Custom component ID not found in iFlow")
            
        return True
        
    except Exception as e:
        print(f"❌ iFlow generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Testing iFlow Generation with New Templates...")
    
    if test_iflow_generation():
        print("\n🎉 iFlow generation test passed!")
        return 0
    else:
        print("\n⚠️ iFlow generation test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
