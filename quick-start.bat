@echo off
echo ========================================
echo IFA Project - Quick Start
echo ========================================
echo.
echo What would you like to do?
echo.
echo 1. Setup Local Development Environment
echo 2. Start Local Development Servers
echo 3. Deploy to Production (All Apps)
echo 4. Deploy Single App to Production
echo 5. Check Deployment Status
echo 6. Clean Environment
echo 7. Show Help
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo.
    echo 🏠 Setting up local development environment...
    call deployment\scripts\manage-env.bat setup-local
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo 🚀 Starting local development servers...
    call deployment\scripts\manage-env.bat start-local
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo 🌐 Deploying all applications to production...
    echo ⚠️ This will deploy to Cloud Foundry!
    set /p confirm="Are you sure? (y/N): "
    if /i "%confirm%"=="y" (
        call deployment\scripts\manage-env.bat deploy-all
    ) else (
        echo Deployment cancelled.
    )
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo Available apps:
    echo   main_api    - Main API
    echo   mule_api    - MuleToIS API
    echo   boomi_api   - BoomiToIS API
    echo   frontend    - Frontend Application
    echo.
    set /p app="Enter app name: "
    if not "%app%"=="" (
        echo 🚀 Deploying %app% to production...
        call deployment\scripts\manage-env.bat deploy-single %app%
    ) else (
        echo No app specified.
    )
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo 📊 Checking deployment status...
    call deployment\scripts\manage-env.bat status
    goto :end
)

if "%choice%"=="6" (
    echo.
    echo 🧹 Cleaning environment...
    call deployment\scripts\manage-env.bat clean
    goto :end
)

if "%choice%"=="7" (
    echo.
    echo 📖 IFA Project Quick Start Help
    echo.
    echo Available Scripts:
    echo   quick-start.bat                           - This interactive menu
    echo   deployment\scripts\manage-env.bat         - Environment management
    echo   deployment\scripts\deploy-local.bat       - Setup local environment
    echo   deployment\scripts\deploy-production.bat  - Deploy to production
    echo   deployment\scripts\start-local.bat        - Start local servers
    echo.
    echo Documentation:
    echo   deployment\README.md                      - Complete deployment guide
    echo.
    echo Local URLs:
    echo   Frontend:     http://localhost:3000
    echo   Main API:     http://localhost:5000
    echo   MuleToIS API: http://localhost:5001
    echo   BoomiToIS API: http://localhost:5002
    echo.
    echo Production URLs:
    echo   Frontend:     https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com
    echo   Main API:     https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com
    echo   MuleToIS API: https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com
    echo   BoomiToIS API: https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com
    echo.
    goto :end
)

echo ❌ Invalid choice. Please enter 1-7.

:end
echo.
pause
