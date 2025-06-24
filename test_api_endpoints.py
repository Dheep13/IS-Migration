#!/usr/bin/env python3
"""
Test script to check which API endpoints are accessible for SAP Integration Suite
"""

import requests
import json
from datetime import datetime

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_oauth_token(tenant_config):
    """Test OAuth token generation"""
    try:
        log("Testing OAuth token generation...")
        response = requests.post(
            tenant_config['oauth_url'],
            data={
                "grant_type": "client_credentials",
                "client_id": tenant_config['client_id'],
                "client_secret": tenant_config['client_secret']
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            log(f"✅ OAuth token obtained: {token[:20]}...")
            return token
        else:
            log(f"❌ OAuth failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        log(f"❌ OAuth error: {e}")
        return None

def test_api_endpoints(base_url, oauth_token):
    """Test different API endpoints"""
    endpoints_to_test = [
        "/cpi/api/v1/IntegrationDesigntimeArtifacts",  # SAP Documentation
        "/api/v1/IntegrationDesigntimeArtifacts",      # Current approach
        "/itspaces/api/1.0/workspace",                 # Alternative
        "/api/v1/IntegrationPackages",                 # Packages
        "/api/v1",                                     # Base API
        "/cpi/api/v1",                                 # CPI Base API
        "/itspaces",                                   # IT Spaces
    ]
    
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Accept": "application/json",
        "X-CSRF-Token": "Fetch"
    }
    
    results = {}
    
    for endpoint in endpoints_to_test:
        try:
            log(f"Testing endpoint: {base_url}{endpoint}")
            response = requests.get(
                f"{base_url}{endpoint}",
                headers=headers,
                timeout=30
            )
            
            status = response.status_code
            csrf_token = response.headers.get("X-CSRF-Token", "None")
            content_type = response.headers.get("Content-Type", "Unknown")
            
            log(f"  Status: {status}")
            log(f"  CSRF Token: {csrf_token}")
            log(f"  Content-Type: {content_type}")
            
            if status == 200:
                log(f"  ✅ Accessible")
            elif status == 401:
                log(f"  ❌ Unauthorized")
            elif status == 404:
                log(f"  ❌ Not Found")
            else:
                log(f"  ⚠️ Status {status}")
            
            results[endpoint] = {
                "status": status,
                "csrf_token": csrf_token,
                "content_type": content_type,
                "accessible": status == 200
            }
            
        except Exception as e:
            log(f"  ❌ Error: {e}")
            results[endpoint] = {
                "status": "ERROR",
                "error": str(e),
                "accessible": False
            }
        
        log("")
    
    return results

def main():
    """Main function"""
    # Tenant configurations
    tenants = {
        "ITR Internal": {
            "tenant_url": "https://itr-internal-2hco92jx.integrationsuite-cpi034.cfapps.us10-002.hana.ondemand.com",
            "client_id": "sb-3c34b7ea-2323-485e-9324-e9c25bbe72be!b124895|it!b410334",
            "client_secret": "408913ea-83d7-458d-8243-31f15e4a4165$n35ZO3mV4kSJY5TJDcURz0XxgCQ4DjFnrwdv32Wwwxs=",
            "oauth_url": "https://itr-internal-2hco92jx.authentication.us10.hana.ondemand.com/oauth/token"
        },
        "Trial": {
            "tenant_url": "https://4728b940trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com",
            "client_id": "sb-09f9c01e-d098-4f72-8b09-b39757ec93a2!b443330|it!b26655",
            "client_secret": "3a96f9f7-f596-48a8-903c-afd54ad9583e$6wFmr1lu8TWwA8OUI2GnRsL4Vie86YcIiUaMBei8zD0=",
            "oauth_url": "https://4728b940trial.authentication.us10.hana.ondemand.com/oauth/token"
        }
    }
    
    for tenant_name, tenant_config in tenants.items():
        print("=" * 60)
        print(f"TESTING TENANT: {tenant_name}")
        print("=" * 60)
        
        # Test OAuth
        oauth_token = test_oauth_token(tenant_config)
        if not oauth_token:
            print(f"❌ Skipping {tenant_name} - OAuth failed")
            continue
        
        # Test API endpoints
        results = test_api_endpoints(tenant_config['tenant_url'], oauth_token)
        
        # Summary
        print("-" * 40)
        print("SUMMARY:")
        accessible_endpoints = [ep for ep, result in results.items() if result.get('accessible')]
        csrf_endpoints = [ep for ep, result in results.items() if result.get('csrf_token') not in ['None', None]]
        
        print(f"✅ Accessible endpoints: {len(accessible_endpoints)}")
        for ep in accessible_endpoints:
            print(f"   {ep}")
        
        print(f"🔑 CSRF token endpoints: {len(csrf_endpoints)}")
        for ep in csrf_endpoints:
            csrf_token = results[ep]['csrf_token']
            print(f"   {ep} -> {csrf_token}")
        
        print("")

if __name__ == "__main__":
    main()
