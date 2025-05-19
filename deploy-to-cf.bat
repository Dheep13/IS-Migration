@echo off
echo ===== IT Resonance Cloud Foundry Deployment =====

echo Checking if logged in to Cloud Foundry...
cf target
if %ERRORLEVEL% neq 0 (
    echo You need to log in to Cloud Foundry first.
    echo Run: cf login -a https://api.cf.us10-001.hana.ondemand.com
    exit /b 1
)

echo.
echo Setting environment to production...
set FLASK_ENV=production

echo.
echo Step 1: Building frontend for production...
cd IFA-Project/frontend
call npm run build
if %ERRORLEVEL% neq 0 (
    echo Frontend build failed!
    exit /b 1
)
echo Frontend built successfully.

echo.
echo Step 2: Deploying main API...
cd ..\..\app
echo Copying production environment file...
copy .env.production .env
echo Setting environment variables...
call cf set-env it-resonance-api-wacky-panther-za CORS_ALLOW_CREDENTIALS true
call cf set-env it-resonance-api-wacky-panther-za ANTHROPIC_API_KEY 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
call cf set-env it-resonance-api-wacky-panther-za GITHUB_TOKEN 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
echo Deploying to Cloud Foundry...
call cf push
if %ERRORLEVEL% neq 0 (
    echo Main API deployment failed!
    exit /b 1
)
echo Restaging Main API to ensure environment variables are applied...
call cf restage it-resonance-api-wacky-panther-za
if %ERRORLEVEL% neq 0 (
    echo Main API restage failed!
    exit /b 1
)
echo Main API deployed successfully.

echo.
echo Step 3: Deploying iFlow API...
cd ..\MuleToIS-API
echo Copying production environment file...
copy .env.production .env
echo Setting environment variables...
call cf set-env mulesoft-iflow-api CORS_ALLOW_CREDENTIALS true
call cf set-env mulesoft-iflow-api ANTHROPIC_API_KEY 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
call cf set-env mulesoft-iflow-api GITHUB_TOKEN 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
echo Deploying to Cloud Foundry...
call cf push
if %ERRORLEVEL% neq 0 (
    echo iFlow API deployment failed!
    exit /b 1
)
echo Restaging iFlow API to ensure environment variables are applied...
call cf restage mulesoft-iflow-api
if %ERRORLEVEL% neq 0 (
    echo iFlow API restage failed!
    exit /b 1
)
echo iFlow API deployed successfully.

echo.
echo Step 4: Deploying frontend...
cd ..\IFA-Project\frontend
echo Deploying to Cloud Foundry...
call cf push
if %ERRORLEVEL% neq 0 (
    echo Frontend deployment failed!
    exit /b 1
)
echo Frontend deployed successfully.

echo.
echo All components deployed successfully!
echo.
echo Main API: https://it-resonance-api-wacky-panther-za.cfapps.us10-001.hana.ondemand.com
echo iFlow API: https://mulesoft-iflow-api.cfapps.us10-001.hana.ondemand.com
echo Frontend: https://ifa-frontend.cfapps.us10-001.hana.ondemand.com
echo.
echo Opening application in browser...
start https://ifa-frontend.cfapps.us10-001.hana.ondemand.com
