@echo off
echo ========================================
echo SAP Integration Suite iFlow Deployer
echo ========================================
echo.

if "%1"=="" (
    echo Usage: deploy_iflow.bat ^<iflow_zip_path^> [tenant]
    echo.
    echo Examples:
    echo   deploy_iflow.bat my_iflow.zip
    echo   deploy_iflow.bat my_iflow.zip trial
    echo   deploy_iflow.bat my_iflow.zip itr_internal
    echo.
    echo Available tenants:
    python standalone_sap_deployer.py --list-tenants
    goto :end
)

set IFLOW_PATH=%1
set TENANT=%2

if "%TENANT%"=="" (
    set TENANT=itr_internal
)

echo Deploying: %IFLOW_PATH%
echo Target: %TENANT%
echo.

python standalone_sap_deployer.py "%IFLOW_PATH%" --tenant %TENANT%

:end
pause
