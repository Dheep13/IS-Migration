@echo off
echo ========================================
echo Testing SAP Integration Suite Deployment
echo ========================================
echo.

set IFLOW_PATH=BoomiToIS-API\results\c8c471bf-2960-4ada-8c1e-95218cb693fb\IFlow_063df8a9.zip

echo Testing with Trial Account (known working)...
echo.
python standalone_sap_deployer.py "%IFLOW_PATH%" --tenant trial

echo.
echo ========================================
echo.

echo Testing with ITR Internal Account...
echo.
python standalone_sap_deployer.py "%IFLOW_PATH%" --tenant itr_internal

echo.
echo ========================================
echo Testing Complete
echo ========================================
pause
