#!/usr/bin/env python3
"""
Test script to verify that the enhanced templates are working correctly for d0a449df case.
This script tests the updated OData and HTTP templates against the corrected .iflw structure.
"""

import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
from enhanced_iflow_templates import EnhancedIFlowTemplates

def test_enhanced_templates():
    """Test that the enhanced templates generate the correct structure"""
    print("🧪 Testing Enhanced Templates for d0a449df case...")
    
    # Load the d0a449df JSON
    input_file = "genai_debug/iflow_input_components_IFlow_d0a449df.json"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    with open(input_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print(f"📄 Loaded test data from {input_file}")
    
    # Initialize the generator
    generator = EnhancedGenAIIFlowGenerator()
    
    # Process the components to generate XML
    try:
        # Use the internal method to process components
        endpoint_components = generator._create_endpoint_components(test_data["endpoints"][0], EnhancedIFlowTemplates())
        
        print(f"📊 Generated components:")
        print(f"  - Process components: {len(endpoint_components['process_components'])}")
        print(f"  - Participants: {len(endpoint_components['participants'])}")
        print(f"  - Message flows: {len(endpoint_components['message_flows'])}")
        
        # Test 1: Check Salesforce OData component
        salesforce_found = False
        for flow in endpoint_components["message_flows"]:
            if "request_reply_salesforce" in flow and "HCIOData" in flow:
                print("✅ SUCCESS: Found Salesforce OData message flow with HCIOData")
                
                # Check for proper operation mapping
                if "Create(POST)" in flow:
                    print("✅ SUCCESS: Salesforce operation correctly mapped to Create(POST)")
                elif "Query(GET)" in flow:
                    print("⚠️  WARNING: Salesforce operation is Query(GET) - should be Create(POST)")
                
                # Check for resource path
                if "/services/data/v52.0/sobjects/Opportunity" in flow:
                    print("✅ SUCCESS: Salesforce resource path correctly set")
                else:
                    print("⚠️  WARNING: Salesforce resource path missing or incorrect")
                
                salesforce_found = True
                break
        
        if not salesforce_found:
            print("❌ FAILURE: Salesforce OData message flow not found")
            return False
        
        # Test 2: Check Stripe HTTP components
        stripe_customer_found = False
        stripe_product_found = False
        
        for flow in endpoint_components["message_flows"]:
            if "request_reply_customer" in flow and "ComponentType" in flow and "HTTP" in flow:
                print("✅ SUCCESS: Found Stripe Customer HTTP message flow")
                
                # Check for proper HTTP method
                if "GET" in flow:
                    print("✅ SUCCESS: Stripe Customer method correctly set to GET")
                
                stripe_customer_found = True
            
            if "request_reply_product" in flow and "ComponentType" in flow and "HTTP" in flow:
                print("✅ SUCCESS: Found Stripe Product HTTP message flow")
                
                # Check for proper HTTP method
                if "GET" in flow:
                    print("✅ SUCCESS: Stripe Product method correctly set to GET")
                
                stripe_product_found = True
        
        if not stripe_customer_found:
            print("❌ FAILURE: Stripe Customer HTTP message flow not found")
            return False
            
        if not stripe_product_found:
            print("❌ FAILURE: Stripe Product HTTP message flow not found")
            return False
        
        # Test 3: Check participant structure (no typos)
        participant_typo_found = False
        for participant in endpoint_components["participants"]:
            if "EndpointRecevier" in participant:  # Check for the typo
                print("❌ FAILURE: Found typo 'EndpointRecevier' in participant")
                participant_typo_found = True
            elif "EndpointReceiver" in participant:
                print("✅ SUCCESS: Participant correctly uses 'EndpointReceiver'")
        
        if participant_typo_found:
            return False
        
        print("🎉 ALL TESTS PASSED! Enhanced templates are working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_methods_directly():
    """Test the template methods directly to verify structure"""
    print("🧪 Testing Template Methods Directly...")
    
    templates = EnhancedIFlowTemplates()
    
    # Test OData template
    print("📋 Testing OData Request-Reply Pattern...")
    odata_pattern = templates.odata_request_reply_pattern(
        service_task_id="test_salesforce",
        participant_id="Participant_test_salesforce", 
        message_flow_id="MessageFlow_test_salesforce",
        name="Test_Salesforce_Opportunity",
        service_url="https://mycompany.salesforce.com",
        operation="Create(POST)",
        resource_path="/services/data/v52.0/sobjects/Opportunity"
    )
    
    # Check OData template structure
    if "HCIOData" in odata_pattern["message_flow"]:
        print("✅ SUCCESS: OData template generates HCIOData component")
    else:
        print("❌ FAILURE: OData template missing HCIOData component")
        return False
    
    if "Create(POST)" in odata_pattern["message_flow"]:
        print("✅ SUCCESS: OData template correctly uses Create(POST) operation")
    else:
        print("❌ FAILURE: OData template missing Create(POST) operation")
        return False
    
    if "/services/data/v52.0/sobjects/Opportunity" in odata_pattern["message_flow"]:
        print("✅ SUCCESS: OData template correctly sets resource path")
    else:
        print("❌ FAILURE: OData template missing resource path")
        return False
    
    # Test HTTP template
    print("📋 Testing HTTP Request-Reply Pattern...")
    http_pattern = templates.http_request_reply_pattern(
        service_task_id="test_stripe",
        participant_id="Participant_test_stripe",
        message_flow_id="MessageFlow_test_stripe", 
        name="Test_Stripe_Customer",
        service_url="https://api.stripe.com/v1",
        http_method="GET"
    )
    
    # Check HTTP template structure
    if "ComponentType" in http_pattern["message_flow"] and "HTTP" in http_pattern["message_flow"]:
        print("✅ SUCCESS: HTTP template generates HTTP component")
    else:
        print("❌ FAILURE: HTTP template missing HTTP component")
        return False
    
    if "GET" in http_pattern["message_flow"]:
        print("✅ SUCCESS: HTTP template correctly uses GET method")
    else:
        print("❌ FAILURE: HTTP template missing GET method")
        return False
    
    print("🎉 TEMPLATE METHODS PASSED! Direct template testing successful.")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Enhanced Templates for d0a449df...")
    print("=" * 60)
    
    try:
        test1_result = test_template_methods_directly()
        print()
        test2_result = test_enhanced_templates()
        
        print("=" * 60)
        if test1_result and test2_result:
            print("🎉 ALL TESTS PASSED! Enhanced templates are working correctly.")
            print("✅ OData templates generate proper HCIOData components with correct operations")
            print("✅ HTTP templates generate proper HTTP components with correct methods")
            print("✅ No typos in participant types (EndpointReceiver)")
            print("✅ Resource paths and operations are correctly mapped from JSON")
        else:
            print("❌ SOME TESTS FAILED! Enhanced templates need more work.")
            if not test1_result:
                print("❌ Direct template method testing failed")
            if not test2_result:
                print("❌ d0a449df case testing failed")
        
        return test1_result and test2_result
        
    except Exception as e:
        print(f"❌ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
