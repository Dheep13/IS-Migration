@echo off
echo Restarting Frontend with Updated Configuration...
echo.
echo Updated iFlow API to use port 5003 (BoomiToIS-API)
echo.

cd IFA-Project\frontend
echo Starting frontend development server...
npm run dev
