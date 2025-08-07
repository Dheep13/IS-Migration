@echo off
echo ========================================
echo IS-Migration Platform - Start All Servers
echo ========================================
echo.

:: Set colors for better visibility
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

echo %BLUE%Starting all servers for IS-Migration platform...%RESET%
echo.

:: Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Node.js is not installed or not in PATH%RESET%
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Python is not installed or not in PATH%RESET%
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo %GREEN%Prerequisites check passed!%RESET%
echo.

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo %YELLOW%Starting servers in background...%RESET%
echo.

:: Start Main API (Documentation Generator) - Port 5000
echo %BLUE%1. Starting Main API (Port 5000)...%RESET%
start "Main API - Port 5000" cmd /k "cd /d app && python app.py"
timeout /t 3 /nobreak >nul

:: Start BoomiToIS API - Port 5003
echo %BLUE%2. Starting BoomiToIS API (Port 5003)...%RESET%
start "BoomiToIS API - Port 5003" cmd /k "cd /d BoomiToIS-API && python app.py"
timeout /t 3 /nobreak >nul

:: Start MuleToIS API - Port 5001
echo %BLUE%3. Starting MuleToIS API (Port 5001)...%RESET%
start "MuleToIS API - Port 5001" cmd /k "cd /d MuleToIS-API && python app.py"
timeout /t 3 /nobreak >nul

:: Start Gemma-3 API - Port 5002
echo %BLUE%4. Starting Gemma-3 API (Port 5002)...%RESET%
start "Gemma-3 API - Port 5002" cmd /k "cd /d MuleToIS-API-Gemma3 && python app.py"
timeout /t 3 /nobreak >nul

:: Start Frontend - Port 5173
echo %BLUE%5. Starting Frontend (Port 5173)...%RESET%
start "Frontend - Port 5173" cmd /k "cd /d IFA-Project\frontend && npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo %GREEN%========================================%RESET%
echo %GREEN%All servers are starting up!%RESET%
echo %GREEN%========================================%RESET%
echo.
echo %YELLOW%Server URLs:%RESET%
echo %BLUE%Frontend:        %RESET%http://localhost:5173
echo %BLUE%Main API:        %RESET%http://localhost:5000
echo %BLUE%BoomiToIS API:   %RESET%http://localhost:5003
echo %BLUE%MuleToIS API:    %RESET%http://localhost:5001
echo %BLUE%Gemma-3 API:     %RESET%http://localhost:5002
echo.
echo %YELLOW%Note: Each server is running in its own window.%RESET%
echo %YELLOW%Close individual windows to stop specific servers.%RESET%
echo.
echo %GREEN%Waiting 10 seconds for all servers to fully start...%RESET%
timeout /t 10 /nobreak >nul

echo.
echo %GREEN%Opening frontend in browser...%RESET%
start http://localhost:5173

echo.
echo %GREEN%All servers started successfully!%RESET%
echo %YELLOW%Press any key to exit this launcher...%RESET%
pause >nul
