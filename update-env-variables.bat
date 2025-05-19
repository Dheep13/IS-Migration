@echo off
echo ===== Updating Environment Variables and Restaging =====

echo.
echo Step 1: Setting environment variables for main API...
call cf set-env it-resonance-api-wacky-panther-za ANTHROPIC_API_KEY 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
call cf set-env it-resonance-api-wacky-panther-za GITHUB_TOKEN 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

echo.
echo Step 2: Setting environment variables for iFlow API...
call cf set-env mulesoft-iflow-api ANTHROPIC_API_KEY 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
call cf set-env mulesoft-iflow-api GITHUB_TOKEN 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

echo.
echo Step 3: Restaging main API...
call cf restage it-resonance-api-wacky-panther-za

echo.
echo Step 4: Restaging iFlow API...
call cf restage mulesoft-iflow-api

echo.
echo Environment variables updated and applications restaged successfully!