@echo off
echo ===== IT Resonance Environment Switcher =====

if "%1"=="" (
    echo Usage: set-env.bat [development^|production]
    echo.
    echo Examples:
    echo   set-env.bat development   - Set development environment
    echo   set-env.bat production    - Set production environment
    exit /b 1
)

set ENV=%1

if /i "%ENV%"=="development" (
    echo Setting up DEVELOPMENT environment...

    REM Set environment variables
    set FLASK_ENV=development

    echo Environment variables set:
    echo   FLASK_ENV=development

    echo.
    echo To start the main API:
    echo   cd app
    echo   set FLASK_ENV=development
    echo   python app.py

    echo.
    echo To start the iFlow API:
    echo   cd MuleToIS-API
    echo   set FLASK_ENV=development
    echo   python app.py

    echo.
    echo To start the frontend:
    echo   cd IFA-Project/frontend
    echo   npm run dev
) else if /i "%ENV%"=="production" (
    echo Setting up PRODUCTION environment...

    REM Set environment variables
    set FLASK_ENV=production

    echo Environment variables set:
    echo   FLASK_ENV=production

    echo.
    echo To start the main API:
    echo   cd app
    echo   set FLASK_ENV=production
    echo   python app.py

    echo.
    echo To start the iFlow API:
    echo   cd MuleToIS-API
    echo   set FLASK_ENV=production
    echo   python app.py

    echo.
    echo To start the frontend:
    echo   cd IFA-Project/frontend
    echo   npm run build
    echo   npm run preview
) else (
    echo Invalid environment: %ENV%
    echo Valid options are: development, production
    exit /b 1
)

echo.
echo Environment set to %ENV%
echo.
echo IMPORTANT: This script only sets environment variables for the current command prompt.
echo You need to run this script in each new command prompt window before running the applications.
echo.
echo For convenience, you can create separate batch files for each service:
echo.
echo 1. Create start-main-api-%ENV%.bat:
echo   @echo off
echo   cd app
echo   set FLASK_ENV=%ENV%
echo   python app.py
echo.
echo 2. Create start-iflow-api-%ENV%.bat:
echo   @echo off
echo   cd MuleToIS-API
echo   set FLASK_ENV=%ENV%
echo   python app.py
echo.
echo 3. Create start-frontend-%ENV%.bat:
echo   @echo off
echo   cd IFA-Project/frontend
if /i "%ENV%"=="development" (
echo   npm run dev
) else (
echo   npm run build
echo   npm run preview
)
