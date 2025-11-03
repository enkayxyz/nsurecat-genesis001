@echo off
:: Environment setup utility for Windows
:: Creates conda environment for NsureCat

set ENV_NAME=nsurecat-env

echo Setting up NsureCat environment...

:: Check if conda is available
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Conda is not installed or not in PATH
    exit /b 1
)

:: Remove existing environment if it exists
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% equ 0 (
    echo Removing existing environment '%ENV_NAME%'...
    conda env remove -n "%ENV_NAME%" -y
)

echo Creating conda environment: %ENV_NAME%
conda create -n "%ENV_NAME%" python=3.10 -y

echo SUCCESS: Environment setup complete