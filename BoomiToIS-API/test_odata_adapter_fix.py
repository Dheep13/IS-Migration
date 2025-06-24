#!/usr/bin/env python3
"""
Test script to verify that the OData adapter fix is working correctly.
This script tests the request_reply component with odata_adapter receiver.
"""

import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
from enhanced_iflow_templates import EnhancedIFlowTemplates

def test_odata_adapter_detection():
    """Test that request_reply components with odata_adapter are properly detected and processed"""
    print("🧪 Testing OData adapter detection and processing...")
    
    # Create test data with request_reply component with odata_adapter (the fixed case)
    test_data = {
        "process_name": "Test OData Process",
        "endpoints": [
            {
                "method": "POST",
                "path": "/test-odata",
                "components": [
                    {
                        "type": "request_reply",
                        "name": "Create_Salesforce_Opportunity",
                        "id": "create_opportunity",
                        "receiver_adapter": {
                            "type": "odata_adapter",
                            "operation": "POST",
                            "endpoint": "/services/data/v53.0/sobjects/Opportunity",
                            "connection": "salesforce_odata_connection"
                        },
                        "config": {
                            "endpoint_path": "/services/data/v53.0/sobjects/Opportunity",
                            "method": "POST",
                            "address": "https://mycompany.salesforce.com",
                            "resource_path": "services/data/v53.0/sobjects/Opportunity"
                        }
                    }
                ]
            }
        ]
    }
    
    # Initialize the generator and templates
    generator = EnhancedGenAIIFlowGenerator()
    templates = EnhancedIFlowTemplates()

    # Process the components to generate XML
    try:
        # Use the internal method to process components
        endpoint_components = generator._create_endpoint_components(test_data["endpoints"][0], templates)
        
        # Check if we have message flows
        if endpoint_components["message_flows"]:
            message_flow = endpoint_components["message_flows"][0]
            print(f"📄 Generated message flow:")
            print(message_flow[:500] + "..." if len(message_flow) > 500 else message_flow)
            
            # Check for HCIOData component type
            if "HCIOData" in message_flow:
                print("✅ SUCCESS: Message flow contains HCIOData component type")
                return True
            elif "HTTP" in message_flow and "HCIOData" not in message_flow:
                print("❌ FAILURE: Message flow contains HTTP instead of HCIOData")
                print("This means the odata_adapter receiver is not being properly detected")
                return False
            else:
                print("⚠️  UNKNOWN: Message flow doesn't contain expected component types")
                return False
        else:
            print("❌ FAILURE: No message flows generated")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_c0c2ca94_case_regeneration():
    """Test regenerating the c0c2ca94 case with the fix"""
    print("🧪 Testing c0c2ca94 case regeneration...")
    
    # Load the c0c2ca94 JSON
    input_file = "genai_debug/iflow_input_components_IFlow_c0c2ca94.json"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    with open(input_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print(f"📄 Loaded test data from {input_file}")
    
    # Initialize the generator and templates
    generator = EnhancedGenAIIFlowGenerator()
    templates = EnhancedIFlowTemplates()

    # Process the components to generate XML
    try:
        # Use the internal method to process components
        endpoint_components = generator._create_endpoint_components(test_data["endpoints"][0], templates)
        
        # Find the Salesforce message flow
        salesforce_flow = None
        for flow in endpoint_components["message_flows"]:
            if "create_opportunity" in flow or "Salesforce" in flow:
                salesforce_flow = flow
                break
        
        if salesforce_flow:
            print(f"📄 Found Salesforce message flow:")
            print(salesforce_flow[:800] + "..." if len(salesforce_flow) > 800 else salesforce_flow)
            
            # Check for HCIOData component type
            if "HCIOData" in salesforce_flow:
                print("✅ SUCCESS: Salesforce message flow now contains HCIOData component type")
                print("🎉 The odata_adapter fix is working!")
                return True
            elif "HTTP" in salesforce_flow and "HCIOData" not in salesforce_flow:
                print("❌ FAILURE: Salesforce message flow still contains HTTP instead of HCIOData")
                print("The odata_adapter receiver is still not being properly detected")
                return False
            else:
                print("⚠️  UNKNOWN: Salesforce message flow doesn't contain expected component types")
                return False
        else:
            print("❌ FAILURE: No Salesforce message flow found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Testing OData adapter fix...")
    print("=" * 60)
    
    try:
        test1_result = test_odata_adapter_detection()
        print()
        test2_result = test_c0c2ca94_case_regeneration()
        
        print("=" * 60)
        if test1_result and test2_result:
            print("🎉 ALL TESTS PASSED! The OData adapter fix is working correctly.")
            print("✅ request_reply components with odata_adapter now generate HCIOData message flows")
            print("✅ Salesforce operations will now use proper OData adapters instead of HTTP")
        else:
            print("❌ SOME TESTS FAILED! The OData adapter fix needs more work.")
            if not test1_result:
                print("❌ Basic OData adapter detection failed")
            if not test2_result:
                print("❌ c0c2ca94 case regeneration failed")
        
        return test1_result and test2_result
        
    except Exception as e:
        print(f"❌ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
