# SAP Integration Suite Standalone Deployer

This standalone script allows you to deploy iFlow ZIP files directly to SAP Integration Suite without needing the full BoomiToIS-API service running.

## 📁 Files Created

- **`standalone_sap_deployer.py`** - Main deployment script
- **`deploy_iflow.bat`** - Windows batch file for easy deployment
- **`SAP_DEPLOYER_USAGE_GUIDE.md`** - This usage guide

## 🚀 Quick Start

### Method 1: Using Batch File (Easiest)
```bash
# Deploy to ITR Internal tenant (default)
deploy_iflow.bat my_iflow.zip

# Deploy to Trial tenant
deploy_iflow.bat my_iflow.zip trial
```

### Method 2: Using Python Script Directly
```bash
# Basic deployment
python standalone_sap_deployer.py my_iflow.zip

# Deploy to specific tenant
python standalone_sap_deployer.py my_iflow.zip --tenant trial

# Custom iFlow ID and package
python standalone_sap_deployer.py my_iflow.zip --iflow-id MyCustomID --package ConversionPackages
```

## 🎯 Available Options

### Tenants
- **`itr_internal`** (default) - ITR Internal tenant with ConversionPackages
- **`trial`** - Trial account with WithRequestReply package

### Command Line Options
```bash
python standalone_sap_deployer.py <iflow_path> [options]

Options:
  --tenant {itr_internal,trial}  Target tenant (default: itr_internal)
  --iflow-id IFLOW_ID           Custom iFlow ID (default: auto-generated)
  --iflow-name IFLOW_NAME       Custom iFlow name (default: filename)
  --package PACKAGE             Target package ID (default: tenant default)
  --list-tenants                List available tenants
```

## 📋 Examples

### Basic Examples
```bash
# Deploy to ITR Internal (default)
python standalone_sap_deployer.py IFlow_12345.zip

# Deploy to Trial account
python standalone_sap_deployer.py IFlow_12345.zip --tenant trial

# List available tenants
python standalone_sap_deployer.py --list-tenants
```

### Advanced Examples
```bash
# Custom iFlow ID and name
python standalone_sap_deployer.py IFlow_12345.zip --iflow-id "MyBoomiConversion" --iflow-name "Boomi to SAP Conversion"

# Deploy to specific package
python standalone_sap_deployer.py IFlow_12345.zip --package "MyCustomPackage"

# Full customization
python standalone_sap_deployer.py IFlow_12345.zip --tenant itr_internal --iflow-id "CustomID" --iflow-name "Custom Name" --package "ConversionPackages"
```

## 🔧 Configuration

The script includes pre-configured tenant settings:

### ITR Internal Tenant
- **URL**: `https://itr-internal-2hco92jx.integrationsuite-cpi034.cfapps.us10-002.hana.ondemand.com`
- **Default Package**: `ConversionPackages`
- **Region**: US10-002

### Trial Tenant
- **URL**: `https://4728b940trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com`
- **Default Package**: `WithRequestReply`
- **Region**: US10-001

## 📊 Output Examples

### Successful Deployment
```
[14:30:15] Deploying iFlow: MyFlow (ID: Generated_MyFlow_20250617_143015) to package: ConversionPackages
[14:30:15] Getting OAuth token...
[14:30:16] OAuth response status: 200
[14:30:16] OAuth token obtained successfully
[14:30:16] Creating authenticated session...
[14:30:17] Session creation response: 200
[14:30:17] Session created successfully
[14:30:17] Reading and encoding iFlow file...
[14:30:17] Read 19854 bytes from file
[14:30:17] File encoded as base64 (26472 characters)
[14:30:17] Creating payload...
[14:30:17] Uploading iFlow...
[14:30:18] Trying upload endpoint: .../api/v1/IntegrationDesigntimeArtifacts
[14:30:19] Upload response status: 201
[14:30:19] ✅ Upload successful!

✅ SUCCESS: iFlow deployed successfully
   iFlow ID: Generated_MyFlow_20250617_143015
   Package: ConversionPackages
   Endpoint: /api/v1/IntegrationDesigntimeArtifacts
```

### Failed Deployment
```
[14:30:15] Getting OAuth token...
[14:30:16] OAuth response status: 401
[14:30:16] Failed to get OAuth token: Unauthorized

❌ FAILED: Failed to get OAuth token
```

## 🔍 Troubleshooting

### Common Issues

1. **File Not Found**
   ```
   ❌ Error: File not found: my_iflow.zip
   ```
   - Check the file path is correct
   - Ensure the ZIP file exists

2. **OAuth Token Failed**
   ```
   ❌ FAILED: Failed to get OAuth token
   ```
   - Check tenant credentials are correct
   - Verify network connectivity

3. **401 Unauthorized**
   ```
   ❌ 401 Unauthorized - Response headers: {...}
   ```
   - Check if package exists in target tenant
   - Verify service account permissions

### Debug Mode
The script provides detailed logging for troubleshooting. All requests and responses are logged with timestamps.

## 🎯 Use Cases

### Testing Deployments
```bash
# Quick test deployment
deploy_iflow.bat test_iflow.zip

# Test on trial account
deploy_iflow.bat test_iflow.zip trial
```

### Batch Deployments
```bash
# Deploy multiple iFlows
for file in *.zip; do python standalone_sap_deployer.py "$file"; done
```

### CI/CD Integration
```bash
# In build pipeline
python standalone_sap_deployer.py generated_iflow.zip --tenant itr_internal --iflow-id "Build_${BUILD_NUMBER}"
```

## 📦 Dependencies

The script requires:
- Python 3.6+
- `requests` library

Install dependencies:
```bash
pip install requests
```

## 🔐 Security Notes

- Credentials are embedded in the script for convenience
- For production use, consider using environment variables
- The script uses session-based authentication for ITR Internal tenant
- OAuth tokens are temporary and automatically refreshed

## 🎉 Benefits

- **Standalone** - No need for full API service
- **Fast** - Direct deployment without intermediate steps
- **Flexible** - Multiple tenant support
- **Debuggable** - Detailed logging for troubleshooting
- **Easy** - Simple command-line interface
