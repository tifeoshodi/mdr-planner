@echo off
echo Starting MDR Management System - All Three Applications
echo ========================================================
echo.
echo App 1: Portfolio Manager will run on http://localhost:5001
echo App 2: Scheduler will run on http://localhost:5002
echo App 3: Discipline Dashboard will run on http://localhost:5003
echo.
echo Press Ctrl+C in each window to stop the apps
echo.
pause

start "App 1: Portfolio Manager" cmd /k "cd app1_portfolio_manager & python app.py"
timeout /t 2 /nobreak >nul

start "App 2: Scheduler" cmd /k "cd app2_scheduler & python app.py"
timeout /t 2 /nobreak >nul

start "App 3: Discipline Dashboard" cmd /k "cd app3_discipline_dashboard & python app.py"

echo.
echo All apps started! Check the opened windows.
echo.
pause

