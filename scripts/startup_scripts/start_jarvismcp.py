"""
JarvisMCP Background Server Startup

Starts the JarvisMCP HTTP server on localhost:8765 as a background process.
Configuration: Modules/AI/agents/MCP/JarvisMCP/.env

Usage:
    python start_jarvismcp.py              # Start server in background
    python start_jarvismcp.py --dry-run    # Show what would run
    python start_jarvismcp.py --foreground # Run in foreground (blocking)
"""

from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = WORKSPACE_ROOT / "Modules" / "AI" / "agents" / "MCP" / "JarvisMCP"
CONFIG_FILE = SCRIPT_DIR / ".env"
SERVER_SCRIPT = SCRIPT_DIR / "server.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start JarvisMCP HTTP server")
    parser.add_argument("--dry-run", action="store_true", help="Show command without running")
    parser.add_argument("--foreground", action="store_true", help="Run in foreground (blocking)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Verify server script exists
    if not SERVER_SCRIPT.exists():
        print(f"ERROR: Server script not found: {SERVER_SCRIPT}")
        return 1

    python_exe = sys.executable
    cmd = [str(python_exe), str(SERVER_SCRIPT)]

    if args.dry_run:
        print(f"[DRY RUN] Would execute:")
        print(f"  cwd: {SCRIPT_DIR}")
        print(f"  cmd: {' '.join(cmd)}")
        print(f"  mode: {'foreground' if args.foreground else 'background'}")
        print(f"\nJarvisMCP Configuration: {CONFIG_FILE}")
        if CONFIG_FILE.exists():
            print(CONFIG_FILE.read_text())
        return 0

    print(f"Starting JarvisMCP Server...")
    print(f"  Working directory: {SCRIPT_DIR}")
    print(f"  Configuration: {CONFIG_FILE}")
    print(f"  Server URL: http://127.0.0.1:8765/mcp")

    if args.foreground:
        # Run in foreground (blocking)
        print(f"\nRunning in FOREGROUND mode:\n")
        result = subprocess.run(cmd, cwd=str(SCRIPT_DIR))
        return result.returncode
    else:
        # Run in background (non-blocking)
        print(f"\nRunning in BACKGROUND mode...")
        process = subprocess.Popen(
            cmd,
            cwd=str(SCRIPT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"  PID: {process.pid}")
        
        # Give the server time to start and bind to port
        print(f"  Waiting for server to become ready...")
        
        # Try to connect to port - this is more reliable than checking process.poll()
        # because FastMCP may spawn daemonized child processes
        max_attempts = 5
        for attempt in range(max_attempts):
            time.sleep(2)  # 2 second wait between attempts
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', 8765))
                sock.close()
                
                if result == 0:
                    print(f"  [OK] JarvisMCP started successfully (running in background)")
                    print(f"  To connect: http://127.0.0.1:8765/mcp")
                    return 0
            except Exception:
                pass
        
        # If we got here, port isn't responding
        # Check if process is still running at least
        if process.poll() is None:
            # Process still running, port might come up later
            print(f"  [WARNING] Port 8765 not responding yet after {max_attempts * 2} seconds")
            print(f"  [OK] Process running - may need more time to fully initialize")
            return 0
        else:
            # Process exited completely
            stdout, stderr = process.communicate()
            print(f"\n[FAILED] JarvisMCP process exited!")
            if stderr:
                print(f"STDERR:\n{stderr.decode()[:500]}")
            if stdout:
                print(f"STDOUT:\n{stdout.decode()[:500]}")
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
