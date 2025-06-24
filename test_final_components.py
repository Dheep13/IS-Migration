#!/usr/bin/env python3
"""
Test the final components that were successfully parsed
"""

import os
import sys
import json

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def test_final_components():
    """Test the final components that were parsed"""
    print("🧪 Testing Final Components Processing...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Load the final components that were successfully parsed
        with open('BoomiToIS-API/genai_debug/final_components.json', 'r') as f:
            final_components = json.load(f)
        
        print(f"📄 Loaded final components: {final_components['process_name']}")
        
        # Create generator
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        
        # Test the component processing directly
        endpoint = final_components['endpoints'][0]
        
        print(f"🔄 Processing endpoint with {len(endpoint['components'])} components...")
        
        # Call the component creation method directly
        endpoint_components = generator._create_endpoint_components(endpoint, generator.templates)
        
        print(f"\n✅ Endpoint components result:")
        print(f"  - Process components: {len(endpoint_components.get('process_components', []))}")
        print(f"  - Participants: {len(endpoint_components.get('participants', []))}")
        print(f"  - Message flows: {len(endpoint_components.get('message_flows', []))}")
        print(f"  - Sequence flows: {len(endpoint_components.get('sequence_flows', []))}")
        
        # Check for specific components
        all_content = str(endpoint_components)
        
        # Check for SuccessFactors components
        sf_indicators = [
            "SuccessFactors",
            "successfactors_request_1",
            "OAuth",
            "EndpointRecevier"
        ]
        
        print(f"\n🔍 SuccessFactors indicators:")
        sf_found = 0
        for indicator in sf_indicators:
            found = indicator in all_content
            print(f"  {'✅' if found else '❌'} {indicator}: {'Found' if found else 'Missing'}")
            if found:
                sf_found += 1
        
        # Check for SFTP components  
        sftp_indicators = [
            "SFTP",
            "sftp_upload_1",
            "EndpointRecevier"
        ]
        
        print(f"\n🔍 SFTP indicators:")
        sftp_found = 0
        for indicator in sftp_indicators:
            found = indicator in all_content
            print(f"  {'✅' if found else '❌'} {indicator}: {'Found' if found else 'Missing'}")
            if found:
                sftp_found += 1
        
        # Summary
        print(f"\n📊 Results:")
        print(f"  - SuccessFactors components: {sf_found}/{len(sf_indicators)}")
        print(f"  - SFTP components: {sftp_found}/{len(sftp_indicators)}")
        
        if sf_found >= 3 and sftp_found >= 2:
            print(f"\n🎉 SUCCESS! Both SuccessFactors and SFTP request-reply patterns detected!")
        else:
            print(f"\n⚠️  Some components may be missing")
        
        # Show actual components generated
        if endpoint_components.get('participants'):
            print(f"\n👥 Generated Participants:")
            for i, part in enumerate(endpoint_components['participants']):
                print(f"  {i+1}. {part[:100]}...")
        
        if endpoint_components.get('message_flows'):
            print(f"\n🔗 Generated Message Flows:")
            for i, flow in enumerate(endpoint_components['message_flows']):
                print(f"  {i+1}. {flow[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing final components: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Final Components Processing")
    print("=" * 50)
    
    success = test_final_components()
    
    if success:
        print("\n🎉 Final components processing test completed!")
    else:
        print("\n❌ Final components processing test failed")
    
    print("\n" + "=" * 50)
