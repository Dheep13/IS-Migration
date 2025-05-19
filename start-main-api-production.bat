@echo off
echo ===== Starting Main API in PRODUCTION mode =====
cd app
set FLASK_ENV=production
python app.py
