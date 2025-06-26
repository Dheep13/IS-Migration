# API Configuration Issues and Fixes

## Issues Identified

### 1. Region Mismatch
**Problem**: Your applications were deployed across different Cloud Foundry regions, causing communication failures.

- **Frontend & Main API**: Deployed to `eu10-005.hana.ondemand.com` ✅
- **BoomiToIS-API & MuleToIS-API**: Configured to call main API at `us10-001.hana.ondemand.com` ❌

### 2. Incorrect CORS Configuration
**Problem**: Backend APIs had CORS origins pointing to the wrong region.

- **Expected**: `https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com`
- **Actual**: `https://ifa-frontend.cfapps.us10-001.hana.ondemand.com`

### 3. Main API URL Mismatch
**Problem**: Backend APIs were trying to communicate with a non-existent main API URL.

- **Expected**: `https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com`
- **Actual**: `https://it-resonance-api-wacky-panther-za.cfapps.us10-001.hana.ondemand.com`

## Files Fixed

### 1. BoomiToIS-API Configuration
- `BoomiToIS-API/manifest.yml` - Updated MAIN_API_URL and CORS_ORIGIN
- `BoomiToIS-API/.env.production` - Updated environment variables

### 2. MuleToIS-API Configuration  
- `MuleToIS-API/manifest.yml` - Updated MAIN_API_URL and CORS_ORIGIN
- `MuleToIS-API/.env.production` - Updated environment variables

### 3. MuleToIS-API-Gemma3 Configuration
- `MuleToIS-API-Gemma3/manifest.yml` - Updated MAIN_API_URL and CORS_ORIGIN

## Deployment Steps

1. **Run the fix script**:
   ```bash
   fix_api_deployment.bat
   ```

2. **Or deploy manually**:
   ```bash
   # Deploy BoomiToIS-API
   cd BoomiToIS-API
   cf push
   
   # Deploy MuleToIS-API
   cd ../MuleToIS-API
   cf push
   ```

## Verification

After deployment, verify the fixes:

1. **Check app status**: `cf apps`
2. **Test API health endpoints**:
   - Main API: https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com/api/health
   - BoomiToIS-API: https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
   - MuleToIS-API: https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health

3. **Test frontend**: https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com

## Expected Results

After these fixes:
- ✅ All APIs will be in the same region (EU10-005)
- ✅ CORS will allow frontend to call backend APIs
- ✅ Backend APIs can communicate with main API
- ✅ iFlow generation should work for both Boomi and MuleSoft platforms
- ✅ No more 404 errors when calling between services
- ✅ Platform-specific routing: MuleSoft → mule-to-is-api, Boomi → boomi-to-is-api
- ✅ SAP Integration Suite deployment uses ITR Internal account (US10-002)
- ✅ Deploy iFlow button calls appropriate backend API based on platform selection

## Platform Routing Logic

### Frontend Platform Selection
- **MuleSoft Platform**: Frontend calls `mule-to-is-api.cfapps.eu10-005.hana.ondemand.com`
- **Boomi Platform**: Frontend calls `boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com`

### iFlow Generation Flow
1. User uploads files and selects platform (MuleSoft/Boomi)
2. Main API processes documentation based on platform
3. Frontend calls appropriate backend API for iFlow generation:
   - MuleSoft: `POST /api/generate-iflow` → mule-to-is-api
   - Boomi: `POST /api/generate-iflow` → boomi-to-is-api
4. Deploy iFlow button calls same backend API for SAP deployment

### SAP Integration Suite Deployment
- **Target**: ITR Internal account (US10-002 region)
- **Credentials**: Updated to use ITR Internal service key
- **Package**: ConversionPackages (default)

## Root Cause

The issue was caused by:
1. **Inconsistent deployment regions** - Some apps deployed to EU10-005, others configured for US10-001
2. **Copy-paste configuration errors** - Old URLs from previous deployments were not updated
3. **Missing environment variable synchronization** - .env.production files didn't match manifest.yml files
4. **Outdated SAP BTP credentials** - Still using trial account instead of ITR Internal
5. **Mixed API routing** - Frontend not consistently calling correct backend APIs
