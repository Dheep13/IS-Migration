import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_KEY = os.getenv('RUNPOD_API_KEY')
ENDPOINT_ID = "s5unaaduyy7otl"
RUN_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
STATUS_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status"

def call_runpod_api(prompt: str, max_wait_time: int = 300):
    """
    Make a call to the RunPod API and wait for completion
    
    Args:
        prompt: The prompt to send
        max_wait_time: Maximum time to wait in seconds (default: 300 = 5 minutes)
    """
    
    if not API_KEY:
        print("Error: RUNPOD_API_KEY not found in .env file")
        print("Please add RUNPOD_API_KEY=your_api_key_here to your .env file")
        return None

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    data = {
        "input": {
            "prompt": prompt
        }
    }

    try:
        # Step 1: Submit the job
        print("Submitting job to RunPod...")
        response = requests.post(RUN_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        job_data = response.json()
        job_id = job_data.get('id')
        
        if not job_id:
            print("Error: No job ID received from RunPod")
            return None
            
        print(f"Job submitted successfully. Job ID: {job_id}")
        print("Waiting for completion...")
        
        # Step 2: Poll for results
        start_time = time.time()
        check_interval = 10  # Check every 10 seconds
        
        while time.time() - start_time < max_wait_time:
            # Check job status
            status_response = requests.get(
                f"{STATUS_URL}/{job_id}", 
                headers=headers, 
                timeout=30
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            
            job_status = status_data.get('status')
            elapsed_time = int(time.time() - start_time)
            
            print(f"Status: {job_status} (Elapsed: {elapsed_time}s)")
            
            if job_status == 'COMPLETED':
                print("Job completed successfully!")
                return status_data
            elif job_status == 'FAILED':
                print("Job failed!")
                return status_data
            elif job_status in ['IN_PROGRESS', 'IN_QUEUE']:
                # Continue waiting
                time.sleep(check_interval)
            else:
                print(f"Unknown status: {job_status}")
                time.sleep(check_interval)
        
        # Timeout reached
        print(f"Timeout reached after {max_wait_time} seconds")
        print("Job may still be running. You can check manually with job ID:", job_id)
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None

def extract_output(result_data):
    """Extract the actual output from the API response"""
    if not result_data:
        return None
    
    # Try to get the output from common response structures
    output = None
    if 'output' in result_data:
        output = result_data['output']
    elif 'result' in result_data:
        output = result_data['result']
    
    return output

# Example usage
if __name__ == "__main__":
    # Replace with your actual prompt
    user_prompt = "Generate a simple groovy script for SAP integration suite"
    
    print(f"Calling RunPod API with prompt: {user_prompt}")
    print("This may take up to 5 minutes...")
    print("-" * 50)
    
    result = call_runpod_api(user_prompt, max_wait_time=300)  # 5 minutes
    
    if result:
        print("\n" + "="*50)
        print("FULL API RESPONSE:")
        print(json.dumps(result, indent=2))
        
        # Try to extract just the output
        output = extract_output(result)
        if output:
            print("\n" + "="*50)
            print("EXTRACTED OUTPUT:")
            if isinstance(output, str):
                print(output)
            else:
                print(json.dumps(output, indent=2))
    else:
        print("Failed to get response from API")