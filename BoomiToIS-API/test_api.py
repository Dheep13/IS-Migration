"""
Test script for the MuleToIS API.
This script tests the API by generating an iFlow from a sample markdown file.
"""

import os
import sys
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API base URL
API_BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    return response.status_code == 200

def test_generate_iflow(markdown_content):
    """Test the generate iFlow endpoint"""
    print("Testing generate iFlow endpoint...")
    
    # Prepare request data
    data = {
        "markdown": markdown_content,
        "iflow_name": "TestIFlow"
    }
    
    # Send request
    response = requests.post(f"{API_BASE_URL}/generate-iflow", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    if response.status_code != 202:
        return None
    
    return response.json().get("job_id")

def test_get_job_status(job_id):
    """Test the get job status endpoint"""
    print(f"Testing get job status endpoint for job {job_id}...")
    
    # Poll for job status
    max_attempts = 30
    attempt = 0
    completed = False
    
    while attempt < max_attempts and not completed:
        # Send request
        response = requests.get(f"{API_BASE_URL}/jobs/{job_id}")
        print(f"Attempt {attempt + 1}/{max_attempts}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        if response.status_code != 200:
            return False
        
        status = response.json().get("status")
        if status == "completed":
            completed = True
        elif status == "failed":
            return False
        
        attempt += 1
        if not completed and attempt < max_attempts:
            print("Waiting 5 seconds before next attempt...")
            time.sleep(5)
    
    return completed

def test_download_iflow(job_id):
    """Test the download iFlow endpoint"""
    print(f"Testing download iFlow endpoint for job {job_id}...")
    
    # Send request
    response = requests.get(f"{API_BASE_URL}/jobs/{job_id}/download")
    print(f"Status code: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to download iFlow")
        return False
    
    # Save the downloaded file
    filename = f"TestIFlow_{job_id}.zip"
    with open(filename, "wb") as f:
        f.write(response.content)
    
    print(f"Downloaded iFlow saved to {filename}")
    print()
    
    return True

def main():
    """Main test function"""
    # Check if the API is running
    if not test_health_check():
        print("Health check failed. Make sure the API is running.")
        return
    
    # Sample markdown content
    markdown_content = """
    # Simple Product API
    
    ## Overview
    This API provides access to product information.
    
    ## Base URL
    `https://example.com/api`
    
    ## Endpoints
    
    ### Get Products
    Retrieves a list of all products.
    
    **Method**: GET  
    **Path**: `/products`  
    **Response**: JSON array of product objects
    
    **Process Flow**:
    1. Prepare request headers
    2. Log the request
    3. Call OData Products service
    4. Set response headers
    5. Transform response to required format
    """
    
    # Generate iFlow
    job_id = test_generate_iflow(markdown_content)
    if not job_id:
        print("Failed to generate iFlow")
        return
    
    # Check job status
    if not test_get_job_status(job_id):
        print("Job failed or timed out")
        return
    
    # Download iFlow
    if not test_download_iflow(job_id):
        print("Failed to download iFlow")
        return
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    main()
