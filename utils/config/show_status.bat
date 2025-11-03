@echo off
:: Status display utility for Windows
:: Shows current status of all components

set ENV_NAME=nsurecat-env
set BACKEND_PORT=8000
set FRONTEND_PORT=8001
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..
set BACKEND_PID_FILE=%PROJECT_ROOT%\.backend.pid
set FRONTEND_PID_FILE=%PROJECT_ROOT%\.frontend.pid

echo Application status:

:: Environment status
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% equ 0 (
    echo Environment: SUCCESS (%ENV_NAME%)
) else (
    echo Environment: ERROR (Not set up)
)

:: Backend status
if exist "%BACKEND_PID_FILE%" (
    set /p BACKEND_PID=<"%BACKEND_PID_FILE%"
    tasklist /FI "PID eq %BACKEND_PID%" 2>NUL | find /I /N "python.exe">NUL
    if !errorlevel! equ 0 (
        echo Backend: SUCCESS (PID: %BACKEND_PID%, Port: %BACKEND_PORT%)
    ) else (
        echo Backend: ERROR (Stopped)
    )
) else (
    echo Backend: ERROR (Stopped)
)

:: Frontend status
if exist "%FRONTEND_PID_FILE%" (
    set /p FRONTEND_PID=<"%FRONTEND_PID_FILE%"
    tasklist /FI "PID eq %FRONTEND_PID%" 2>NUL | find /I /N "python.exe">NUL
    if !errorlevel! equ 0 (
        echo Frontend: SUCCESS (PID: %FRONTEND_PID%, Port: %FRONTEND_PORT%)
    ) else (
        echo Frontend: ERROR (Stopped)
    )
) else (
    echo Frontend: ERROR (Stopped)
)

echo.
echo URLs:
echo   Backend API: http://localhost:%BACKEND_PORT%
echo   API Docs: http://localhost:%BACKEND_PORT%/docs
echo   Frontend: http://localhost:%FRONTEND_PORT%
echo   Scan Page: http://localhost:%FRONTEND_PORT%/scan.html