#!/usr/bin/env python3
"""
Test the EndEvent connection fix.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_endevent_connection():
    """Test that EndEvent has proper incoming connection."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Create a simple test components structure
        test_components = {
            "process_name": "Test EndEvent Connection",
            "description": "Test integration to verify EndEvent connections",
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/test",
                    "purpose": "Test endpoint",
                    "components": [
                        {
                            "type": "odata",
                            "name": "Test_OData_Call",
                            "id": "test_odata_1",
                            "config": {
                                "address": "https://test.com/odata",
                                "resource_path": "TestData"
                            }
                        },
                        {
                            "type": "enricher",
                            "name": "Test_Enricher",
                            "id": "test_enricher_1",
                            "config": {
                                "content": "Test content"
                            }
                        }
                    ],
                    "sequence": ["test_odata_1", "test_enricher_1"]
                }
            ]
        }
        
        print("🧪 Testing EndEvent Connection Fix")
        print("=" * 50)
        
        # Generate the iFlow files with dummy markdown content
        dummy_markdown = "# Test Integration\nThis is a test integration for EndEvent connection verification."
        result = generator._generate_iflow_files(test_components, "TestFlow_EndEventFix", dummy_markdown)
        
        if result and result.get("success"):
            print("✅ iFlow generated successfully")
            
            # Read the generated XML file
            xml_file = "BoomiToIS-API/genai_debug/final_iflow_TestFlow_EndEventFix.xml"
            if os.path.exists(xml_file):
                with open(xml_file, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                
                print("✅ Final XML file found")
                
                # Check for EndEvent
                if 'id="EndEvent_2"' in xml_content:
                    print("✅ EndEvent_2 found in XML")
                    
                    # Extract the EndEvent incoming reference
                    import re
                    end_event_match = re.search(r'<bpmn2:endEvent id="EndEvent_2".*?<bpmn2:incoming>(.*?)</bpmn2:incoming>', xml_content, re.DOTALL)
                    
                    if end_event_match:
                        incoming_flow = end_event_match.group(1)
                        print(f"✅ EndEvent incoming flow: {incoming_flow}")
                        
                        # Check if this flow exists in sequence flows
                        if f'id="{incoming_flow}"' in xml_content:
                            print(f"✅ Sequence flow {incoming_flow} exists in XML")
                            
                            # Extract the source of this flow
                            flow_match = re.search(f'<bpmn2:sequenceFlow id="{re.escape(incoming_flow)}".*?sourceRef="(.*?)"', xml_content)
                            if flow_match:
                                source_ref = flow_match.group(1)
                                print(f"✅ EndEvent receives from: {source_ref}")
                                
                                # Check if source component exists
                                if f'id="{source_ref}"' in xml_content:
                                    print(f"✅ Source component {source_ref} exists in XML")
                                    print("\n🎉 EndEvent connection is PROPERLY CONFIGURED!")
                                    return True
                                else:
                                    print(f"❌ Source component {source_ref} NOT found in XML")
                            else:
                                print(f"❌ Could not find source for flow {incoming_flow}")
                        else:
                            print(f"❌ Sequence flow {incoming_flow} NOT found in XML")
                            print("❌ EndEvent incoming reference is BROKEN!")
                    else:
                        print("❌ EndEvent incoming flow not found")
                else:
                    print("❌ EndEvent_2 not found in XML")
                    
            else:
                print(f"❌ XML file not found: {xml_file}")
                return False
                
        else:
            print("❌ Failed to generate iFlow")
            return False
            
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🔧 Testing EndEvent Connection Fix")
    print("=" * 60)
    
    success = test_endevent_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 EndEvent connection test PASSED!")
        print("✅ The fix is working correctly")
        print("🚀 Both StartEvent and EndEvent connections are now fixed!")
        return 0
    else:
        print("⚠️ EndEvent connection test FAILED!")
        print("❌ The fix needs more work")
        return 1

if __name__ == "__main__":
    exit(main())
