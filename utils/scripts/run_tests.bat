@echo off
:: Test runner utility for Windows
:: Runs pytest test suite

set ENV_NAME=nsurecat-env
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..

echo Running tests...

:: Check if environment exists
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Environment '%ENV_NAME%' does not exist. Run setup first.
    exit /b 1
)

cd /d "%PROJECT_ROOT%"

echo Installing Playwright browsers...
conda run -n "%ENV_NAME%" python -m playwright install chromium

echo Activating environment and running pytest
conda run -n "%ENV_NAME%" pytest tests/ -v --browser chromium

echo SUCCESS: Tests completed