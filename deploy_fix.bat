@echo off
echo Fixing API routing issue by deploying missing services...

echo.
echo 1. Deploying Main API...
cd app
cf push -f manifest.yml
if %ERRORLEVEL% neq 0 (
    echo ERROR: Main API deployment failed!
    pause
    exit /b 1
)

echo.
echo 2. Rebuilding and deploying Frontend...
cd ..\IFA-Project\frontend
call npm run build
if %ERRORLEVEL% neq 0 (
    echo ERROR: Frontend build failed!
    pause
    exit /b 1
)

cf push -f manifest.yml
if %ERRORLEVEL% neq 0 (
    echo ERROR: Frontend deployment failed!
    pause
    exit /b 1
)

echo.
echo 3. Testing API connections...
echo Testing Main API...
curl -f https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com/api/health
if %ERRORLEVEL% neq 0 (
    echo WARNING: Main API health check failed
) else (
    echo Main API is healthy
)

echo Testing MuleSoft API...
curl -f https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
if %ERRORLEVEL% neq 0 (
    echo WARNING: MuleSoft API health check failed
) else (
    echo MuleSoft API is healthy
)

echo Testing Boomi API...
curl -f https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
if %ERRORLEVEL% neq 0 (
    echo WARNING: Boomi API health check failed
) else (
    echo Boomi API is healthy
)

echo.
echo Deployment complete! 
echo Frontend: https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com
echo Main API: https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com
echo MuleSoft API: https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com
echo Boomi API: https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com

echo.
echo The iFlow generation button should now work properly!
pause 