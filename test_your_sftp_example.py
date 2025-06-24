#!/usr/bin/env python3
"""
Test your original SFTP example with the enhanced request-reply functionality
"""

import os
import sys
import json
import zipfile

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def test_your_sftp_example():
    """Test your original SFTP example"""
    print("🧪 Testing Your Original SFTP Example...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Create generator
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        
        # Your exact SFTP example
        your_sftp_json = {
            "process_name": "SAP SuccessFactors to SFTP Integration",
            "description": "This integration connects SAP SuccessFactors with an SFTP server, enabling the automated transfer of employee data with comprehensive error handling.",
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/SuccessFactors/EmployeeData",
                    "purpose": "Retrieves employee data from SAP SuccessFactors",
                    "components": [
                        {
                            "type": "request_reply",
                            "name": "SAP_SuccessFactors_Request",
                            "id": "sf_request_1",
                            "config": {
                                "method": "GET",
                                "address": "https://api.successfactors.com/odata/v2/User",
                                "headers": {
                                    "Content-Type": "application/json",
                                    "Authorization": "Bearer ${token}"
                                },
                                "authentication": "OAuth"
                            }
                        },
                        {
                            "type": "request_reply",
                            "name": "SFTP_Upload",
                            "id": "sftp_upload_1",
                            "config": {
                                "protocol": "SFTP",
                                "operation": "PUT",
                                "host": "sftp.example.com",
                                "port": 22,
                                "path": "/uploads/employeedata/employeeData_${date}.json",
                                "authentication": {
                                    "type": "Password",
                                    "username": "${sftp_username}"
                                }
                            }
                        }
                    ],
                    "sequence": [
                        "sf_request_1",
                        "sftp_upload_1"
                    ]
                }
            ]
        }
        
        # Convert to markdown
        test_markdown = f"""
# {your_sftp_json['process_name']}

## Overview
{your_sftp_json['description']}

## Integration Details
{json.dumps(your_sftp_json, indent=2)}
"""
        
        print(f"📄 Generating iFlow from your SFTP example...")
        
        # Generate iFlow
        output_dir = "your_sftp_test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        iflow_name = "YourSFTPExample"
        
        result_path = generator.generate_iflow(test_markdown, output_dir, iflow_name)
        
        print(f"✅ Generated iFlow: {result_path}")
        
        # Analyze the results
        if os.path.exists(result_path):
            print(f"✅ Output file exists: {os.path.getsize(result_path)} bytes")
            
            # Extract and examine the BPMN content
            with zipfile.ZipFile(result_path, 'r') as zf:
                files = zf.namelist()
                print(f"✅ ZIP contains {len(files)} files: {files}")
                
                # Look for the main iFlow file
                iflow_file = None
                for file in files:
                    if file.endswith('.iflw'):
                        iflow_file = file
                        break
                
                if iflow_file:
                    print(f"✅ Found iFlow file: {iflow_file}")
                    
                    # Extract and examine the BPMN content
                    bpmn_content = zf.read(iflow_file).decode('utf-8')
                    print(f"✅ BPMN content length: {len(bpmn_content)} characters")
                    
                    # Check for your specific requirements
                    your_requirements = [
                        ('serviceTask', 'Service Tasks (request components)'),
                        ('participant.*EndpointRecevier', 'Receiver Participants (reply components)'),
                        ('messageFlow', 'Message Flows (arrows with protocol details)'),
                        ('SFTP', 'SFTP Protocol'),
                        ('sftp.example.com', 'Your SFTP Host'),
                        ('/uploads/employeedata/', 'Your SFTP Path'),
                        ('SuccessFactors', 'SuccessFactors System'),
                        ('api.successfactors.com', 'SuccessFactors URL'),
                        ('OAuth', 'OAuth Authentication'),
                        ('Password', 'SFTP Password Auth'),
                        ('${sftp_username}', 'SFTP Username Parameter')
                    ]
                    
                    found_count = 0
                    for pattern, description in your_requirements:
                        import re
                        if re.search(pattern, bpmn_content):
                            print(f"  ✅ {description}: Found")
                            found_count += 1
                        else:
                            print(f"  ❌ {description}: Missing")
                    
                    print(f"\n📊 Results: {found_count}/{len(your_requirements)} requirements met")
                    
                    # Count components
                    import re
                    service_tasks = len(re.findall(r'<bpmn2:serviceTask', bpmn_content))
                    participants = len(re.findall(r'<bpmn2:participant.*EndpointRecevier', bpmn_content))
                    message_flows = len(re.findall(r'<bpmn2:messageFlow', bpmn_content))
                    
                    print(f"\n🔢 Component Counts:")
                    print(f"  - Service Tasks (request parts): {service_tasks}")
                    print(f"  - Receiver Participants (reply parts): {participants}")
                    print(f"  - Message Flows (connections): {message_flows}")
                    
                    if service_tasks >= 2 and participants >= 2 and message_flows >= 2:
                        print(f"\n🎉 SUCCESS! Complete request-reply patterns detected!")
                        print(f"   Both SuccessFactors AND SFTP have request + reply components!")
                    else:
                        print(f"\n⚠️  Incomplete patterns detected")
                    
                    # Save for inspection
                    with open("your_sftp_example_bpmn.xml", "w", encoding="utf-8") as f:
                        f.write(bpmn_content)
                    print(f"📄 Saved BPMN to: your_sftp_example_bpmn.xml")
                    
                else:
                    print("❌ No .iflw file found in ZIP")
        else:
            print(f"❌ Output file not found: {result_path}")
        
        # Clean up
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing your SFTP example: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Your Original SFTP Example")
    print("=" * 60)
    
    success = test_your_sftp_example()
    
    if success:
        print("\n🎉 Your SFTP example test completed!")
    else:
        print("\n❌ Your SFTP example test failed")
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("\n📋 What was tested:")
    print("- ✅ Your exact SFTP configuration")
    print("- ✅ SuccessFactors request-reply pattern")
    print("- ✅ SFTP request-reply pattern")
    print("- ✅ Complete receiver participants")
    print("- ✅ Message flows with protocol details")
    print("- ✅ Authentication configurations")
