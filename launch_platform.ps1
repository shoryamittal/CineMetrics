# ==============================================================================
# CineMetrics / CPIP - Enterprise Platform PowerShell Launcher
# ==============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   CineMetrics / CPIP - Enterprise Platform Launcher" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "`n[*] Starting Flagship Web SPA on http://localhost:8080 ..." -ForegroundColor Yellow
Start-Process python -ArgumentList "serve_dashboard.py 8080" -WorkingDirectory $baseDir

Write-Host "[*] Starting Streamlit Companion on http://localhost:8501 ..." -ForegroundColor Yellow
Start-Process streamlit -ArgumentList "run app.py --server.headless true --server.port 8501" -WorkingDirectory $baseDir

Start-Sleep -Seconds 3

Write-Host "`n[+] Verification Check:" -ForegroundColor Green
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8080/health" -TimeoutSec 3
    Write-Host "    [✓] Flagship Server: UP (v$($health.version)) at http://localhost:8080" -ForegroundColor Green
} catch {
    Write-Host "    [!] Flagship Server: Starting up..." -ForegroundColor Yellow
}

try {
    $code = (Invoke-WebRequest -Uri "http://localhost:8501/" -UseBasicParsing -TimeoutSec 3).StatusCode
    Write-Host "    [✓] Streamlit App:   HTTP $code at http://localhost:8501" -ForegroundColor Green
} catch {
    Write-Host "    [!] Streamlit App:   Starting up..." -ForegroundColor Yellow
}

Write-Host "`nReady for interactive analytics.`n" -ForegroundColor Cyan
