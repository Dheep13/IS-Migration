#!/usr/bin/env python3
"""
Test script for RunPod API integration
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
RUNPOD_ENDPOINT_ID = os.getenv('RUNPOD_ENDPOINT_ID', 's5unaaduyy7otl')
RUNPOD_RUN_URL = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run"
RUNPOD_STATUS_URL = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status"

def test_runpod_api():
    """Test the RunPod API with a simple prompt"""
    
    if not RUNPOD_API_KEY:
        print("❌ RUNPOD_API_KEY not set in .env file")
        return False
    
    print(f"🚀 Testing RunPod API...")
    print(f"   Endpoint ID: {RUNPOD_ENDPOINT_ID}")
    print(f"   API Key: {RUNPOD_API_KEY[:10]}...")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {RUNPOD_API_KEY}'
    }
    
    # Simple test prompt
    data = {
        "input": {
            "prompt": "Generate a simple SAP Integration Suite iFlow XML structure with basic HTTP sender and receiver components.",
            "max_tokens": 500,
            "temperature": 0.7
        }
    }
    
    try:
        print("\n📤 Submitting job to RunPod...")
        response = requests.post(RUNPOD_RUN_URL, headers=headers, json=data, timeout=30)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return False
        
        job_data = response.json()
        job_id = job_data.get('id')
        
        if not job_id:
            print(f"❌ No job ID received: {job_data}")
            return False
        
        print(f"✅ Job submitted successfully!")
        print(f"   Job ID: {job_id}")
        
        # Poll for results (with shorter timeout for testing)
        print(f"\n⏳ Polling for results (max 2 minutes for test)...")
        start_time = time.time()
        max_wait = 120  # 2 minutes for test
        
        while time.time() - start_time < max_wait:
            try:
                status_response = requests.get(
                    f"{RUNPOD_STATUS_URL}/{job_id}",
                    headers=headers,
                    timeout=30
                )
                
                if status_response.status_code != 200:
                    print(f"❌ Status check failed: {status_response.text}")
                    return False
                
                status_data = status_response.json()
                job_status = status_data.get('status')
                elapsed = int(time.time() - start_time)
                
                print(f"   Status: {job_status} (Elapsed: {elapsed}s)")
                
                if job_status == 'COMPLETED':
                    print(f"✅ Job completed successfully!")
                    print(f"   Response structure: {list(status_data.keys())}")
                    
                    if 'output' in status_data:
                        output = status_data['output']
                        print(f"   Output type: {type(output)}")
                        if isinstance(output, list) and len(output) > 0:
                            print(f"   First output keys: {list(output[0].keys()) if isinstance(output[0], dict) else 'Not a dict'}")
                    
                    return True
                    
                elif job_status == 'FAILED':
                    print(f"❌ Job failed: {status_data}")
                    return False
                    
                elif job_status in ['IN_PROGRESS', 'IN_QUEUE']:
                    time.sleep(10)
                    
                else:
                    print(f"⚠️  Unknown status: {job_status}")
                    time.sleep(10)
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Error checking status: {e}")
                time.sleep(10)
        
        print(f"⏰ Timeout reached after {max_wait} seconds")
        print(f"   Job may still be running (cold start can take up to 10 minutes)")
        print(f"   You can check status manually at: {RUNPOD_STATUS_URL}/{job_id}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making RunPod API call: {e}")
        return False

def test_endpoint_health():
    """Test if the RunPod endpoint is accessible"""
    
    if not RUNPOD_API_KEY:
        print("❌ RUNPOD_API_KEY not set")
        return False
    
    headers = {
        'Authorization': f'Bearer {RUNPOD_API_KEY}'
    }
    
    try:
        # Try to get endpoint info (this might not work for all endpoints)
        print("🔍 Testing endpoint accessibility...")
        
        # Just try a simple request to see if we get a proper error
        response = requests.get(
            f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing endpoint: {e}")
        return False

if __name__ == "__main__":
    print("🧪 RunPod API Test")
    print("=" * 50)
    
    # Test endpoint health
    test_endpoint_health()
    
    print("\n" + "=" * 50)
    
    # Test actual API call
    success = test_runpod_api()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ RunPod API test completed successfully!")
    else:
        print("❌ RunPod API test failed or timed out")
        print("💡 Note: Cold starts can take up to 10 minutes")
