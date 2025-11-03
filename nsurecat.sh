#!/bin/bash

# NsureCat MVP Control Script
# Simple command dispatcher that calls utility scripts

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Main script logic
case "${1:-help}" in
    setup)
        "$SCRIPT_DIR/utils/setup/setup_env.sh" && "$SCRIPT_DIR/utils/setup/setup_deps.sh"
        ;;
    start)
        "$SCRIPT_DIR/utils/scripts/start_servers.sh"
        ;;
    stop)
        "$SCRIPT_DIR/utils/scripts/stop_servers.sh"
        ;;
    test|run_tests)
        "$SCRIPT_DIR/utils/scripts/run_tests.sh"
        ;;
    check)
        "$SCRIPT_DIR/utils/config/check_connectivity.sh"
        ;;
    status)
        "$SCRIPT_DIR/utils/config/show_status.sh"
        ;;
    clean)
        "$SCRIPT_DIR/utils/scripts/cleanup.sh"
        ;;
    help|--help|-h)
        cat << EOF
NsureCat MVP Control Script

USAGE:
    ./nsurecat.sh [COMMAND]

COMMANDS:
    setup     Create conda environment and install dependencies
    start     Start both backend and frontend servers
    stop      Stop all running servers
    test      Run pytest test suite
    run_tests Run pytest test suite (alias for test)
    check     Check connectivity to services and dependencies
    status    Show current status of all components
    clean     Clean up environment, caches, and stop services
    help      Show this help message

EXAMPLES:
    ./nsurecat.sh setup    # Set up the environment
    ./nsurecat.sh start    # Start the application
    ./nsurecat.sh status   # Check what's running
    ./nsurecat.sh test     # Run tests
    ./nsurecat.sh run_tests # Run tests (alternative)
    ./nsurecat.sh stop     # Stop everything
    ./nsurecat.sh clean    # Clean up everything

SERVICES:
    Backend:  FastAPI server on port 8000
    Frontend: Static file server on port 8001

EOF
        ;;
    *)
        echo "ERROR: Unknown command: $1"
        echo ""
        "$SCRIPT_DIR/nsurecat.sh" help
        exit 1
        ;;
esac