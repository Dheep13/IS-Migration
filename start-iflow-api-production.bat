@echo off
echo ===== Starting iFlow API in PRODUCTION mode =====
cd MuleToIS-API
set FLASK_ENV=production
python app.py
