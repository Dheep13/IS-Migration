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
echo Step 1: Setting environment variables for all applications...
echo Setting main API environment variables...
call cf set-env it-resonance-api-wacky-panther-za CORS_ALLOW_CREDENTIALS true
call cf set-env it-resonance-api-wacky-panther-za ANTHROPIC_API_KEY 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
call cf set-env it-resonance-api-wacky-panther-za GITHUB_TOKEN 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

echo Setting iFlow API environment variables...
call cf set-env mulesoft-iflow-api CORS_ALLOW_CREDENTIALS true
call cf set-env mulesoft-iflow-api ANTHROPIC_API_KEY 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
call cf set-env mulesoft-iflow-api GITHUB_TOKEN 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
call cf set-env mulesoft-iflow-api SAP_BTP_TENANT_URL https://4728b940trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com
call cf set-env mulesoft-iflow-api SAP_BTP_CLIENT_ID sb-09f9c01e-d098-4f72-8b09-b39757ec93a2!b443330^|it!b26655
call cf set-env mulesoft-iflow-api SAP_BTP_CLIENT_SECRET 3a96f9f7-f596-48a8-903c-afd54ad9583e$6wFmr1lu8TWwA8OUI2GnRsL4Vie86YcIiUaMBei8zD0=
call cf set-env mulesoft-iflow-api SAP_BTP_OAUTH_URL https://4728b940trial.authentication.us10.hana.ondemand.com/oauth/token
call cf set-env mulesoft-iflow-api SAP_BTP_DEFAULT_PACKAGE WithRequestReply

echo Setting Gemma3 iFlow API environment variables...
call cf set-env mulesoft-iflow-api-gemma3 CORS_ALLOW_CREDENTIALS true
call cf set-env mulesoft-iflow-api-gemma3 RUNPOD_API_KEY %RUNPOD_API_KEY%
call cf set-env mulesoft-iflow-api-gemma3 RUNPOD_ENDPOINT_ID s5unaaduyy7otl
call cf set-env mulesoft-iflow-api-gemma3 GITHUB_TOKEN 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

echo.
echo Step 2: Building frontend for production...
cd IFA-Project/frontend
call npm run build
if %ERRORLEVEL% neq 0 (
    echo Frontend build failed!
    exit /b 1
)
echo Frontend built successfully.

echo.
echo Step 3: Deploying main API...
cd ..\..\app
echo Copying production environment file...
copy .env.production .env
echo Setting environment variables for manifest.yml...
set ANTHROPIC_API_KEY=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
set GITHUB_TOKEN=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
echo Deploying to Cloud Foundry...
call cf push
if %ERRORLEVEL% neq 0 (
    echo Main API deployment failed!
    exit /b 1
)
echo Main API deployed successfully.

echo.
echo Step 4: Deploying iFlow API...
cd ..\MuleToIS-API
echo Copying production environment file...
copy .env.production .env
echo Setting environment variables for manifest.yml...
set ANTHROPIC_API_KEY=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
set GITHUB_TOKEN=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
set "SAP_BTP_CLIENT_ID=sb-09f9c01e-d098-4f72-8b09-b39757ec93a2!b443330|it!b26655"
set "SAP_BTP_CLIENT_SECRET=3a96f9f7-f596-48a8-903c-afd54ad9583e$6wFmr1lu8TWwA8OUI2GnRsL4Vie86YcIiUaMBei8zD0="
echo Deploying to Cloud Foundry...
call cf push
if %ERRORLEVEL% neq 0 (
    echo iFlow API deployment failed!
    exit /b 1
)
echo iFlow API deployed successfully.

echo.
echo Step 5: Deploying Gemma3 iFlow API...
cd ..\MuleToIS-API-Gemma3
echo Setting environment variables for manifest.yml...
set "RUNPOD_API_KEY=%RUNPOD_API_KEY%"
set RUNPOD_ENDPOINT_ID=s5unaaduyy7otl
set GITHUB_TOKEN=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
echo Deploying to Cloud Foundry...
call cf push
if %ERRORLEVEL% neq 0 (
    echo Gemma3 iFlow API deployment failed!
    exit /b 1
)
echo Gemma3 iFlow API deployed successfully.

echo.
echo Step 6: Deploying frontend...
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
echo iFlow API (Anthropic): https://mulesoft-iflow-api.cfapps.us10-001.hana.ondemand.com
echo iFlow API (Gemma3): https://mulesoft-iflow-api-gemma3.cfapps.us10-001.hana.ondemand.com
echo Frontend: https://ifa-frontend.cfapps.us10-001.hana.ondemand.com
echo.
echo Opening application in browser...
start https://ifa-frontend.cfapps.us10-001.hana.ondemand.com
