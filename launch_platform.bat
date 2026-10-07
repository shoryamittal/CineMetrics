@echo off
title CineMetrics CPIP - Launch All Servers
echo ======================================================================
echo    CineMetrics / CPIP - Enterprise Platform Launcher
echo ======================================================================
echo.
echo [*] Starting Flagship Web SPA on http://localhost:8080 ...
start "CPIP Flagship Web Server (Port 8080)" cmd /k python serve_dashboard.py 8080

echo [*] Starting Streamlit Companion on http://localhost:8501 ...
start "CPIP Streamlit Dual-Domain (Port 8501)" cmd /k streamlit run app.py --server.headless true --server.port 8501

echo.
echo [+] Both services started in separate console windows!
echo     - Flagship Web Dashboard: http://localhost:8080
echo     - Streamlit Companion:    http://localhost:8501
echo.
pause
