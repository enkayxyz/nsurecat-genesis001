---
applyTo: '**'
---
Our Architecture 
Purpose: This defines the standard, opinionated, and extensible directory structure for all new projects.
Core Technology Stack:
Environment Manager: Conda (No Docker)
Backend Language: Python 3.10+
Backend Framework: FastAPI
API Server: Uvicorn
Frontend: HTML5, CSS3, & Vanilla JavaScript (ES6+)
Frontend Server: python http.server (standard library)
Testing: Pytest
Key Constraint: This project WILL NOT use Node.js, npm, or any JS frameworks (React, Vue, etc.). 
This is a 2-layer application. The FastAPI backend serves as the API layer. The frontend is a set of static files (.html, .js, .css) served by a separate, simple python http.server.
Root Directory Structure:
/: Contains root files (.gitignore, requirements.txt, etc.)
README.md: Public-facing project summary and setup instructions.
Main Folders:
/docs/: All documentation.
/docs/product/: Product requirements, user stories, ...
/docs/pmo/: Project management, roadmaps, internal plans, ...
/docs/tech/: API specs, architecture diagrams, ...
...
/src/: All application source code.
/src/backend/: Main FastAPI application logic (e.g., main.py, core business rules).
/src/frontend/: All static HTML, CSS, and Vanilla JS files.
/src/api_routes/: API controllers/routes (FastAPI routers) that connect the backend to the frontend.
/src/agent/: Core "smart" logic (e.g., AI agent modules, data processing).
/src/services/: Python modules for all external API calls (e.g., to carriers, Arc).
...
/tests/: All Pytest unit and integration tests. This folder's structure must mirror the /src/ folder structure.
/tests/backend/
/tests/api_routes/
/tests/agent/
/tests/services/
...
/utils/: Standalone utility/helper scripts.
/utils/setup/
/utils/config/
/utils/scripts/
...
Utility Scripts (in root):
setup.sh / setup.bat: Creates conda env, installs requirements.txt.
start.sh / start.bat: Activates conda env, starts the uvicorn API server and the python http.server for the frontend.
test.sh / test.bat: Activates conda env, runs pytest.
...



