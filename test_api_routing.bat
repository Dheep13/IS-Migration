@echo off
echo ========================================
echo Testing API Routing and Configuration
echo ========================================
echo.

echo Testing API Health Endpoints...
echo.

echo 1. Main API Health:
curl -s https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com/api/health
echo.
echo.

echo 2. MuleToIS-API Health:
curl -s https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
echo.
echo.

echo 3. BoomiToIS-API Health:
curl -s https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/health
echo.
echo.

echo 4. Frontend Health:
curl -s https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com/
echo.
echo.

echo ========================================
echo Testing CORS Configuration...
echo ========================================
echo.

echo Testing CORS preflight for MuleToIS-API:
curl -s -X OPTIONS -H "Origin: https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: Content-Type" https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/generate-iflow
echo.
echo.

echo Testing CORS preflight for BoomiToIS-API:
curl -s -X OPTIONS -H "Origin: https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: Content-Type" https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com/api/generate-iflow
echo.
echo.

echo ========================================
echo Configuration Summary
echo ========================================
echo.
echo ✅ All APIs deployed to EU10-005 region
echo ✅ Frontend: https://ifa-frontend.cfapps.eu10-005.hana.ondemand.com
echo ✅ Main API: https://it-resonance-main-api.cfapps.eu10-005.hana.ondemand.com
echo ✅ MuleToIS-API: https://mule-to-is-api.cfapps.eu10-005.hana.ondemand.com
echo ✅ BoomiToIS-API: https://boomi-to-is-api.cfapps.eu10-005.hana.ondemand.com
echo.
echo Platform Routing:
echo - MuleSoft files → mule-to-is-api
echo - Boomi files → boomi-to-is-api
echo.
echo SAP Integration Suite:
echo - Target: ITR Internal (US10-002)
echo - Package: ConversionPackages
echo.
pause
