"""
JarvisMCP Server Startup Script

Starts the JarvisMCP HTTP server on localhost:8765
Configuration: Modules/AI/agents/MCP/JarvisMCP/.env

Usage:
    python startup.py              # Start server
    python startup.py --dry-run    # Show what would run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / ".env"
SERVER_SCRIPT = SCRIPT_DIR / "server.py"
VENV_PYTHON = SCRIPT_DIR.parent.parent.parent.parent / ".venv" / "Scripts" / "python.exe"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start JarvisMCP HTTP server")
    parser.add_argument("--dry-run", action="store_true", help="Show command without running")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    
    # Verify server script exists
    if not SERVER_SCRIPT.exists():
        print(f"ERROR: Server script not found: {SERVER_SCRIPT}")
        return 1
    
    # Use workspace venv if available, otherwise use system python
    python_exe = VENV_PYTHON if VENV_PYTHON.exists() else sys.executable
    
    cmd = [str(python_exe), str(SERVER_SCRIPT)]
    
    if args.dry_run:
        print(f"[DRY RUN] Would execute:")
        print(f"  cwd: {SCRIPT_DIR}")
        print(f"  cmd: {' '.join(cmd)}")
        print(f"\nJarvisMCP Configuration: {CONFIG_FILE}")
        if CONFIG_FILE.exists():
            print(CONFIG_FILE.read_text())
        return 0
    
    print(f"Starting JarvisMCP Server...")
    print(f"  Working directory: {SCRIPT_DIR}")
    print(f"  Configuration: {CONFIG_FILE}")
    print(f"  Server URL: http://127.0.0.1:8765/mcp")
    print(f"\nRunning: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=str(SCRIPT_DIR))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
