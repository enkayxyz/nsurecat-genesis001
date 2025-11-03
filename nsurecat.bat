@echo off
:: NsureCat MVP Control Script for Windows
:: Simple command dispatcher that calls utility scripts

set SCRIPT_DIR=%~dp0

if "%1"=="" goto help
if "%1"=="setup" goto setup
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="test" goto test
if "%1"=="run_tests" goto test
if "%1"=="check" goto check
if "%1"=="status" goto status
if "%1"=="clean" goto clean
if "%1"=="help" goto help
if "%1"=="--help" goto help
if "%1"=="-h" goto help

echo ERROR: Unknown command: %1
echo.
goto help

:setup
call "%SCRIPT_DIR%utils\setup\setup_env.bat"
if %errorlevel% equ 0 call "%SCRIPT_DIR%utils\setup\setup_deps.bat"
goto :eof

:start
call "%SCRIPT_DIR%utils\scripts\start_servers.bat"
goto :eof

:stop
call "%SCRIPT_DIR%utils\scripts\stop_servers.bat"
goto :eof

:test
call "%SCRIPT_DIR%utils\scripts\run_tests.bat"
goto :eof

:check
call "%SCRIPT_DIR%utils\config\check_connectivity.bat"
goto :eof

:status
call "%SCRIPT_DIR%utils\config\show_status.bat"
goto :eof

:clean
call "%SCRIPT_DIR%utils\scripts\cleanup.bat"
goto :eof

:help
echo NsureCat MVP Control Script for Windows
echo.
echo USAGE:
echo     nsurecat.bat [COMMAND]
echo.
echo COMMANDS:
echo     setup     Create conda environment and install dependencies
echo     start     Start both backend and frontend servers
echo     stop      Stop all running servers
echo     test      Run pytest test suite
echo     run_tests Run pytest test suite (alias for test)
echo     check     Check connectivity to services and dependencies
echo     status    Show current status of all components
echo     clean     Clean up environment, caches, and stop services
echo     help      Show this help message
echo.
echo EXAMPLES:
echo     nsurecat.bat setup    ^& Set up the environment
echo     nsurecat.bat start    ^& Start the application
echo     nsurecat.bat status   ^& Check what's running
echo     nsurecat.bat test     ^& Run tests
echo     nsurecat.bat run_tests ^& Run tests (alternative)
echo     nsurecat.bat stop     ^& Stop everything
echo     nsurecat.bat clean    ^& Clean up everything
echo.
echo SERVICES:
echo     Backend:  FastAPI server on port 8000
echo     Frontend: Static file server on port 8001
echo.
goto :eof