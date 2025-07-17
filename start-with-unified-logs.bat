@echo off
echo ========================================
echo Starting IMigrate Platform with Unified Logging
echo ========================================

:: Create logs directory
if not exist "logs" mkdir logs

:: Get timestamp for log files
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

:: Set log file paths
set "MAIN_LOG=logs\main-api_%timestamp%.log"
set "BOOMI_LOG=logs\boomi-api_%timestamp%.log"
set "GEMMA_LOG=logs\gemma-api_%timestamp%.log"
set "FRONTEND_LOG=logs\frontend_%timestamp%.log"
set "UNIFIED_LOG=logs\unified_%timestamp%.log"

echo Starting services with logging...
echo Main API logs: %MAIN_LOG%
echo BoomiToIS API logs: %BOOMI_LOG%
echo Gemma-3 API logs: %GEMMA_LOG%
echo Frontend logs: %FRONTEND_LOG%
echo Unified logs: %UNIFIED_LOG%
echo.

:: Start services in background with logging
echo [%time%] Starting Main API... >> %UNIFIED_LOG%
start "Main API" cmd /c "cd app && python app.py > ..\%MAIN_LOG% 2>&1"

timeout /t 3 /nobreak > nul

echo [%time%] Starting BoomiToIS API... >> %UNIFIED_LOG%
start "BoomiToIS API" cmd /c "cd BoomiToIS-API && python app.py > ..\%BOOMI_LOG% 2>&1"

timeout /t 3 /nobreak > nul

echo [%time%] Starting Gemma-3 API... >> %UNIFIED_LOG%
start "Gemma-3 API" cmd /c "cd MuleToIS-API-Gemma3 && python app.py > ..\%GEMMA_LOG% 2>&1"

timeout /t 3 /nobreak > nul

echo [%time%] Starting Frontend... >> %UNIFIED_LOG%
start "Frontend" cmd /c "cd IFA-Project\frontend && npm run dev > ..\..\%FRONTEND_LOG% 2>&1"

timeout /t 5 /nobreak > nul

:: Start log aggregator
echo [%time%] Starting log aggregator... >> %UNIFIED_LOG%
start "Log Aggregator" cmd /c "powershell -Command "& {
    Write-Host 'Log Aggregator Started - Monitoring all services...' -ForegroundColor Green
    while ($true) {
        $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        
        # Check if new log entries exist and append to unified log
        if (Test-Path '%MAIN_LOG%') {
            Get-Content '%MAIN_LOG%' -Tail 10 | ForEach-Object { 
                if ($_ -ne '') { 
                    Add-Content '%UNIFIED_LOG%' \"[$timestamp] [MAIN-API] $_\" 
                }
            }
        }
        
        if (Test-Path '%BOOMI_LOG%') {
            Get-Content '%BOOMI_LOG%' -Tail 10 | ForEach-Object { 
                if ($_ -ne '') { 
                    Add-Content '%UNIFIED_LOG%' \"[$timestamp] [BOOMI-API] $_\" 
                }
            }
        }
        
        if (Test-Path '%GEMMA_LOG%') {
            Get-Content '%GEMMA_LOG%' -Tail 10 | ForEach-Object { 
                if ($_ -ne '') { 
                    Add-Content '%UNIFIED_LOG%' \"[$timestamp] [GEMMA-API] $_\" 
                }
            }
        }
        
        if (Test-Path '%FRONTEND_LOG%') {
            Get-Content '%FRONTEND_LOG%' -Tail 10 | ForEach-Object { 
                if ($_ -ne '') { 
                    Add-Content '%UNIFIED_LOG%' \"[$timestamp] [FRONTEND] $_\" 
                }
            }
        }
        
        Start-Sleep -Seconds 2
    }
}""

echo.
echo ========================================
echo All services started with unified logging!
echo ========================================
echo.
echo Service URLs:
echo - Frontend: http://localhost:3000
echo - Main API: http://localhost:5000
echo - BoomiToIS API: http://localhost:5003
echo - Gemma-3 API: http://localhost:5002
echo.
echo Log Files:
echo - Unified Log: %UNIFIED_LOG%
echo - Individual logs in: logs\ directory
echo.
echo To view unified logs in real-time:
echo   powershell Get-Content %UNIFIED_LOG% -Wait -Tail 50
echo.
echo Press any key to open log viewer...
pause

:: Open log viewer
start "Log Viewer" cmd /c "powershell Get-Content %UNIFIED_LOG% -Wait -Tail 50"
