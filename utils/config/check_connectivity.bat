@echo off
:: Connectivity check utility for Windows
:: Checks connectivity to services and dependencies

set ENV_NAME=nsurecat-env
set BACKEND_PORT=8000
set FRONTEND_PORT=8001

echo Checking connectivity...

:: Check backend
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:%BACKEND_PORT%/' -TimeoutSec 5 | Out-Null; Write-Host 'SUCCESS: Backend server is accessible on port %BACKEND_PORT%' } catch { Write-Host 'ERROR: Backend server is not accessible on port %BACKEND_PORT%' }" 2>nul

:: Check frontend
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:%FRONTEND_PORT%/' -TimeoutSec 5 | Out-Null; Write-Host 'SUCCESS: Frontend server is accessible on port %FRONTEND_PORT%' } catch { Write-Host 'ERROR: Frontend server is not accessible on port %FRONTEND_PORT%' }" 2>nul

:: Check Arc Testnet
powershell -Command "try { Invoke-WebRequest -Uri 'https://rpc-testnet.arbitrum.io' -TimeoutSec 10 | Out-Null; Write-Host 'SUCCESS: Arc Testnet RPC is accessible' } catch { Write-Host 'WARNING: Arc Testnet RPC is not accessible (may be temporary)' }" 2>nul

:: Check if environment is set up
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: Conda environment '%ENV_NAME%' exists
) else (
    echo ERROR: Conda environment '%ENV_NAME%' does not exist
)

:: Check Python dependencies
conda env list | findstr /C:"%ENV_NAME%" >nul 2>nul
if %errorlevel% equ 0 (
    conda run -n "%ENV_NAME%" python -c "import fastapi, uvicorn, pydantic" >nul 2>nul
    if !errorlevel! equ 0 (
        echo SUCCESS: Python dependencies are installed
    ) else (
        echo ERROR: Python dependencies are not properly installed
    )
)

echo Connectivity check completed