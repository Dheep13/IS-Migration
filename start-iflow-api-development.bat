@echo off
echo ===== Starting iFlow API in DEVELOPMENT mode =====
cd MuleToIS-API
set FLASK_ENV=development
python app.py
