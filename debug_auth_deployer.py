#!/usr/bin/env python3
"""
Debug different authentication methods for ITR Internal
Try Basic Auth, different headers, and other variations
"""
import os
import sys
import json
import base64
import requests
import argparse
from datetime import datetime
from pathlib import Path

class DebugAuthDeployer:
    """Debug authentication methods for ITR Internal"""
    
    def __init__(self):
        """Initialize with ITR Internal configuration - NEW CREDENTIALS"""
        # NEW SERVICE KEY CREDENTIALS
        self.tenant_url = "https://itr-internal-2hco92jx.it-cpi034.cfapps.us10-002.hana.ondemand.com"
        self.client_id = "sb-5e4b1b9b-d22f-427d-a6ae-f33c83513c0f!b124895|it!b410334"
        self.client_secret = "5813ca83-4ba6-4231-96e1-1a48a80eafec$kmhNJINpEbcsXgBQJn9vvaAHGgMegiM_-FB7EC_SF9w="
        self.oauth_url = "https://itr-internal-2hco92jx.authentication.us10.hana.ondemand.com/oauth/token"
        self.default_package = "ConversionPackages"
        
        self.base_url = self.tenant_url.rstrip('/')
        
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def get_oauth_token(self):
        """Get OAuth token"""
        try:
            self.log("Getting OAuth token...")
            response = requests.post(
                self.oauth_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                token = token_data["access_token"]
                self.log("✅ OAuth token obtained")
                return token
            else:
                self.log(f"❌ OAuth failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.log(f"❌ OAuth error: {e}")
            return None
    
    def test_auth_methods(self, payload):
        """Test different authentication methods"""
        oauth_token = self.get_oauth_token()
        if not oauth_token:
            self.log("❌ Cannot get OAuth token")
            return
        
        url = f"{self.base_url}/api/v1/IntegrationDesigntimeArtifacts"
        
        # Method 1: Bearer token with minimal headers
        self.log("\n=== Method 1: Bearer + Minimal Headers ===")
        headers1 = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json"
        }
        self.test_post_request(url, headers1, payload, "Bearer + Minimal")
        
        # Method 2: Bearer token with OData headers
        self.log("\n=== Method 2: Bearer + OData Headers ===")
        headers2 = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "DataServiceVersion": "2.0"
        }
        self.test_post_request(url, headers2, payload, "Bearer + OData")
        
        # Method 3: Basic Auth using client credentials
        self.log("\n=== Method 3: Basic Auth ===")
        basic_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers3 = {
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.test_post_request(url, headers3, payload, "Basic Auth")
        
        # Method 4: Bearer with User-Agent
        self.log("\n=== Method 4: Bearer + User-Agent ===")
        headers4 = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "DataServiceVersion": "2.0",
            "User-Agent": "ITR-Deployer/1.0"
        }
        self.test_post_request(url, headers4, payload, "Bearer + User-Agent")
        
        # Method 5: Try without Accept header
        self.log("\n=== Method 5: Bearer without Accept ===")
        headers5 = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json",
            "DataServiceVersion": "2.0"
        }
        self.test_post_request(url, headers5, payload, "Bearer without Accept")
        
        # Method 6: Try different Content-Type
        self.log("\n=== Method 6: Bearer + XML Content-Type ===")
        headers6 = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/atom+xml",
            "Accept": "application/json"
        }
        self.test_post_request(url, headers6, payload, "Bearer + XML Content-Type")
        
        # Method 7: Try with session approach
        self.log("\n=== Method 7: Session-based approach ===")
        session = requests.Session()
        # First, make a GET request to establish session
        get_response = session.get(url, headers={"Authorization": f"Bearer {oauth_token}"})
        self.log(f"Session GET status: {get_response.status_code}")
        
        # Then try POST with the same session
        headers7 = {
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "DataServiceVersion": "2.0"
        }
        
        try:
            response = session.post(url, headers=headers7, json=payload, timeout=60)
            self.log(f"Session POST result: {response.status_code}")
            if response.status_code not in [401, 403]:
                self.log(f"Response: {response.text[:200]}...")
        except Exception as e:
            self.log(f"Session POST error: {e}")
    
    def test_post_request(self, url, headers, payload, method_name):
        """Test a single POST request"""
        try:
            self.log(f"Testing {method_name}...")
            self.log(f"Headers: {list(headers.keys())}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            self.log(f"Status: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                self.log(f"🎉 SUCCESS with {method_name}!")
                self.log(f"Response: {response.text[:200]}...")
                return True
            elif response.status_code != 401:
                self.log(f"Different error: {response.text[:200]}...")
            else:
                self.log("Still 401 Unauthorized")
                
        except Exception as e:
            self.log(f"Error: {e}")
        
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Debug authentication methods for ITR Internal")
    parser.add_argument("iflow_path", help="Path to the iFlow ZIP file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.iflow_path):
        print(f"❌ File not found: {args.iflow_path}")
        return
    
    print("🔍 ITR Internal Authentication Debug")
    print(f"📁 File: {args.iflow_path}")
    print("-" * 50)
    
    # Read and encode file
    with open(args.iflow_path, "rb") as f:
        iflow_content = f.read()
    
    base64_content = base64.b64encode(iflow_content).decode("utf-8")
    
    # Create test payload
    payload = {
        "Name": "Test_Debug_Flow",
        "Id": f"Debug_Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "PackageId": "ConversionPackages",
        "ArtifactContent": base64_content
    }
    
    print(f"Payload size: {len(base64_content)} characters")
    
    # Test different authentication methods
    deployer = DebugAuthDeployer()
    deployer.test_auth_methods(payload)

if __name__ == "__main__":
    main()