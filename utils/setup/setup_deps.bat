@echo off
:: Dependencies installation utility for Windows
:: Installs Python requirements in conda environment

set ENV_NAME=nsurecat-env
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..

echo Installing Python dependencies...

:: Check if environment exists
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Environment '%ENV_NAME%' does not exist. Run setup_env.bat first.
    exit /b 1
)

cd /d "%PROJECT_ROOT%"

echo Activating environment and installing requirements
conda run -n "%ENV_NAME%" pip install -r requirements.txt

echo SUCCESS: Dependencies installed