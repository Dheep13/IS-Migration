@echo off
echo ===== Starting Main API in DEVELOPMENT mode =====
cd app
set FLASK_ENV=development
python app.py
