@echo off
:: Server startup utility for Windows
:: Starts backend and frontend servers

set ENV_NAME=nsurecat-env
set BACKEND_PORT=8000
set FRONTEND_PORT=8001
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..
set BACKEND_PID_FILE=%PROJECT_ROOT%\.backend.pid
set FRONTEND_PID_FILE=%PROJECT_ROOT%\.frontend.pid

echo Starting NsureCat servers...

:: Check if environment exists
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Environment '%ENV_NAME%' does not exist. Run setup first.
    exit /b 1
)

cd /d "%PROJECT_ROOT%"

:: Check if backend is already running
if exist "%BACKEND_PID_FILE%" (
    set /p BACKEND_PID=<"%BACKEND_PID_FILE%"
    tasklist /FI "PID eq %BACKEND_PID%" 2>NUL | find /I /N "python.exe">NUL
    if !errorlevel! equ 0 (
        echo WARNING: Backend appears to be already running (PID: %BACKEND_PID%)
        goto :check_frontend
    )
)

echo Starting FastAPI backend on port %BACKEND_PORT%
start /B conda run -n "%ENV_NAME%" uvicorn src.backend.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE /NH ^| findstr /C:"python.exe"') do set BACKEND_PID=%%i
echo !BACKEND_PID! > "%BACKEND_PID_FILE%"
echo SUCCESS: Backend started (PID: !BACKEND_PID!)

:check_frontend
:: Check if frontend is already running
if exist "%FRONTEND_PID_FILE%" (
    set /p FRONTEND_PID=<"%FRONTEND_PID_FILE%"
    tasklist /FI "PID eq %FRONTEND_PID%" 2>NUL | find /I /N "python.exe">NUL
    if !errorlevel! equ 0 (
        echo WARNING: Frontend appears to be already running (PID: %FRONTEND_PID%)
        goto :done
    )
)

echo Starting frontend server on port %FRONTEND_PORT%
cd src\frontend
start /B python -m http.server %FRONTEND_PORT%
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE /NH ^| findstr /C:"python.exe"') do set FRONTEND_PID=%%i
echo !FRONTEND_PID! > "..\%FRONTEND_PID_FILE%"
cd ..
echo SUCCESS: Frontend started (PID: !FRONTEND_PID!)

:done
echo SUCCESS: Servers started
echo Backend: http://localhost:%BACKEND_PORT%
echo Frontend: http://localhost:%FRONTEND_PORT%