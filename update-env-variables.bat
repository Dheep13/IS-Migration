@echo off
echo ===== Updating Environment Variables and Restaging =====

echo.
echo Step 1: Setting environment variables for main API...
call cf set-env it-resonance-api-wacky-panther-za ANTHROPIC_API_KEY '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'
call cf set-env it-resonance-api-wacky-panther-za GITHUB_TOKEN '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'

echo.
echo Step 2: Setting environment variables for iFlow API...
call cf set-env mulesoft-iflow-api ANTHROPIC_API_KEY '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'
call cf set-env mulesoft-iflow-api GITHUB_TOKEN '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'

echo.
echo Step 3: Setting SAP BTP environment variables for iFlow API...
call cf set-env mulesoft-iflow-api SAP_BTP_TENANT_URL 'https://4728b940trial.it-cpitrial05.cfapps.us10-001.hana.ondemand.com'
call cf set-env mulesoft-iflow-api SAP_BTP_CLIENT_ID 'sb-09f9c01e-d098-4f72-8b09-b39757ec93a2!b443330|it!b26655'
call cf set-env mulesoft-iflow-api SAP_BTP_CLIENT_SECRET '3a96f9f7-f596-48a8-903c-afd54ad9583e$6wFmr1lu8TWwA8OUI2GnRsL4Vie86YcIiUaMBei8zD0='
call cf set-env mulesoft-iflow-api SAP_BTP_OAUTH_URL 'https://4728b940trial.authentication.us10.hana.ondemand.com/oauth/token'
call cf set-env mulesoft-iflow-api SAP_BTP_DEFAULT_PACKAGE 'WithRequestReply'

echo.
echo Step 4: Restaging main API...
call cf restage it-resonance-api-wacky-panther-za

echo.
echo Step 5: Restaging iFlow API...
call cf restage mulesoft-iflow-api

echo.
echo Environment variables updated and applications restaged successfully!