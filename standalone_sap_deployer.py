#!/usr/bin/env python3
"""
Standalone SAP Integration Suite iFlow Deployer

This script allows you to deploy iFlow ZIP files directly to SAP Integration Suite
without needing the full BoomiToIS-API service.

Usage:
    python standalone_sap_deployer.py <iflow_zip_path> [options]

Examples:
    python standalone_sap_deployer.py my_iflow.zip
    python standalone_sap_deployer.py my_iflow.zip --iflow-id MyCustomID --package ConversionPackages
    python standalone_sap_deployer.py my_iflow.zip --tenant trial
"""

import os
import sys
import json
import base64
import requests
import argparse
from datetime import datetime
from pathlib import Path

class StandaloneSAPDeployer:
    """Standalone SAP Integration Suite iFlow deployer"""
    
    def __init__(self, tenant_config):
        """Initialize with tenant configuration"""
        self.tenant_url = tenant_config['tenant_url']
        self.client_id = tenant_config['client_id']
        self.client_secret = tenant_config['client_secret']
        self.oauth_url = tenant_config['oauth_url']
        self.default_package = tenant_config.get('default_package', 'ConversionPackages')
        
        self.base_url = self.tenant_url.rstrip('/')
        self.token_url = self.oauth_url
        
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def get_oauth_token(self):
        """Get OAuth token for authentication"""
        try:
            self.log("Getting OAuth token...")
            response = requests.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=30
            )
            
            self.log(f"OAuth response status: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = f"Failed to get OAuth token: {response.text}"
                self.log(error_msg)
                return None
                
            try:
                oauth_token = response.json()["access_token"]
                self.log("OAuth token obtained successfully")
                return oauth_token
            except (json.JSONDecodeError, KeyError) as e:
                error_msg = f"Error parsing OAuth response: {e}"
                self.log(error_msg)
                return None
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during OAuth request: {e}"
            self.log(error_msg)
            return None
    
    def create_session(self, oauth_token):
        """Create authenticated session with multiple approaches"""
        try:
            self.log("Creating authenticated session...")
            session = requests.Session()

            # Try multiple session initialization approaches
            session_endpoints = [
                "/itspaces/shell",
                "/itspaces",
                "/api/v1",
                "/shell",
                "/"
            ]

            for endpoint in session_endpoints:
                try:
                    self.log(f"Trying session endpoint: {self.base_url}{endpoint}")
                    session_response = session.get(
                        f"{self.base_url}{endpoint}",
                        headers={
                            "Authorization": f"Bearer {oauth_token}",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        },
                        timeout=30,
                        allow_redirects=True
                    )

                    self.log(f"Session endpoint {endpoint} response: {session_response.status_code}")

                    if session.cookies:
                        self.log(f"Session cookies obtained: {list(session.cookies.keys())}")
                        break
                    else:
                        self.log(f"No cookies from {endpoint}")

                except requests.exceptions.RequestException as e:
                    self.log(f"Error with session endpoint {endpoint}: {e}")

            # Final cookie check
            if session.cookies:
                self.log("✅ Session created successfully with cookies")
            else:
                self.log("⚠️ Session created but no cookies - will try anyway")

            return session

        except requests.exceptions.RequestException as e:
            self.log(f"Error creating session: {e}")
            return requests.Session()  # Return basic session as fallback

    def get_csrf_token(self, session, oauth_token):
        """Get CSRF token as required by SAP documentation"""
        try:
            self.log("Getting CSRF token...")

            # Try multiple CSRF endpoints based on SAP documentation
            csrf_endpoints = [
                "/cpi/api/v1/IntegrationDesigntimeArtifacts",
                "/api/v1/IntegrationDesigntimeArtifacts",
                "/itspaces/api/1.0/workspace",
                "/api/v1/IntegrationPackages"
            ]

            for endpoint in csrf_endpoints:
                try:
                    self.log(f"Trying CSRF endpoint: {self.base_url}{endpoint}")
                    response = session.get(
                        f"{self.base_url}{endpoint}",
                        headers={
                            "Authorization": f"Bearer {oauth_token}",
                            "X-CSRF-Token": "Fetch",
                            "Accept": "application/json"
                        },
                        timeout=30
                    )

                    self.log(f"CSRF request to {endpoint} returned status {response.status_code}")

                    # Check for CSRF token in response headers
                    csrf_headers = ["X-CSRF-Token", "x-csrf-token", "X-Csrf-Token"]
                    for header_name in csrf_headers:
                        if header_name in response.headers:
                            csrf_token = response.headers[header_name]
                            self.log(f"✅ CSRF token obtained from {header_name}: {csrf_token[:10]}...")
                            return csrf_token

                    self.log(f"No CSRF token in response headers: {list(response.headers.keys())}")

                except requests.exceptions.RequestException as e:
                    self.log(f"Error getting CSRF from {endpoint}: {e}")

            self.log("⚠️ No CSRF token found - will proceed without it")
            return None

        except Exception as e:
            self.log(f"Error getting CSRF token: {e}")
            return None

    def deploy_iflow(self, iflow_path, iflow_id=None, iflow_name=None, package_id=None):
        """Deploy iFlow to SAP Integration Suite"""
        try:
            # Validate file exists
            if not os.path.exists(iflow_path):
                return {"status": "error", "message": f"File not found: {iflow_path}"}
            
            # Set defaults
            if not package_id:
                package_id = self.default_package
            if not iflow_name:
                iflow_name = Path(iflow_path).stem
            if not iflow_id:
                iflow_id = f"Generated_{iflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.log(f"Deploying iFlow: {iflow_name} (ID: {iflow_id}) to package: {package_id}")
            
            # Step 1: Get OAuth token
            oauth_token = self.get_oauth_token()
            if not oauth_token:
                return {"status": "error", "message": "Failed to get OAuth token"}
            
            # Step 2: Create session
            session = self.create_session(oauth_token)

            # Step 2.5: Get CSRF token (required by SAP documentation)
            csrf_token = self.get_csrf_token(session, oauth_token)
            
            # Step 3: Read and encode iFlow file
            self.log("Reading and encoding iFlow file...")
            try:
                with open(iflow_path, "rb") as f:
                    iflow_content = f.read()
                
                self.log(f"Read {len(iflow_content)} bytes from file")
                base64_content = base64.b64encode(iflow_content).decode("utf-8")
                self.log(f"File encoded as base64 ({len(base64_content)} characters)")
            except Exception as e:
                return {"status": "error", "message": f"Error reading file: {e}"}
            
            # Step 4: Create payload
            self.log("Creating payload...")
            payload = {
                "Name": iflow_name,
                "Id": iflow_id,
                "PackageId": package_id,
                "ArtifactContent": base64_content
            }
            
            # Step 5: Upload iFlow with enhanced headers (based on SAP documentation)
            self.log("Uploading iFlow...")
            headers = {
                "Authorization": f"Bearer {oauth_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "DataServiceVersion": "2.0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }

            # Add CSRF token if available (required by SAP documentation)
            if csrf_token:
                headers["X-CSRF-Token"] = csrf_token
                self.log(f"✅ Using CSRF token: {csrf_token[:10]}...")
            else:
                self.log("⚠️ No CSRF token available - proceeding without it")
            
            # Try multiple endpoints with different approaches (based on SAP documentation)
            endpoints = [
                "/cpi/api/v1/IntegrationDesigntimeArtifacts",  # SAP documented endpoint
                "/api/v1/IntegrationDesigntimeArtifacts",      # Original endpoint
                "/itspaces/api/1.0/workspace/content"          # Alternative endpoint
            ]

            # For ITR Internal tenant, also try without session (direct approach)
            if "itr-internal" in self.base_url:
                self.log("ITR Internal tenant detected - will try both session and direct approaches")
            
            for endpoint in endpoints:
                self.log(f"Trying upload endpoint: {self.base_url}{endpoint}")
                
                try:
                    response = session.post(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        json=payload,
                        timeout=120
                    )
                    
                    self.log(f"Upload response status: {response.status_code}")
                    response_text = response.text
                    self.log(f"Response content: {response_text[:300]}...")
                    
                    if response.status_code in [200, 201, 202]:
                        self.log("✅ Upload successful!")
                        return {
                            "status": "success",
                            "message": "iFlow deployed successfully",
                            "iflow_id": iflow_id,
                            "package_id": package_id,
                            "iflow_name": iflow_name,
                            "endpoint_used": endpoint
                        }
                    elif response.status_code == 401:
                        self.log(f"❌ 401 Unauthorized - Response headers: {dict(response.headers)}")
                        
                except requests.exceptions.RequestException as e:
                    self.log(f"Network error during upload to {endpoint}: {e}")

            # If session approach failed for ITR Internal, try direct requests
            if "itr-internal" in self.base_url:
                self.log("Session approach failed, trying direct requests...")
                for endpoint in endpoints:
                    self.log(f"Trying direct upload to: {self.base_url}{endpoint}")

                    try:
                        response = requests.post(
                            f"{self.base_url}{endpoint}",
                            headers=headers,
                            json=payload,
                            timeout=120
                        )

                        self.log(f"Direct upload response status: {response.status_code}")
                        response_text = response.text
                        self.log(f"Direct response content: {response_text[:300]}...")

                        if response.status_code in [200, 201, 202]:
                            self.log("✅ Direct upload successful!")
                            return {
                                "status": "success",
                                "message": "iFlow deployed successfully (direct approach)",
                                "iflow_id": iflow_id,
                                "package_id": package_id,
                                "iflow_name": iflow_name,
                                "endpoint_used": endpoint,
                                "method": "direct"
                            }

                    except requests.exceptions.RequestException as e:
                        self.log(f"Network error during direct upload to {endpoint}: {e}")

            return {"status": "error", "message": f"Failed to deploy iFlow. Last response: {response_text}"}
            
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

def get_tenant_configs():
    """Get available tenant configurations"""
    return {
        "itr_internal": {
            "name": "ITR Internal",
            "tenant_url": "https://itr-internal-2hco92jx.integrationsuite-cpi034.cfapps.us10-002.hana.ondemand.com",
            "client_id": "sb-3c34b7ea-2323-485e-9324-e9c25bbe72be!b124895|it!b410334",
            "client_secret": "408913ea-83d7-458d-8243-31f15e4a4165$n35ZO3mV4kSJY5TJDcURz0XxgCQ4DjFnrwdv32Wwwxs=",
            "oauth_url": "https://itr-internal-2hco92jx.authentication.us10.hana.ondemand.com/oauth/token",
            "default_package": "ConversionPackages"
        },
        "trial": {
            "name": "Trial Account",
            "tenant_url": "https://4728b940trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com",
            "client_id": "sb-09f9c01e-d098-4f72-8b09-b39757ec93a2!b443330|it!b26655",
            "client_secret": "3a96f9f7-f596-48a8-903c-afd54ad9583e$6wFmr1lu8TWwA8OUI2GnRsL4Vie86YcIiUaMBei8zD0=",
            "oauth_url": "https://4728b940trial.authentication.us10.hana.ondemand.com/oauth/token",
            "default_package": "WithRequestReply"
        }
    }

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Deploy iFlow ZIP files to SAP Integration Suite")
    parser.add_argument("iflow_path", help="Path to the iFlow ZIP file")
    parser.add_argument("--tenant", choices=["itr_internal", "trial"], default="itr_internal",
                       help="Target tenant (default: itr_internal)")
    parser.add_argument("--iflow-id", help="Custom iFlow ID (default: auto-generated)")
    parser.add_argument("--iflow-name", help="Custom iFlow name (default: filename)")
    parser.add_argument("--package", help="Target package ID (default: tenant default)")
    parser.add_argument("--list-tenants", action="store_true", help="List available tenants")
    
    args = parser.parse_args()
    
    # List tenants if requested
    if args.list_tenants:
        configs = get_tenant_configs()
        print("\nAvailable tenants:")
        for key, config in configs.items():
            print(f"  {key}: {config['name']} ({config['tenant_url']})")
        return
    
    # Validate file path
    if not os.path.exists(args.iflow_path):
        print(f"❌ Error: File not found: {args.iflow_path}")
        sys.exit(1)
    
    # Get tenant configuration
    configs = get_tenant_configs()
    if args.tenant not in configs:
        print(f"❌ Error: Unknown tenant: {args.tenant}")
        print(f"Available tenants: {list(configs.keys())}")
        sys.exit(1)
    
    tenant_config = configs[args.tenant]
    print(f"🚀 Deploying to: {tenant_config['name']}")
    print(f"📁 File: {args.iflow_path}")
    print(f"📦 Package: {args.package or tenant_config['default_package']}")
    print("-" * 50)
    
    # Deploy iFlow
    deployer = StandaloneSAPDeployer(tenant_config)
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
        print(f"   Endpoint: {result.get('endpoint_used', 'N/A')}")
    else:
        print(f"\n❌ FAILED: {result['message']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
