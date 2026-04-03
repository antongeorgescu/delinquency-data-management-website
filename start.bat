@echo off
echo Starting Delinquency Website...
echo.
echo Please ensure you have installed dependencies first:
echo   cd src\api && pip install -r requirements.txt
echo   cd src\web && npm install
echo.
echo Starting Flask API server...
start "Flask API" cmd /k "cd src\api && python app.py"

echo Waiting for API to start...
timeout /t 3 /nobreak > nul

echo Starting Angular development server...
start "Angular Dev Server" cmd /k "cd src\web && npm start"

echo.
echo Both servers are starting...
echo - API: http://localhost:5000
echo - Frontend: http://localhost:4200
echo.
echo Press any key to exit this script (servers will continue running)
pause > nul