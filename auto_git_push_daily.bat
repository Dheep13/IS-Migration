@echo off
setlocal enabledelayedexpansion

echo ========================================
echo AUTOMATED DAILY GIT PUSH
echo ========================================

:: Get current date and time for commit message
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

:: Create log directory if it doesn't exist
if not exist "logs" mkdir logs

:: Set log file with date
set "logfile=logs\auto_git_push_%YYYY%-%MM%-%DD%.log"

echo Starting automated git push at %timestamp% >> "%logfile%"
echo Starting automated git push at %timestamp%

:: Change to project directory (adjust if needed)
cd /d "C:\Users\deepan\OneDrive - IT Resonance\Documents\DheepLearningITR\mule_cf_deployment"

:: Check if we're in a git repository
git status >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Not in a git repository! >> "%logfile%"
    echo ERROR: Not in a git repository!
    goto :end
)

:: Check if there are any changes
git diff-index --quiet HEAD --
if %ERRORLEVEL% equ 0 (
    :: No changes detected
    echo No changes detected - skipping commit >> "%logfile%"
    echo No changes detected - skipping commit
    goto :check_unpushed
)

echo Changes detected, proceeding with commit... >> "%logfile%"
echo Changes detected, proceeding with commit...

:: Add all changes
echo Adding all changes... >> "%logfile%"
git add .
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to add changes >> "%logfile%"
    echo ERROR: Failed to add changes
    goto :end
)

:: Create commit with automated message
set "commit_msg=Automated daily backup - %timestamp%"
echo Committing with message: %commit_msg% >> "%logfile%"
git commit -m "!commit_msg!"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to commit changes >> "%logfile%"
    echo ERROR: Failed to commit changes
    goto :end
)

:check_unpushed
:: Check for unpushed commits
git log origin/main..HEAD --oneline >nul 2>&1
if %ERRORLEVEL% equ 0 (
    :: There are unpushed commits, proceed with push
    echo Pushing to remote repository... >> "%logfile%"
    echo Pushing to remote repository...
    
    git push origin main
    if %ERRORLEVEL% equ 0 (
        echo SUCCESS: Changes pushed successfully >> "%logfile%"
        echo SUCCESS: Changes pushed successfully
    ) else (
        echo ERROR: Failed to push to remote repository >> "%logfile%"
        echo ERROR: Failed to push to remote repository
        echo Check your internet connection and git credentials >> "%logfile%"
        echo Check your internet connection and git credentials
    )
) else (
    echo No unpushed commits found >> "%logfile%"
    echo No unpushed commits found
)

:end
echo Automated git push completed at %timestamp% >> "%logfile%"
echo Automated git push completed
echo ======================================== >> "%logfile%"
echo.

:: Optional: Clean up old log files (keep last 30 days)
forfiles /p logs /s /m *.log /d -30 /c "cmd /c del @path" 2>nul

echo Log saved to: %logfile%
timeout /t 5 