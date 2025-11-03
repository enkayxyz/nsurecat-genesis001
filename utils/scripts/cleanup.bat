@echo off
:: Cleanup utility for Windows
:: Cleans up environment, caches, and stops services

set ENV_NAME=nsurecat-env
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..
set BACKEND_PID_FILE=%PROJECT_ROOT%\.backend.pid
set FRONTEND_PID_FILE=%PROJECT_ROOT%\.frontend.pid

echo Cleaning up...

:: Stop services first
call "%SCRIPT_DIR%\stop_servers.bat"

cd /d "%PROJECT_ROOT%"

:: Remove Python cache
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul

:: Remove conda environment
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% equ 0 (
    echo Removing conda environment '%ENV_NAME%'
    conda env remove -n "%ENV_NAME%" -y
)

echo SUCCESS: Cleanup completed