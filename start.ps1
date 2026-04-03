Write-Host "Starting Delinquency Website..." -ForegroundColor Green
Write-Host ""
Write-Host "Please ensure you have installed dependencies first:" -ForegroundColor Yellow
Write-Host "  cd src\api && pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "  cd src\web && npm install" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Flask API server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd src\api; python app.py"

Write-Host "Waiting for API to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Angular development server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd src\web; npm start"

Write-Host ""
Write-Host "Both servers are starting..." -ForegroundColor Green
Write-Host "- API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "- Frontend: http://localhost:4200" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to exit this script (servers will continue running)" -ForegroundColor Yellow
Read-Host