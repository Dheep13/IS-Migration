#!/usr/bin/env python3
"""
Debug the component processing to see why request_reply components aren't being generated
"""

import os
import sys
import json

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def debug_component_processing():
    """Debug component processing step by step"""
    print("🔍 Debugging Component Processing...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        from bpmn_templates import BpmnTemplates
        
        # Create generator
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        templates = BpmnTemplates()
        
        # Simple test endpoint with SFTP request_reply
        test_endpoint = {
            "method": "GET",
            "path": "/test",
            "purpose": "Test SFTP",
            "components": [
                {
                    "type": "request_reply",
                    "name": "SFTP_Upload_Test",
                    "id": "sftp_test_1",
                    "config": {
                        "protocol": "SFTP",
                        "operation": "PUT",
                        "host": "sftp.example.com",
                        "port": 22,
                        "path": "/uploads/test.json",
                        "authentication": {
                            "type": "Password",
                            "username": "${sftp_username}"
                        }
                    }
                }
            ],
            "sequence": ["sftp_test_1"]
        }
        
        print("📄 Test endpoint:")
        print(json.dumps(test_endpoint, indent=2))
        
        print("\n🔄 Calling _create_endpoint_components...")
        
        # Call the component creation method directly
        endpoint_components = generator._create_endpoint_components(test_endpoint, templates)
        
        print(f"\n✅ Endpoint components result:")
        print(f"  - Process components: {len(endpoint_components.get('process_components', []))}")
        print(f"  - Participants: {len(endpoint_components.get('participants', []))}")
        print(f"  - Message flows: {len(endpoint_components.get('message_flows', []))}")
        print(f"  - Sequence flows: {len(endpoint_components.get('sequence_flows', []))}")
        
        # Print the actual components
        if endpoint_components.get('process_components'):
            print(f"\n📋 Process components:")
            for i, comp in enumerate(endpoint_components['process_components']):
                print(f"  {i+1}. {comp[:100]}...")
        
        if endpoint_components.get('participants'):
            print(f"\n👥 Participants:")
            for i, part in enumerate(endpoint_components['participants']):
                print(f"  {i+1}. {part[:100]}...")
        
        if endpoint_components.get('message_flows'):
            print(f"\n🔗 Message flows:")
            for i, flow in enumerate(endpoint_components['message_flows']):
                print(f"  {i+1}. {flow[:100]}...")
        
        # Check if SFTP-specific content is present
        all_content = str(endpoint_components)
        sftp_indicators = [
            "SFTP",
            "sftp.example.com",
            "/uploads/test.json",
            "Password",
            "${sftp_username}",
            "EndpointRecevier"
        ]
        
        print(f"\n🔍 SFTP indicators found:")
        for indicator in sftp_indicators:
            found = indicator in all_content
            print(f"  {'✅' if found else '❌'} {indicator}: {'Found' if found else 'Missing'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in component processing debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Debugging Component Processing")
    print("=" * 50)
    
    success = debug_component_processing()
    
    if success:
        print("\n🎉 Component processing debug completed!")
    else:
        print("\n❌ Component processing debug failed")
    
    print("\n" + "=" * 50)
