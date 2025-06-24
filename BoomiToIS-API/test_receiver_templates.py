#!/usr/bin/env python3
"""
Test script to verify that our updated receiver templates work correctly.
This will generate an iFlow from the Stripe-Salesforce JSON to test if receivers appear.
"""

import json
import sys
import os
from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator

def test_receiver_templates():
    """Test the updated receiver templates with Stripe-Salesforce integration"""
    
    print("🧪 Testing Updated Receiver Templates...")
    
    # Load the test JSON
    with open('test_stripe_salesforce.json', 'r') as f:
        test_components = json.load(f)
    
    print(f"✅ Loaded test components: {test_components['process_name']}")
    print(f"📊 Components to test: {len(test_components['endpoints'][0]['components'])}")
    
    # Count request_reply components
    request_reply_count = sum(1 for comp in test_components['endpoints'][0]['components'] 
                             if comp['type'] == 'request_reply')
    print(f"🔗 Request-reply components: {request_reply_count}")
    
    # Initialize generator
    generator = EnhancedGenAIIFlowGenerator(
        provider="claude",
        model="claude-3-7-sonnet-20250219"
    )
    
    # Generate iFlow
    iflow_name = "Test_Stripe_Salesforce_Receivers"
    print(f"\n🚀 Generating iFlow: {iflow_name}")
    
    try:
        # Generate the iFlow files directly from components using internal method
        result = generator._generate_iflow_files(test_components, iflow_name, "Test markdown content")

        if result:
            print("✅ iFlow generation successful!")
            print(f"📁 Generated files in: genai_debug/")
            print(f"📄 Final XML: genai_debug/final_iflow_{iflow_name}.xml")
            
            # Check if receivers were generated
            xml_file = f"genai_debug/final_iflow_{iflow_name}.xml"
            if os.path.exists(xml_file):
                with open(xml_file, 'r') as f:
                    xml_content = f.read()
                
                # Count participants and message flows (using SAP's typo: EndpointRecevier)
                participant_count = xml_content.count('ifl:type="EndpointRecevier"')  # Count participants by attribute
                message_flow_count = xml_content.count('<bpmn2:messageFlow')
                http_adapter_count = xml_content.count('<value>HTTP</value>')
                odata_adapter_count = xml_content.count('<value>HCIOData</value>')

                print(f"\n📊 Analysis Results:")
                print(f"   🎯 Receiver participants: {participant_count}")
                print(f"   🔗 Message flows: {message_flow_count}")
                print(f"   ✅ HTTP adapters: {http_adapter_count}")
                print(f"   ✅ OData adapters: {odata_adapter_count}")
                print(f"   ✅ SAP typo fix applied: {'EndpointRecevier' in xml_content}")

                if participant_count >= request_reply_count:
                    print("🎉 SUCCESS: All receivers generated correctly!")
                    print("🎯 Ready to import into SAP Integration Suite!")
                else:
                    print("❌ ISSUE: Missing receivers detected")
                    
        else:
            print("❌ iFlow generation failed!")
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_receiver_templates()
