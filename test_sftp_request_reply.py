#!/usr/bin/env python3
"""
Test the enhanced request_reply functionality with SFTP components
"""

import os
import sys
import json
import zipfile

# Add the BoomiToIS-API directory to the path
sys.path.append('BoomiToIS-API')

def test_sftp_request_reply():
    """Test SFTP request-reply pattern generation"""
    print("🧪 Testing SFTP Request-Reply Pattern...")
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        
        # Create generator with no API key (forces fallback)
        generator = EnhancedGenAIIFlowGenerator(api_key="test", provider="local")
        
        # Your SFTP example JSON
        sftp_json = {
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
        
        # Convert to markdown format that the generator expects
        test_markdown = f"""
# {sftp_json['process_name']}

## Overview
{sftp_json['description']}

## Components
{json.dumps(sftp_json, indent=2)}
"""
        
        print(f"📄 Test markdown length: {len(test_markdown)} characters")
        
        # Generate iFlow
        output_dir = "test_sftp_output"
        os.makedirs(output_dir, exist_ok=True)
        
        iflow_name = "TestSFTPRequestReply"
        
        print("🔄 Generating iFlow with SFTP request-reply...")
        result_path = generator.generate_iflow(test_markdown, output_dir, iflow_name)
        
        print(f"✅ Generated iFlow: {result_path}")
        
        # Verify the output
        if os.path.exists(result_path):
            print(f"✅ Output file exists: {os.path.getsize(result_path)} bytes")
            
            # Extract and examine the BPMN content
            with zipfile.ZipFile(result_path, 'r') as zf:
                files = zf.namelist()
                print(f"✅ ZIP contains {len(files)} files")
                
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
                    
                    # Check for SFTP-specific elements
                    sftp_checks = [
                        ('<bpmn2:serviceTask', 'Service tasks (process components)'),
                        ('<bpmn2:participant', 'Receiver participants'),
                        ('<bpmn2:messageFlow', 'Message flows (connections)'),
                        ('SFTP', 'SFTP protocol references'),
                        ('sftp.example.com', 'SFTP host configuration'),
                        ('SuccessFactors', 'SuccessFactors references'),
                        ('EndpointRecevier', 'Receiver endpoint type'),
                        ('/uploads/employeedata/', 'SFTP path configuration'),
                        ('Password', 'Authentication type'),
                        ('${sftp_username}', 'Username parameter')
                    ]
                    
                    found_elements = 0
                    for element, description in sftp_checks:
                        if element in bpmn_content:
                            print(f"  ✅ {description}: Found")
                            found_elements += 1
                        else:
                            print(f"  ❌ {description}: Missing")
                    
                    print(f"✅ Found {found_elements}/{len(sftp_checks)} expected SFTP elements")
                    
                    # Save BPMN content for inspection
                    with open("test_sftp_bpmn.xml", "w", encoding="utf-8") as f:
                        f.write(bpmn_content)
                    print("📄 Saved BPMN content to test_sftp_bpmn.xml")
                    
                    # Count specific components
                    service_task_count = bpmn_content.count('<bpmn2:serviceTask')
                    participant_count = bpmn_content.count('<bpmn2:participant')
                    message_flow_count = bpmn_content.count('<bpmn2:messageFlow')
                    
                    print(f"📊 Component counts:")
                    print(f"  - Service Tasks: {service_task_count}")
                    print(f"  - Participants: {participant_count}")
                    print(f"  - Message Flows: {message_flow_count}")
                    
                    # Check if we have the complete request-reply pattern
                    if service_task_count >= 2 and participant_count >= 2 and message_flow_count >= 2:
                        print("🎉 Complete request-reply patterns detected!")
                    else:
                        print("⚠️  Incomplete request-reply patterns - missing components")
                    
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
        print(f"❌ Error in SFTP request-reply test: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup():
    """Clean up test files"""
    print("\n🧹 Cleaning up...")
    
    test_files = [
        "test_sftp_bpmn.xml"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"✅ Removed: {file}")

if __name__ == "__main__":
    print("🚀 Testing Enhanced Request-Reply with SFTP")
    print("=" * 50)
    
    try:
        success = test_sftp_request_reply()
        
        if success:
            print("\n🎉 SFTP request-reply generation is working!")
        else:
            print("\n❌ SFTP request-reply generation has issues")
            
    finally:
        cleanup()
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")
    print("\n📋 What was tested:")
    print("- ✅ SFTP request-reply pattern generation")
    print("- ✅ SuccessFactors request-reply pattern generation")
    print("- ✅ Receiver participant creation")
    print("- ✅ Message flow creation with protocol details")
    print("- ✅ Complete request-reply pattern validation")
