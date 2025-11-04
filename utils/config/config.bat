@echo off
REM NsureCat Configuration for Windows
REM This file defines all environment variables and configuration used across the project

REM Environment
set NSURECAT_ENV_NAME=nsurecat
set PYTHON_VERSION=3.10

REM Ports
set BACKEND_PORT=8000
set FRONTEND_PORT=8001

REM URLs (derived from ports)
set BACKEND_URL=http://localhost:%BACKEND_PORT%
set FRONTEND_URL=http://localhost:%FRONTEND_PORT%

REM API Configuration
set API_BASE_URL=%BACKEND_URL%

REM Directories
set PROJECT_ROOT=%~dp0
set BACKEND_DIR=%PROJECT_ROOT%src\backend
set FRONTEND_DIR=%PROJECT_ROOT%src\frontend
set TESTS_DIR=%PROJECT_ROOT%tests

REM Testing
set TEST_TIMEOUT=30000
set PYTEST_ARGS=-v --tb=short

REM Development
set UVICORN_RELOAD=--reload
set LOG_LEVEL=info

REM Export marker to detect if config is loaded
set NSURECAT_CONFIG_LOADED=1

if "%1"=="show" (
    echo === NsureCat Configuration ===
    echo Environment: %NSURECAT_ENV_NAME%
    echo Python: %PYTHON_VERSION%
    echo Backend: %BACKEND_URL%
    echo Frontend: %FRONTEND_URL%
    echo Project Root: %PROJECT_ROOT%
    echo =============================
)
