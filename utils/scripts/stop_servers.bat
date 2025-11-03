@echo off
:: Server stop utility for Windows
:: Stops backend and frontend servers

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..
set BACKEND_PID_FILE=%PROJECT_ROOT%\.backend.pid
set FRONTEND_PID_FILE=%PROJECT_ROOT%\.frontend.pid

echo Stopping NsureCat servers...

:: Stop backend
if exist "%BACKEND_PID_FILE%" (
    set /p BACKEND_PID=<"%BACKEND_PID_FILE%"
    tasklist /FI "PID eq %BACKEND_PID%" 2>NUL | find /I /N "python.exe">NUL
    if !errorlevel! equ 0 (
        echo Stopping backend (PID: %BACKEND_PID%)
        taskkill /PID %BACKEND_PID% /F >nul 2>nul
        del "%BACKEND_PID_FILE%" 2>nul
        echo SUCCESS: Backend stopped
    ) else (
        echo WARNING: Backend does not appear to be running
    )
) else (
    echo WARNING: Backend PID file not found
)

:: Stop frontend
if exist "%FRONTEND_PID_FILE%" (
    set /p FRONTEND_PID=<"%FRONTEND_PID_FILE%"
    tasklist /FI "PID eq %FRONTEND_PID%" 2>NUL | find /I /N "python.exe">NUL
    if !errorlevel! equ 0 (
        echo Stopping frontend (PID: %FRONTEND_PID%)
        taskkill /PID %FRONTEND_PID% /F >nul 2>nul
        del "%FRONTEND_PID_FILE%" 2>nul
        echo SUCCESS: Frontend stopped
    ) else (
        echo WARNING: Frontend does not appear to be running
    )
) else (
    echo WARNING: Frontend PID file not found
)

echo SUCCESS: Servers stopped