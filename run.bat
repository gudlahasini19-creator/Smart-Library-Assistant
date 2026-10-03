@echo off
title Smart Library Assistant - DAA Hackathon
echo ========================================================
echo   Starting Smart Library Assistant (DAA Project)
echo ========================================================
echo.

:: Check if Flask is installed; if not, install it automatically
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Flask is not installed. Installing Flask...
    pip install flask
)

python app.py
pause
