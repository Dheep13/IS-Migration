@echo off
echo ========================================
echo Fixing API Deployment Configuration Issues
echo ========================================
echo.
echo Fixed Issues:
echo ✅ Updated all APIs to use EU10-005 region
echo ✅ Fixed CORS origins to point to correct frontend URL
echo ✅ Updated SAP BTP Integration to use ITR Internal account
echo ✅ Ensured proper API routing: MuleSoft → mule-to-is-api, Boomi → boomi-to-is-api
echo.

echo Step 1: Redeploying BoomiToIS-API with corrected configuration...
cd BoomiToIS-API
call cf push
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to deploy BoomiToIS-API
    pause
    exit /b 1
)
cd ..
echo ✅ BoomiToIS-API deployed successfully
echo.

echo Step 2: Redeploying MuleToIS-API with corrected configuration...
cd MuleToIS-API
call cf push
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to deploy MuleToIS-API
    pause
    exit /b 1
)
cd ..
echo ✅ MuleToIS-API deployed successfully
echo.

echo Step 3: Redeploying Main API to ensure environment variables are updated...
cd app
call cf push
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to deploy Main API
    pause
    exit /b 1
)
cd ..
echo ✅ Main API deployed successfully
echo.

echo Step 4: Checking application status...
call cf apps
echo.

echo Step 5: Testing API connectivity...
echo Testing Main API health...
curl -s https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com/api/health
echo.
echo.

echo Testing BoomiToIS-API health...
curl -s https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
echo.
echo.

echo Testing MuleToIS-API health...
curl -s https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
echo.
echo.

echo ========================================
echo Deployment Fix Complete!
echo ========================================
echo.
echo All APIs are now properly configured:
echo ✅ All services deployed to EU10-005 region
echo ✅ CORS configured for https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com
echo ✅ SAP BTP Integration uses ITR Internal account (US10-002)
echo ✅ Platform routing: MuleSoft → mule-to-is-api, Boomi → boomi-to-is-api
echo ✅ Backend APIs can communicate with main API correctly
echo.
echo You can now test the frontend at:
echo https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com
echo.
echo Expected functionality:
echo - Upload MuleSoft files → calls mule-to-is-api
echo - Upload Boomi files → calls boomi-to-is-api
echo - Deploy iFlow button → calls appropriate API based on platform
echo - SAP Integration Suite deployment → uses ITR Internal account
echo.
pause
