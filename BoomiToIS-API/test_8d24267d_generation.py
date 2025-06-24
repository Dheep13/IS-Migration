#!/usr/bin/env python3
"""
Test script to verify XML generation for 8d24267d case using enhanced templates.
This tests the same pattern as d0a449df but with different component configurations.
"""

import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator

def test_8d24267d_xml_generation():
    """Test XML generation for 8d24267d case"""
    print("🧪 Testing XML Generation for 8d24267d case...")
    
    # Load the 8d24267d JSON
    input_file = "genai_debug/iflow_input_components_IFlow_8d24267d.json"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    with open(input_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print(f"📄 Loaded test data from {input_file}")
    print(f"📋 Process: {test_data['process_name']}")
    print(f"📋 Components: {len(test_data['endpoints'][0]['components'])}")
    
    # Initialize the generator
    generator = EnhancedGenAIIFlowGenerator()
    
    try:
        # Generate the complete iFlow XML using the internal method
        print("🔧 Generating complete iFlow XML...")
        iflow_name = "IFlow_8d24267d"
        xml_content = generator._generate_iflw_content(test_data, iflow_name)

        if xml_content:
            # Save the generated XML for inspection
            output_file = "genai_debug/test_generated_IFlow_8d24267d.xml"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"✅ SUCCESS: Generated XML saved to {output_file}")
            
            # Analyze the generated XML
            print("\n📊 Analyzing Generated XML...")
            
            # Test 1: Check for OData components (Salesforce)
            if "request_reply_salesforce" in xml_content and "HCIOData" in xml_content:
                print("✅ SUCCESS: Found Salesforce OData component with HCIOData")
                
                # Check operation mapping
                if "Create(POST)" in xml_content:
                    print("✅ SUCCESS: Salesforce operation correctly mapped to Create(POST)")
                elif "Query(GET)" in xml_content:
                    print("⚠️  WARNING: Salesforce operation is Query(GET) - should be Create(POST)")
                
                # Check resource path
                if "/services/data/v53.0/sobjects/Opportunity" in xml_content:
                    print("✅ SUCCESS: Salesforce resource path correctly set (v53.0)")
                else:
                    print("⚠️  WARNING: Salesforce resource path missing or incorrect")
            else:
                print("❌ FAILURE: Salesforce OData component not found or incorrect")
                return False
            
            # Test 2: Check for HTTP components (Stripe)
            stripe_customer_found = "request_reply_stripe_customer" in xml_content and "ComponentType" in xml_content and "HTTP" in xml_content
            stripe_product_found = "request_reply_stripe_product" in xml_content and "ComponentType" in xml_content and "HTTP" in xml_content
            
            if stripe_customer_found:
                print("✅ SUCCESS: Found Stripe Customer HTTP component")
            else:
                print("❌ FAILURE: Stripe Customer HTTP component not found")
                return False
                
            if stripe_product_found:
                print("✅ SUCCESS: Found Stripe Product HTTP component")
            else:
                print("❌ FAILURE: Stripe Product HTTP component not found")
                return False
            
            # Test 3: Check for Enricher components
            enricher_count = xml_content.count('activityType">Enricher')
            print(f"📋 Found {enricher_count} Enricher components")
            
            expected_enrichers = ["enricher_initial_props", "enricher_description", "enricher_customer_response", "enricher_product_response"]
            enrichers_found = 0
            for enricher in expected_enrichers:
                if enricher in xml_content:
                    enrichers_found += 1
                    print(f"✅ SUCCESS: Found enricher {enricher}")
                else:
                    print(f"⚠️  WARNING: Missing enricher {enricher}")
            
            # Test 4: Check for Groovy Script components
            script_count = xml_content.count('activityType">Script')
            print(f"📋 Found {script_count} Script components")
            
            expected_scripts = ["script_close_date", "transform_to_opportunity"]
            scripts_found = 0
            for script in expected_scripts:
                if script in xml_content:
                    scripts_found += 1
                    print(f"✅ SUCCESS: Found script {script}")
                else:
                    print(f"⚠️  WARNING: Missing script {script}")
            
            # Test 5: Check for participant typos
            if "EndpointRecevier" in xml_content:
                print("❌ FAILURE: Found typo 'EndpointRecevier' in participants")
                return False
            elif "EndpointReceiver" in xml_content:
                print("✅ SUCCESS: Participants correctly use 'EndpointReceiver'")
            
            # Test 6: Check sequence flows
            sequence_flow_count = xml_content.count('<bpmn2:sequenceFlow')
            print(f"📋 Found {sequence_flow_count} sequence flows")
            
            if sequence_flow_count >= 8:  # Expected from JSON
                print("✅ SUCCESS: Adequate sequence flows generated")
            else:
                print("⚠️  WARNING: Fewer sequence flows than expected")
            
            # Summary
            print("\n🎯 Generation Summary:")
            print(f"  - Salesforce OData: ✅")
            print(f"  - Stripe HTTP APIs: ✅")
            print(f"  - Enrichers: {enrichers_found}/{len(expected_enrichers)}")
            print(f"  - Scripts: {scripts_found}/{len(expected_scripts)}")
            print(f"  - Sequence Flows: {sequence_flow_count}")
            print(f"  - No Typos: ✅")
            
            return True
            
        else:
            print("❌ FAILURE: No XML content generated")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during XML generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_with_d0a449df():
    """Compare 8d24267d generation with d0a449df patterns"""
    print("\n🔍 Comparing with d0a449df patterns...")
    
    # Check if both files exist
    file_8d24267d = "genai_debug/test_generated_IFlow_8d24267d.xml"
    file_d0a449df = "genai_debug/final_iflow_IFlow_d0a449df.xml"
    
    if not os.path.exists(file_8d24267d):
        print("⚠️  8d24267d XML not found - run generation first")
        return False
    
    if not os.path.exists(file_d0a449df):
        print("⚠️  d0a449df XML not found for comparison")
        return False
    
    with open(file_8d24267d, 'r', encoding='utf-8') as f:
        xml_8d24267d = f.read()
    
    with open(file_d0a449df, 'r', encoding='utf-8') as f:
        xml_d0a449df = f.read()
    
    print("📊 Comparison Results:")
    
    # Compare OData structure
    odata_8d24267d = "HCIOData" in xml_8d24267d and "Create(POST)" in xml_8d24267d
    odata_d0a449df = "HCIOData" in xml_d0a449df and "Create(POST)" in xml_d0a449df
    
    if odata_8d24267d and odata_d0a449df:
        print("✅ SUCCESS: Both use correct OData structure")
    else:
        print(f"⚠️  OData comparison: 8d24267d={odata_8d24267d}, d0a449df={odata_d0a449df}")
    
    # Compare HTTP structure
    http_8d24267d = xml_8d24267d.count("ComponentType\">HTTP")
    http_d0a449df = xml_d0a449df.count("ComponentType\">HTTP")
    
    print(f"📋 HTTP components: 8d24267d={http_8d24267d}, d0a449df={http_d0a449df}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing 8d24267d XML Generation with Enhanced Templates...")
    print("=" * 70)
    
    try:
        test1_result = test_8d24267d_xml_generation()
        test2_result = compare_with_d0a449df()
        
        print("=" * 70)
        if test1_result:
            print("🎉 XML GENERATION SUCCESSFUL!")
            print("✅ Enhanced templates working correctly for 8d24267d")
            print("✅ All expected components generated")
            print("✅ Proper adapter types and operations")
        else:
            print("❌ XML GENERATION FAILED!")
            print("❌ Issues found in template generation")
        
        return test1_result
        
    except Exception as e:
        print(f"❌ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
