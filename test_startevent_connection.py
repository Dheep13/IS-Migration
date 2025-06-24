#!/usr/bin/env python3
"""
Test the StartEvent connection fix.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_startevent_connection():
    """Test that StartEvent has proper outgoing connection."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        
        # Create a simple test components structure
        test_components = {
            "process_name": "Test StartEvent Connection",
            "description": "Test integration to verify StartEvent connections",
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
        
        print("🧪 Testing StartEvent Connection Fix")
        print("=" * 50)
        
        # Generate the iFlow files with dummy markdown content
        dummy_markdown = "# Test Integration\nThis is a test integration for StartEvent connection verification."
        result = generator._generate_iflow_files(test_components, "TestFlow_StartEventFix", dummy_markdown)
        xml_content = result.get("xml_content", "") if result else ""
        
        if xml_content:
            print("✅ iFlow XML generated successfully")
            
            # Check for StartEvent
            if 'id="StartEvent_2"' in xml_content:
                print("✅ StartEvent_2 found in XML")
                
                # Extract the StartEvent outgoing reference
                import re
                start_event_match = re.search(r'<bpmn2:startEvent id="StartEvent_2".*?<bpmn2:outgoing>(.*?)</bpmn2:outgoing>', xml_content, re.DOTALL)
                
                if start_event_match:
                    outgoing_flow = start_event_match.group(1)
                    print(f"✅ StartEvent outgoing flow: {outgoing_flow}")
                    
                    # Check if this flow exists in sequence flows
                    if f'id="{outgoing_flow}"' in xml_content:
                        print(f"✅ Sequence flow {outgoing_flow} exists in XML")
                        
                        # Extract the target of this flow
                        flow_match = re.search(f'<bpmn2:sequenceFlow id="{re.escape(outgoing_flow)}".*?targetRef="(.*?)"', xml_content)
                        if flow_match:
                            target_ref = flow_match.group(1)
                            print(f"✅ StartEvent connects to: {target_ref}")
                            
                            # Check if target component exists
                            if f'id="{target_ref}"' in xml_content:
                                print(f"✅ Target component {target_ref} exists in XML")
                                print("\n🎉 StartEvent connection is PROPERLY CONFIGURED!")
                                return True
                            else:
                                print(f"❌ Target component {target_ref} NOT found in XML")
                        else:
                            print(f"❌ Could not find target for flow {outgoing_flow}")
                    else:
                        print(f"❌ Sequence flow {outgoing_flow} NOT found in XML")
                        print("❌ StartEvent outgoing reference is BROKEN!")
                else:
                    print("❌ StartEvent outgoing flow not found")
            else:
                print("❌ StartEvent_2 not found in XML")
                
            # Save the test XML for inspection
            with open("test_startevent_connection.xml", "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"\n💾 Test XML saved to: test_startevent_connection.xml")
            
        else:
            print("❌ Failed to generate iFlow XML")
            return False
            
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🔧 Testing StartEvent Connection Fix")
    print("=" * 60)
    
    success = test_startevent_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 StartEvent connection test PASSED!")
        print("✅ The fix is working correctly")
        return 0
    else:
        print("⚠️ StartEvent connection test FAILED!")
        print("❌ The fix needs more work")
        return 1

if __name__ == "__main__":
    exit(main())
