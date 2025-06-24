#!/usr/bin/env python3
"""
SAP Integration Suite Permissions and Configuration Checker

This script checks:
1. OAuth token permissions
2. Package existence
3. Write permissions
4. CSRF token availability
5. API endpoint accessibility
"""

import requests
import json
import base64
from datetime import datetime

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_oauth_permissions(tenant_config):
    """Check OAuth token and decode permissions"""
    try:
        log("🔐 Checking OAuth token and permissions...")
        
        response = requests.post(
            tenant_config['oauth_url'],
            data={
                "grant_type": "client_credentials",
                "client_id": tenant_config['client_id'],
                "client_secret": tenant_config['client_secret']
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code != 200:
            log(f"❌ OAuth failed: {response.status_code} - {response.text}")
            return None
        
        token = response.json()["access_token"]
        log(f"✅ OAuth token obtained: {token[:20]}...")
        
        # Try to decode JWT token to see permissions (basic decode, no verification)
        try:
            # JWT has 3 parts separated by dots
            parts = token.split('.')
            if len(parts) == 3:
                # Decode payload (second part)
                payload = parts[1]
                # Add padding if needed
                payload += '=' * (4 - len(payload) % 4)
                decoded = base64.b64decode(payload)
                token_data = json.loads(decoded)
                
                log("🔍 Token permissions found:")
                if 'authorities' in token_data:
                    authorities = token_data['authorities']
                    write_perms = [auth for auth in authorities if 'Write' in auth or 'write' in auth]
                    integration_perms = [auth for auth in authorities if 'Integration' in auth]
                    
                    log(f"   📝 Write permissions: {len(write_perms)}")
                    for perm in write_perms[:5]:  # Show first 5
                        log(f"      - {perm}")
                    
                    log(f"   🔗 Integration permissions: {len(integration_perms)}")
                    for perm in integration_perms[:5]:  # Show first 5
                        log(f"      - {perm}")
                        
                if 'scope' in token_data:
                    scopes = token_data['scope']
                    log(f"   🎯 OAuth scopes: {len(scopes)}")
                    
        except Exception as e:
            log(f"⚠️ Could not decode token permissions: {e}")
        
        return token
        
    except Exception as e:
        log(f"❌ OAuth error: {e}")
        return None

def check_package_existence(base_url, oauth_token, package_id):
    """Check if the target package exists"""
    try:
        log(f"📦 Checking if package '{package_id}' exists...")
        
        # Try different package API endpoints
        package_endpoints = [
            f"/cpi/api/v1/IntegrationPackages('{package_id}')",
            f"/api/v1/IntegrationPackages('{package_id}')",
            f"/cpi/api/v1/IntegrationPackages",
            f"/api/v1/IntegrationPackages"
        ]
        
        headers = {
            "Authorization": f"Bearer {oauth_token}",
            "Accept": "application/json"
        }
        
        for endpoint in package_endpoints:
            try:
                log(f"   Trying: {base_url}{endpoint}")
                response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=30)
                
                log(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    if package_id in endpoint:
                        log(f"   ✅ Package '{package_id}' exists!")
                        return True
                    else:
                        # List all packages
                        try:
                            data = response.json()
                            if 'd' in data and 'results' in data['d']:
                                packages = data['d']['results']
                                package_names = [pkg.get('Id', 'Unknown') for pkg in packages]
                                log(f"   📋 Available packages: {package_names}")
                                
                                if package_id in package_names:
                                    log(f"   ✅ Package '{package_id}' found in list!")
                                    return True
                                else:
                                    log(f"   ❌ Package '{package_id}' not found in list")
                        except:
                            log(f"   ⚠️ Could not parse package list")
                            
                elif response.status_code == 404:
                    log(f"   ❌ Package '{package_id}' not found (404)")
                elif response.status_code == 401:
                    log(f"   ❌ Unauthorized to access packages (401)")
                elif response.status_code == 403:
                    log(f"   ❌ Forbidden to access packages (403)")
                    
            except Exception as e:
                log(f"   ❌ Error checking {endpoint}: {e}")
        
        return False
        
    except Exception as e:
        log(f"❌ Package check error: {e}")
        return False

def check_write_permissions(base_url, oauth_token):
    """Check write permissions by testing a minimal create operation"""
    try:
        log("✍️ Testing write permissions...")
        
        # Create a minimal test payload
        test_payload = {
            "Name": "PermissionTest_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
            "Id": "PermissionTest_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
            "PackageId": "ConversionPackages"
        }
        
        headers = {
            "Authorization": f"Bearer {oauth_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "DataServiceVersion": "2.0"
        }
        
        # Try different endpoints
        write_endpoints = [
            "/cpi/api/v1/IntegrationDesigntimeArtifacts",
            "/api/v1/IntegrationDesigntimeArtifacts"
        ]
        
        for endpoint in write_endpoints:
            try:
                log(f"   Testing write to: {base_url}{endpoint}")
                response = requests.post(
                    f"{base_url}{endpoint}",
                    headers=headers,
                    json=test_payload,
                    timeout=30
                )
                
                log(f"   Status: {response.status_code}")
                log(f"   Response: {response.text[:200]}...")
                
                if response.status_code == 201:
                    log(f"   ✅ Write permissions confirmed!")
                    return True
                elif response.status_code == 400:
                    log(f"   ⚠️ Bad request (but write permission exists)")
                    return True
                elif response.status_code == 401:
                    log(f"   ❌ Unauthorized (401)")
                elif response.status_code == 403:
                    log(f"   ❌ Forbidden - no write permissions (403)")
                elif response.status_code == 404:
                    log(f"   ❌ Endpoint not found (404)")
                else:
                    log(f"   ⚠️ Unexpected status: {response.status_code}")
                    
            except Exception as e:
                log(f"   ❌ Error testing {endpoint}: {e}")
        
        return False
        
    except Exception as e:
        log(f"❌ Write permission test error: {e}")
        return False

def check_csrf_token(base_url, oauth_token):
    """Check CSRF token availability"""
    try:
        log("🛡️ Checking CSRF token availability...")
        
        csrf_endpoints = [
            "/cpi/api/v1/IntegrationDesigntimeArtifacts",
            "/api/v1/IntegrationDesigntimeArtifacts",
            "/itspaces/api/1.0/workspace",
            "/api/v1/IntegrationPackages"
        ]
        
        headers = {
            "Authorization": f"Bearer {oauth_token}",
            "X-CSRF-Token": "Fetch",
            "Accept": "application/json"
        }
        
        for endpoint in csrf_endpoints:
            try:
                log(f"   Trying CSRF from: {base_url}{endpoint}")
                response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=30)
                
                csrf_token = response.headers.get("X-CSRF-Token")
                log(f"   Status: {response.status_code}, CSRF: {csrf_token or 'None'}")
                
                if csrf_token and csrf_token != "Required":
                    log(f"   ✅ CSRF token obtained: {csrf_token[:20]}...")
                    return csrf_token
                    
            except Exception as e:
                log(f"   ❌ Error getting CSRF from {endpoint}: {e}")
        
        log("   ❌ No CSRF token found")
        return None
        
    except Exception as e:
        log(f"❌ CSRF check error: {e}")
        return None

def main():
    """Main diagnostic function"""
    tenants = {
        "ITR Internal": {
            "tenant_url": "https://itr-internal-2hco92jx.integrationsuite-cpi034.cfapps.us10-002.hana.ondemand.com",
            "client_id": "sb-3c34b7ea-2323-485e-9324-e9c25bbe72be!b124895|it!b410334",
            "client_secret": "408913ea-83d7-458d-8243-31f15e4a4165$n35ZO3mV4kSJY5TJDcURz0XxgCQ4DjFnrwdv32Wwwxs=",
            "oauth_url": "https://itr-internal-2hco92jx.authentication.us10.hana.ondemand.com/oauth/token",
            "package": "ConversionPackages"
        },
        "Trial": {
            "tenant_url": "https://4728b940trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com",
            "client_id": "sb-09f9c01e-d098-4f72-8b09-b39757ec93a2!b443330|it!b26655",
            "client_secret": "3a96f9f7-f596-48a8-903c-afd54ad9583e$6wFmr1lu8TWwA8OUI2GnRsL4Vie86YcIiUaMBei8zD0=",
            "oauth_url": "https://4728b940trial.authentication.us10.hana.ondemand.com/oauth/token",
            "package": "WithRequestReply"
        }
    }
    
    for tenant_name, config in tenants.items():
        print("=" * 70)
        print(f"🔍 DIAGNOSING TENANT: {tenant_name}")
        print("=" * 70)
        
        # 1. Check OAuth and permissions
        oauth_token = check_oauth_permissions(config)
        if not oauth_token:
            print(f"❌ Skipping {tenant_name} - OAuth failed\n")
            continue
        
        # 2. Check package existence
        package_exists = check_package_existence(config['tenant_url'], oauth_token, config['package'])
        
        # 3. Check CSRF token
        csrf_token = check_csrf_token(config['tenant_url'], oauth_token)
        
        # 4. Check write permissions
        has_write_perms = check_write_permissions(config['tenant_url'], oauth_token)
        
        # Summary
        print("-" * 50)
        print("📋 DIAGNOSTIC SUMMARY:")
        print(f"   🔐 OAuth Token: ✅ Working")
        print(f"   📦 Package '{config['package']}': {'✅ Exists' if package_exists else '❌ Missing'}")
        print(f"   🛡️ CSRF Token: {'✅ Available' if csrf_token else '❌ Missing'}")
        print(f"   ✍️ Write Permissions: {'✅ Granted' if has_write_perms else '❌ Denied'}")
        
        if package_exists and csrf_token and has_write_perms:
            print(f"   🎯 RESULT: ✅ {tenant_name} should work for deployment!")
        else:
            print(f"   🎯 RESULT: ❌ {tenant_name} has configuration issues")
            
        print("")

if __name__ == "__main__":
    main()
