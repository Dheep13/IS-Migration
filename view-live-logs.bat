@echo off
echo ========================================
echo IMigrate Platform - Live Log Viewer
echo ========================================

:: Check if services are running
echo Checking running services...

tasklist /FI "WINDOWTITLE eq Main API*" 2>NUL | find /I "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Main API is running
) else (
    echo ❌ Main API not found
)

tasklist /FI "WINDOWTITLE eq BoomiToIS API*" 2>NUL | find /I "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ BoomiToIS API is running
) else (
    echo ❌ BoomiToIS API not found
)

tasklist /FI "WINDOWTITLE eq Gemma-3 API*" 2>NUL | find /I "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Gemma-3 API is running
) else (
    echo ❌ Gemma-3 API not found
)

tasklist /FI "WINDOWTITLE eq Frontend*" 2>NUL | find /I "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Frontend is running
) else (
    echo ❌ Frontend not found
)

echo.
echo ========================================
echo Choose log viewing option:
echo ========================================
echo 1. View latest unified log file
echo 2. Monitor Main API logs (real-time)
echo 3. Monitor BoomiToIS API logs (real-time)
echo 4. Monitor Gemma-3 API logs (real-time)
echo 5. Monitor Frontend logs (real-time)
echo 6. View all logs side-by-side (4 windows)
echo 7. Create new unified log session
echo ========================================

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto view_unified
if "%choice%"=="2" goto monitor_main
if "%choice%"=="3" goto monitor_boomi
if "%choice%"=="4" goto monitor_gemma
if "%choice%"=="5" goto monitor_frontend
if "%choice%"=="6" goto view_all
if "%choice%"=="7" goto create_unified

echo Invalid choice. Exiting...
goto end

:view_unified
echo Looking for latest unified log...
for /f "delims=" %%i in ('dir /b /o-d logs\unified_*.log 2^>nul') do (
    echo Opening: logs\%%i
    start "Unified Log Viewer" cmd /c "powershell Get-Content logs\%%i -Wait -Tail 100"
    goto end
)
echo No unified log files found. Run start-with-unified-logs.bat first.
goto end

:monitor_main
echo Monitoring Main API logs...
start "Main API Logs" cmd /c "cd app && python -u app.py"
goto end

:monitor_boomi
echo Monitoring BoomiToIS API logs...
start "BoomiToIS API Logs" cmd /c "cd BoomiToIS-API && python -u app.py"
goto end

:monitor_gemma
echo Monitoring Gemma-3 API logs...
start "Gemma-3 API Logs" cmd /c "cd MuleToIS-API-Gemma3 && python -u app.py"
goto end

:monitor_frontend
echo Monitoring Frontend logs...
start "Frontend Logs" cmd /c "cd IFA-Project\frontend && npm run dev"
goto end

:view_all
echo Opening all service logs in separate windows...
start "Main API" cmd /c "cd app && python -u app.py"
timeout /t 2 /nobreak > nul
start "BoomiToIS API" cmd /c "cd BoomiToIS-API && python -u app.py"
timeout /t 2 /nobreak > nul
start "Gemma-3 API" cmd /c "cd MuleToIS-API-Gemma3 && python -u app.py"
timeout /t 2 /nobreak > nul
start "Frontend" cmd /c "cd IFA-Project\frontend && npm run dev"
echo All services started in separate windows!
goto end

:create_unified
echo Creating new unified logging session...
call start-with-unified-logs.bat
goto end

:end
echo.
echo Tip: To filter logs for image processing, look for:
echo   - "Starting image extraction"
echo   - "Found image"
echo   - "Vision analysis"
echo   - "image_count"
echo.
pause
