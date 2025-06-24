@echo off
echo Starting Dell Boomi to SAP Integration Suite API (Development Mode)
echo.

REM Set environment to development
call set-env-development.bat

REM Navigate to Boomi API directory
cd /d "%~dp0BoomiToIS-API"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Set Flask environment variables
set FLASK_APP=app.py
set FLASK_ENV=development
set PORT=5003

echo.
echo ========================================
echo Dell Boomi to SAP Integration Suite API
echo ========================================
echo Environment: Development
echo Port: 5003
echo Platform: Dell Boomi
echo ========================================
echo.

REM Start the Flask application
python app.py

pause
