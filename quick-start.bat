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
    echo Installing dependencies...
    echo.
    echo Installing Main API dependencies...
    cd app
    pip install -r requirements.txt
    cd ..
    echo.
    echo Installing BoomiToIS API dependencies...
    cd BoomiToIS-API
    pip install -r requirements.txt
    cd ..
    echo.
    echo Installing Frontend dependencies...
    cd IFA-Project\frontend
    npm install
    cd ..\..
    echo.
    echo ✅ Setup complete!
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo 🚀 Starting local development servers...
    echo.
    echo Starting Main API (Port 5000)...
    cd app
    start "Main API" cmd /k "python app.py"
    cd ..
    timeout /t 2 /nobreak >nul
    echo.
    echo Starting BoomiToIS API (Port 5003)...
    cd BoomiToIS-API
    start "BoomiToIS API" cmd /k "python app.py"
    cd ..
    timeout /t 2 /nobreak >nul
    echo.
    echo Starting Frontend (Port 3000)...
    cd IFA-Project\frontend
    start "Frontend" cmd /k "npm run dev"
    cd ..\..
    echo.
    echo ✅ All services started!
    echo Frontend: http://localhost:3000
    echo Main API: http://localhost:5000
    echo BoomiToIS API: http://localhost:5003
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo 🌐 Deploying all applications to production...
    echo ⚠️ This will deploy to Cloud Foundry!
    set /p confirm="Are you sure? (y/N): "
    if /i "%confirm%"=="y" (
        echo Deploying Main API...
        cd app
        cf push
        cd ..
        echo.
        echo Deploying BoomiToIS API...
        cd BoomiToIS-API
        cf push
        cd ..
        echo.
        echo Deploying Frontend...
        cd IFA-Project\frontend
        npm run build
        cf push
        cd ..\..
        echo ✅ All applications deployed!
    ) else (
        echo Deployment cancelled.
    )
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo Available apps:
    echo   main_api    - Main API (app folder)
    echo   boomi_api   - BoomiToIS API (BoomiToIS-API folder)
    echo   frontend    - Frontend Application (IFA-Project/frontend folder)
    echo.
    set /p app="Enter app name: "
    if "%app%"=="main_api" (
        echo 🚀 Deploying Main API...
        cd app
        cf push
        cd ..
    ) else (
        if "%app%"=="boomi_api" (
            echo 🚀 Deploying BoomiToIS API...
            cd BoomiToIS-API
            cf push
            cd ..
        ) else (
            if "%app%"=="frontend" (
                echo 🚀 Deploying Frontend...
                cd IFA-Project\frontend
                npm run build
                cf push
                cd ..\..
            ) else (
                echo Invalid app name. Please use: main_api, boomi_api, or frontend
            )
        )
    )
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo 📊 Checking deployment status...
    echo Checking Cloud Foundry apps...
    cf apps
    goto :end
)

if "%choice%"=="6" (
    echo.
    echo 🧹 Cleaning environment...
    echo Stopping local services...
    taskkill /f /im python.exe 2>nul
    taskkill /f /im node.exe 2>nul
    echo Cleaning temporary files...
    if exist "app\results" rmdir /s /q "app\results"
    if exist "app\uploads" rmdir /s /q "app\uploads"
    if exist "BoomiToIS-API\results" rmdir /s /q "BoomiToIS-API\results"
    if exist "BoomiToIS-API\uploads" rmdir /s /q "BoomiToIS-API\uploads"
    echo ✅ Environment cleaned!
    goto :end
)

if "%choice%"=="7" (
    echo.
    echo 📖 IMigrate Platform Quick Start Help
    echo.
    echo Available Scripts:
    echo   quick-start.bat       - This interactive menu
    echo   manage-project.bat    - Consolidated project management
    echo.
    echo Documentation:
    echo   README.md             - Main project overview
    echo   HOW_TO_RUN_GUIDE.md   - Complete usage instructions
    echo   PROJECT_DOCS.md       - Technical details and architecture
    echo.
    echo Local URLs:
    echo   Frontend:     http://localhost:3000
    echo   Main API:     http://localhost:5000
    echo   BoomiToIS API: http://localhost:5003
    echo.
    echo Production URLs:
    echo   Frontend:     https://ifa-project.cfapps.eu10.hana.ondemand.com
    echo   Main API:     https://mule2is-api.cfapps.eu10.hana.ondemand.com
    echo   BoomiToIS API: https://boomitois-api.cfapps.eu10.hana.ondemand.com
    echo.
    echo Project Structure:
    echo   app/                  - Main API (Port 5000)
    echo   BoomiToIS-API/        - Boomi processing service (Port 5003)
    echo   IFA-Project/frontend/ - React frontend (Port 3000)
    echo   archive/              - Archived files
    echo.
    goto :end
)

echo ❌ Invalid choice. Please enter 1-7.

:end
echo.
pause
