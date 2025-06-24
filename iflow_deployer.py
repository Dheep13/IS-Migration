#!/usr/bin/env python3
"""
Working SAP Integration Suite iFlow Deployer - ITR Internal
Final version with correct credentials and minimal headers
"""
import os
import sys
import json
import base64
import requests
import argparse
from datetime import datetime
from pathlib import Path

class WorkingITRDeployer:
    """Working SAP iFlow deployer for ITR Internal"""
    
    def __init__(self):
        """Initialize with working ITR Internal configuration"""
        # WORKING CREDENTIALS - NEW SERVICE KEY
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
    
    def deploy_iflow(self, iflow_path, iflow_id=None, iflow_name=None, package_id=None):
        """Deploy iFlow using the working method (Bearer + Minimal Headers)"""
        try:
            # Validate file
            if not os.path.exists(iflow_path):
                return {"status": "error", "message": f"File not found: {iflow_path}"}
            
            # Set defaults
            if not package_id:
                package_id = self.default_package
            if not iflow_name:
                iflow_name = Path(iflow_path).stem
            if not iflow_id:
                iflow_id = f"Generated_{iflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.log(f"Deploying: {iflow_name} (ID: {iflow_id}) to package: {package_id}")
            
            # Get OAuth token
            oauth_token = self.get_oauth_token()
            if not oauth_token:
                return {"status": "error", "message": "Failed to get OAuth token"}
            
            # Read and encode file
            self.log("Reading and encoding iFlow file...")
            with open(iflow_path, "rb") as f:
                iflow_content = f.read()
            
            base64_content = base64.b64encode(iflow_content).decode("utf-8")
            self.log(f"File encoded: {len(base64_content)} characters")
            
            # Create payload
            payload = {
                "Name": iflow_name,
                "Id": iflow_id,
                "PackageId": package_id,
                "ArtifactContent": base64_content
            }
            
            # Deploy with WORKING headers (Bearer + Minimal)
            self.log("Deploying with working headers...")
            headers = {
                "Authorization": f"Bearer {oauth_token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/api/v1/IntegrationDesigntimeArtifacts"
            self.log(f"POST to: {url}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            self.log(f"Response status: {response.status_code}")
            
            if response.status_code in [200, 201, 202]:
                self.log("✅ Deployment successful!")
                
                # Parse the response to get the actual ID
                try:
                    if response.headers.get('content-type', '').startswith('application/xml'):
                        # XML response, extract ID if possible
                        response_text = response.text
                        if 'Id=' in response_text:
                            # Try to extract ID from XML
                            import re
                            id_match = re.search(r"Id='([^']+)'", response_text)
                            if id_match:
                                actual_id = id_match.group(1)
                                self.log(f"Actual ID from response: {actual_id}")
                except:
                    pass
                
                return {
                    "status": "success",
                    "message": "iFlow deployed successfully",
                    "iflow_id": iflow_id,
                    "package_id": package_id,
                    "response_code": response.status_code,
                    "method": "Bearer + Minimal Headers"
                }
            elif response.status_code == 500 and "already exists" in response.text:
                return {
                    "status": "error", 
                    "message": f"iFlow with ID '{iflow_id}' already exists. Use a different ID or delete the existing one."
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text[:300]}"
                return {"status": "error", "message": error_msg}
            
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Deploy iFlow to ITR Internal (WORKING VERSION)")
    parser.add_argument("iflow_path", help="Path to the iFlow ZIP file")
    parser.add_argument("--iflow-id", help="Custom iFlow ID")
    parser.add_argument("--iflow-name", help="Custom iFlow name")
    parser.add_argument("--package", help="Target package ID")
    
    args = parser.parse_args()
    
    print("🚀 ITR Internal iFlow Deployment - WORKING VERSION")
    print(f"📁 File: {args.iflow_path}")
    print(f"📦 Package: {args.package or 'ConversionPackages'}")
    print("-" * 50)
    
    # Deploy
    deployer = WorkingITRDeployer()
    result = deployer.deploy_iflow(
        args.iflow_path,
        iflow_id=args.iflow_id,
        iflow_name=args.iflow_name,
        package_id=args.package
    )
    
    # Print result
    if result["status"] == "success":
        print(f"\n✅ SUCCESS: {result['message']}")
        print(f"   iFlow ID: {result['iflow_id']}")
        print(f"   Package: {result['package_id']}")
        print(f"   Response Code: {result['response_code']}")
        print(f"   Method: {result['method']}")
        print("\n🎉 Your iFlow has been deployed to ITR Internal!")
    else:
        print(f"\n❌ FAILED: {result['message']}")
        if "already exists" in result["message"]:
            print("\n💡 TIP: Try with a custom ID: --iflow-id MyUniqueID")
        sys.exit(1)

if __name__ == "__main__":
    main()