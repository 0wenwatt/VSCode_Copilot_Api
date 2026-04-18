# Workspace Startup Fix

## Issue
The workspace was configured to automatically run a startup task (`startup.py`) every time the folder was opened in VS Code. This task:
- Launches Docker Desktop
- Starts Docker containers for ArangoDB
- Waits up to 80 seconds for ArangoDB to become healthy
- **Caused VS Code to hang and the system to crash** due to resource constraints and blocking I/O

## Solution
Removed the `"runOn": "folderOpen"` configuration from `.vscode/tasks.json` for the "Workspace Startup" task.

**File modified:** `.vscode/tasks.json`
**Line removed:** `"runOptions": { "runOn": "folderOpen" }`

## How to Use the Startup Script Now

### Manual Trigger (Recommended)
1. Open the workspace normally
2. Go to **Terminal** → **Run Task**
3. Select one of:
   - **"Workspace Startup"** - Normal startup with ArangoDB
   - **"Workspace Startup (dry-run)"** - See what would execute without running it
   - **"Workspace Startup (with MCP)"** - Startup + MCP Arangodb profile

### Command Line (Alternative)
```powershell
python ./startup.py                    # Normal startup
python ./startup.py --dry-run          # Preview mode
python ./startup.py --with-mcp         # With MCP profile
```

## Prerequisites
- **Docker Desktop** must be installed: https://www.docker.com/products/docker-desktop/
- Ensure the Docker daemon can start without issues

## Troubleshooting
If the startup task still hangs:
1. Check if Docker Desktop is running: `docker info`
2. Start the task in dry-run mode first: `python ./startup.py --dry-run`
3. Check resource availability (Task Manager → Performance)

---
**Modified:** 2026-04-18 | **Status:** Auto-startup disabled to prevent crashes
