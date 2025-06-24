#!/usr/bin/env python3
"""
Test ITR Internal connection with current credentials
"""
import requests
import json
from datetime import datetime

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_itr_connection():
    """Test ITR Internal connection step by step"""
    
    # ITR Internal configuration
    tenant_url = "https://itr-internal-2hco92jx.integrationsuite-cpi034.cfapps.us10-002.hana.ondemand.com"
    client_id = "sb-3c34b7ea-2323-485e-9324-e9c25bbe72be!b124895|it!b410334"
    client_secret = "408913ea-83d7-458d-8243-31f15e4a4165$n35ZO3mV4kSJY5TJDcURz0XxgCQ4DjFnrwdv32Wwwxs="
    oauth_url = "https://itr-internal-2hco92jx.authentication.us10.hana.ondemand.com/oauth/token"
    
    log("🔍 Testing ITR Internal Connection")
    log("=" * 50)
    
    # Step 1: Test OAuth
    log("Step 1: Testing OAuth Token...")
    try:
        oauth_response = requests.post(
            oauth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if oauth_response.status_code == 200:
            token_data = oauth_response.json()
            oauth_token = token_data["access_token"]
            log(f"✅ OAuth Success: {oauth_response.status_code}")
            log(f"   Token Type: {token_data.get('token_type', 'Not specified')}")
            log(f"   Scope: {token_data.get('scope', 'Not specified')}")
            log(f"   Expires: {token_data.get('expires_in', 'Not specified')} seconds")
        else:
            log(f"❌ OAuth Failed: {oauth_response.status_code}")
            log(f"   Response: {oauth_response.text}")
            return
            
    except Exception as e:
        log(f"❌ OAuth Error: {e}")
        return
    
    print("\n" + "=" * 50)
    
    # Step 2: Test Package Access
    log("Step 2: Testing Package Access...")
    try:
        package_url = f"{tenant_url}/api/v1/IntegrationPackages('ConversionPackages')"
        headers = {
            "Authorization": f"Bearer {oauth_token}",
            "Accept": "application/json"
        }
        
        package_response = requests.get(package_url, headers=headers, timeout=30)
        log(f"Package access: {package_response.status_code}")
        
        if package_response.status_code == 200:
            log("✅ ConversionPackages exists and accessible")
            package_data = package_response.json()
            log(f"   Package Name: {package_data.get('d', {}).get('Name', 'Unknown')}")
        elif package_response.status_code == 404:
            log("❌ ConversionPackages not found")
        elif package_response.status_code == 401:
            log("❌ Unauthorized for package access")
        else:
            log(f"⚠️ Package access returned: {package_response.status_code}")
            log(f"   Response: {package_response.text[:200]}")
            
    except Exception as e:
        log(f"❌ Package check error: {e}")
    
    print("\n" + "=" * 50)
    
    # Step 3: Test CSRF Token
    log("Step 3: Testing CSRF Token...")
    try:
        csrf_url = f"{tenant_url}/api/v1/IntegrationDesigntimeArtifacts"
        csrf_headers = {
            "Authorization": f"Bearer {oauth_token}",
            "X-CSRF-Token": "Fetch",
            "Accept": "application/json"
        }
        
        csrf_response = requests.get(csrf_url, headers=csrf_headers, timeout=30)
        log(f"CSRF request: {csrf_response.status_code}")
        
        csrf_token = csrf_response.headers.get("X-CSRF-Token")
        if csrf_token and csrf_token != "Required":
            log(f"✅ CSRF token obtained: {csrf_token[:30]}...")
        else:
            log("⚠️ No CSRF token (might not be required)")
            
    except Exception as e:
        log(f"❌ CSRF test error: {e}")
    
    print("\n" + "=" * 50)
    
    # Step 4: Test Integration Design Time Artifacts Access
    log("Step 4: Testing Design Time Artifacts Access...")
    try:
        artifacts_url = f"{tenant_url}/api/v1/IntegrationDesigntimeArtifacts"
        artifacts_headers = {
            "Authorization": f"Bearer {oauth_token}",
            "Accept": "application/json"
        }
        
        artifacts_response = requests.get(artifacts_url, headers=artifacts_headers, timeout=30)
        log(f"Artifacts access: {artifacts_response.status_code}")
        
        if artifacts_response.status_code == 200:
            log("✅ Can access Integration Design Time Artifacts")
            artifacts_data = artifacts_response.json()
            if 'd' in artifacts_data and 'results' in artifacts_data['d']:
                count = len(artifacts_data['d']['results'])
                log(f"   Found {count} existing artifacts")
            else:
                log("   No existing artifacts found")
        elif artifacts_response.status_code == 401:
            log("❌ Unauthorized for artifacts access")
        else:
            log(f"⚠️ Artifacts access returned: {artifacts_response.status_code}")
            log(f"   Response: {artifacts_response.text[:200]}")
            
    except Exception as e:
        log(f"❌ Artifacts test error: {e}")
    
    print("\n" + "=" * 50)
    log("📋 CONNECTION TEST SUMMARY")
    log("=" * 50)
    
    # Determine the issue
    if oauth_response.status_code == 200:
        log("✅ OAuth authentication is working")
        if package_response.status_code == 200:
            log("✅ Package access is working")
            if artifacts_response.status_code == 200:
                log("✅ API access is working")
                log("🎉 Your credentials and permissions look good!")
                log("   The 401 errors were likely due to incorrect headers")
                log("   Try running the deployment script now")
            else:
                log("❌ Cannot access Design Time Artifacts API")
                log("   Issue: Missing 'WorkspaceArtifactsDeploy' or similar permission")
        else:
            log("❌ Cannot access ConversionPackages")
            log("   Issue: Package doesn't exist or no package read permission")
    else:
        log("❌ OAuth authentication is failing")
        log("   Issue: Wrong credentials or service instance configuration")

if __name__ == "__main__":
    test_itr_connection()