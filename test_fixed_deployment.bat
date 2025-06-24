@echo off
echo ========================================
echo Testing Fixed SAP Deployment Methods
echo ========================================
echo.

set IFLOW_PATH=BoomiToIS-API\results\c8c471bf-2960-4ada-8c1e-95218cb693fb\IFlow_063df8a9.zip

echo Testing Trial Tenant (has CSRF token)...
echo.
python sap_deployer_fixed.py "%IFLOW_PATH%" --tenant trial

echo.
echo ========================================
echo.

echo Testing ITR Internal Tenant (no CSRF)...
echo.
python sap_deployer_fixed.py "%IFLOW_PATH%" --tenant itr_internal

echo.
echo ========================================
echo Testing Complete
echo ========================================
pause
