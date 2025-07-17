@echo off
REM IMigrate Platform - Consolidated Management Script
REM This script consolidates all project management operations

echo ========================================
echo IMigrate Platform - Project Management
echo ========================================
echo.

if "%1"=="" goto :show_menu
if "%1"=="quick-start" goto :quick_start
if "%1"=="deploy" goto :deploy
if "%1"=="test" goto :test
if "%1"=="git-push" goto :git_push
if "%1"=="restart" goto :restart
if "%1"=="clean" goto :clean
goto :show_help

:show_menu
echo What would you like to do?
echo.
echo 1. Quick Start (Setup and run locally)
echo 2. Deploy to Production
echo 3. Test API Routing
echo 4. Git Push (Daily automation)
echo 5. Restart Frontend
echo 6. Clean Environment
echo 7. Show Help
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto :quick_start
if "%choice%"=="2" goto :deploy
if "%choice%"=="3" goto :test
if "%choice%"=="4" goto :git_push
if "%choice%"=="5" goto :restart
if "%choice%"=="6" goto :clean
if "%choice%"=="7" goto :show_help
echo Invalid choice. Please enter 1-7.
goto :end

:quick_start
echo 🚀 Starting Quick Start...
if exist "quick-start.bat" (
    call quick-start.bat
) else (
    echo Setting up local development environment...
    echo.
    echo 1. Starting Main API (Port 5000)...
    cd app
    start "Main API" cmd /k "python app.py"
    cd ..
    
    echo 2. Starting BoomiToIS API (Port 5003)...
    cd BoomiToIS-API
    start "BoomiToIS API" cmd /k "python app.py"
    cd ..
    
    echo 3. Starting Frontend (Port 3000)...
    cd IFA-Project/frontend
    start "Frontend" cmd /k "npm run dev"
    cd ../..
    
    echo.
    echo ✅ All services started!
    echo Frontend: http://localhost:3000
    echo Main API: http://localhost:5000
    echo BoomiToIS API: http://localhost:5003
)
goto :end

:deploy
echo 🌐 Deploying to Production...
if exist "deploy_fix.bat" (
    call deploy_fix.bat
) else (
    echo Deploying to Cloud Foundry...
    cf push
)
goto :end

:test
echo 🔍 Testing API Routing...
if exist "test_api_routing.bat" (
    call test_api_routing.bat
) else (
    echo Testing API endpoints...
    curl -f http://localhost:5000/api/health || echo Main API not responding
    curl -f http://localhost:5003/api/health || echo BoomiToIS API not responding
    curl -f http://localhost:3000 || echo Frontend not responding
)
goto :end

:git_push
echo 📤 Performing Git Push...
if exist "auto_git_push_daily.bat" (
    call auto_git_push_daily.bat
) else (
    echo Pushing to Git repository...
    git add .
    git commit -m "Automated daily push - %date% %time%"
    git push origin main
)
goto :end

:restart
echo 🔄 Restarting Frontend...
if exist "restart_frontend.bat" (
    call restart_frontend.bat
) else (
    echo Restarting frontend service...
    taskkill /f /im node.exe 2>nul
    cd IFA-Project/frontend
    start "Frontend" cmd /k "npm run dev"
    cd ../..
)
goto :end

:clean
echo 🧹 Cleaning Environment...
echo Stopping all services...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
echo Cleaning temporary files...
if exist "app/results" rmdir /s /q "app/results"
if exist "app/uploads" rmdir /s /q "app/uploads"
if exist "BoomiToIS-API/results" rmdir /s /q "BoomiToIS-API/results"
if exist "BoomiToIS-API/uploads" rmdir /s /q "BoomiToIS-API/uploads"
echo ✅ Environment cleaned!
goto :end

:show_help
echo.
echo 📖 IMigrate Platform - Help
echo.
echo Usage: manage-project.bat [command]
echo.
echo Available Commands:
echo   quick-start    Setup and run all services locally
echo   deploy         Deploy all applications to production
echo   test          Test API routing and connectivity
echo   git-push      Perform automated git push
echo   restart       Restart frontend service
echo   clean         Clean environment and stop services
echo.
echo Interactive Mode:
echo   Run without parameters for interactive menu
echo.
echo Documentation:
echo   README.md           - Project overview and quick start
echo   HOW_TO_RUN_GUIDE.md - Complete setup instructions
echo   PROJECT_DOCS.md     - Technical details and architecture
echo.
echo Service URLs (Local):
echo   Frontend:     http://localhost:3000
echo   Main API:     http://localhost:5000
echo   BoomiToIS API: http://localhost:5003
echo.
echo Service URLs (Production):
echo   Frontend:     https://ifa-project.cfapps.eu10.hana.ondemand.com
echo   Main API:     https://mule2is-api.cfapps.eu10.hana.ondemand.com
echo   BoomiToIS API: https://boomitois-api.cfapps.eu10.hana.ondemand.com
echo.
goto :end

:end
echo.
pause
