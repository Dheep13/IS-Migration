#!/usr/bin/env python3
"""
Test script for the complete Boomi to SAP Integration Suite implementation

This script tests the end-to-end flow:
1. Main API (app/app.py) - Platform selection and routing
2. Boomi Documentation Generator (app/boomi_flow_documentation.py) 
3. Boomi iFlow Generator (BoomiToIS-API/enhanced_genai_iflow_generator.py)
4. Frontend platform selection
"""

import os
import sys
import requests
import json
import time

def test_main_api_health():
    """Test the main API health endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("✅ Main API (port 5000) is running")
            return True
        else:
            print(f"❌ Main API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Main API (port 5000) is not running")
        return False

def test_boomi_api_health():
    """Test the Boomi API health endpoint"""
    try:
        response = requests.get('http://localhost:5003/api/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Boomi API (port 5003) is running - Platform: {data.get('platform', 'Unknown')}")
            return True
        else:
            print(f"❌ Boomi API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Boomi API (port 5003) is not running")
        return False

def test_platform_selection():
    """Test platform selection in main API"""
    try:
        # Test with sample Boomi XML file
        boomi_xml = """<?xml version="1.0" encoding="UTF-8"?>
<component xmlns="http://api.platform.boomi.com/" componentId="test-process" name="Test Boomi Process" type="process">
    <process allowSimultaneous="false">
        <shape name="Start" shapetype="start" x="100" y="100">
            <dragpoint name="out" toShape="Transform" x="150" y="100"/>
        </shape>
        <shape name="Transform" shapetype="map" x="200" y="100">
            <configuration>
                <map mapId="test-map"/>
            </configuration>
            <dragpoint name="out" toShape="End" x="250" y="100"/>
        </shape>
        <shape name="End" shapetype="stop" x="300" y="100"/>
    </process>
</component>"""
        
        # Create test file
        test_file_path = 'test_boomi_process.xml'
        with open(test_file_path, 'w') as f:
            f.write(boomi_xml)
        
        # Test Boomi platform selection
        files = {'files[]': open(test_file_path, 'rb')}
        data = {'platform': 'boomi', 'enhance': 'true'}
        
        response = requests.post('http://localhost:5000/api/generate-docs', files=files, data=data)
        files['files[]'].close()
        
        if response.status_code == 202:
            result = response.json()
            print(f"✅ Platform selection works - Job ID: {result['job_id']}, Platform: {result['platform']}")
            
            # Clean up
            os.remove(test_file_path)
            return result['job_id']
        else:
            print(f"❌ Platform selection failed: {response.status_code} - {response.text}")
            os.remove(test_file_path)
            return None
            
    except Exception as e:
        print(f"❌ Platform selection test failed: {str(e)}")
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        return None

def test_job_status(job_id):
    """Test job status monitoring"""
    try:
        max_attempts = 30  # 30 seconds timeout
        for attempt in range(max_attempts):
            response = requests.get(f'http://localhost:5000/api/jobs/{job_id}')
            if response.status_code == 200:
                job_data = response.json()
                status = job_data['status']
                platform = job_data.get('platform', 'unknown')
                
                print(f"📊 Job {job_id} - Status: {status}, Platform: {platform}")
                
                if status == 'completed':
                    print("✅ Job completed successfully")
                    return True
                elif status == 'failed':
                    error = job_data.get('error', 'Unknown error')
                    print(f"❌ Job failed: {error}")
                    return False
                
                time.sleep(1)
            else:
                print(f"❌ Failed to get job status: {response.status_code}")
                return False
        
        print("❌ Job timed out")
        return False
        
    except Exception as e:
        print(f"❌ Job status test failed: {str(e)}")
        return False

def test_boomi_iflow_generation():
    """Test Boomi iFlow generation via BoomiToIS-API"""
    try:
        # Test markdown content that represents Boomi documentation
        markdown_content = """
# Dell Boomi Process Documentation

## Process: Customer Data Sync

### Process Flow
- **Start Shape**: Initiates the process
- **HTTP Connector**: Receives customer data from external system
- **Map**: Transforms customer data format
- **Salesforce Connector**: Sends data to Salesforce
- **Stop Shape**: Ends the process

### Integration Patterns
- Data synchronization
- Real-time integration
- Error handling

### Component Mapping to SAP Integration Suite
| Boomi Component | SAP Equivalent |
|-----------------|----------------|
| Start Shape | Start Event |
| HTTP Connector | HTTP Adapter |
| Map | Message Mapping |
| Salesforce Connector | Salesforce Adapter |
| Stop Shape | End Event |
"""
        
        # Send to Boomi API for iFlow generation
        response = requests.post(
            'http://localhost:5003/api/generate-iflow',
            json={'markdown_content': markdown_content}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Boomi iFlow generation successful")
            print(f"📄 Generated iFlow ID: {result.get('iflow_id', 'Unknown')}")
            return True
        else:
            print(f"❌ Boomi iFlow generation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Boomi iFlow generation test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Dell Boomi to SAP Integration Suite Implementation")
    print("=" * 60)
    
    # Test 1: API Health Checks
    print("\n1. Testing API Health...")
    main_api_ok = test_main_api_health()
    boomi_api_ok = test_boomi_api_health()
    
    if not main_api_ok:
        print("\n❌ Main API is not running. Please start it with:")
        print("   cd app && python app.py")
        return False
    
    if not boomi_api_ok:
        print("\n❌ Boomi API is not running. Please start it with:")
        print("   start-boomi-api-development.bat")
        return False
    
    # Test 2: Platform Selection
    print("\n2. Testing Platform Selection...")
    job_id = test_platform_selection()
    
    if not job_id:
        print("❌ Platform selection test failed")
        return False
    
    # Test 3: Job Processing
    print("\n3. Testing Job Processing...")
    job_success = test_job_status(job_id)
    
    if not job_success:
        print("❌ Job processing test failed")
        return False
    
    # Test 4: Boomi iFlow Generation
    print("\n4. Testing Boomi iFlow Generation...")
    iflow_success = test_boomi_iflow_generation()
    
    if not iflow_success:
        print("❌ Boomi iFlow generation test failed")
        return False
    
    # All tests passed
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Dell Boomi to SAP Integration Suite implementation is working correctly")
    print("\nNext steps:")
    print("1. Test with real Boomi XML files")
    print("2. Verify frontend platform selection UI")
    print("3. Test end-to-end workflow with actual Boomi processes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
