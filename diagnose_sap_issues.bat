@echo off
echo ========================================
echo SAP Integration Suite Diagnostic Tool
echo ========================================
echo.
echo This will check:
echo - OAuth token permissions
echo - Package existence
echo - Write permissions  
echo - CSRF token availability
echo - API endpoint accessibility
echo.
echo Running diagnostic...
echo.

python sap_permissions_checker.py

echo.
echo ========================================
echo Diagnostic Complete
echo ========================================
pause
