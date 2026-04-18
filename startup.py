"""
startup.py — Workspace startup script
Run this once when opening the workspace to bring up all services.

Usage:
    python startup.py              # normal mode
    python startup.py --dry-run    # print commands, don't execute
    python startup.py --with-mcp   # also start the ArangoDB MCP sidecar

VS Code auto-runs this via .vscode/tasks.json on folder open.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# ── Workspace root (this file lives at the root) ──────────────────────────────
WORKSPACE_ROOT = Path(__file__).resolve().parent
STARTUP_SCRIPTS_DIR = WORKSPACE_ROOT / "scripts" / "startup_scripts"

# ── Scripts to run in order ───────────────────────────────────────────────────
# Each entry: (script_path, extra_args)
# extra_args is a list of CLI flags forwarded from this script where relevant.
STARTUP_SCRIPTS: list[tuple[Path, list[str]]] = [
    (STARTUP_SCRIPTS_DIR / "setup_arangodb_docker.py", []),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Workspace startup — runs all startup scripts in order."
    )
    parser.add_argument("--dry-run", action="store_true", help="Pass --dry-run to all scripts")
    parser.add_argument("--with-mcp", action="store_true", help="Pass --with-mcp to arangodb script")
    return parser.parse_args()


def run_script(script: Path, extra_args: list[str], global_args: argparse.Namespace) -> int:
    """Run a single startup script via the current Python interpreter."""
    cmd = [sys.executable, str(script)]

    # Forward global flags to scripts that accept them
    if global_args.dry_run:
        cmd.append("--dry-run")

    # Forward script-specific extra args
    cmd.extend(extra_args)

    # --with-mcp is forwarded to the arangodb script specifically
    if global_args.with_mcp and "arangodb" in script.stem:
        cmd.append("--with-mcp")

    print(f"\n{'='*60}")
    print(f"Running: {script.name}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT))
    return result.returncode


def main() -> int:
    args = parse_args()
    print(f"Workspace startup — {WORKSPACE_ROOT}")
    print(f"Scripts directory: {STARTUP_SCRIPTS_DIR}")
    print(f"Mode: {'dry-run' if args.dry_run else 'apply'}")

    failures: list[str] = []

    for script, extra_args in STARTUP_SCRIPTS:
        if not script.exists():
            print(f"WARNING: script not found, skipping: {script}")
            continue

        rc = run_script(script, extra_args, args)
        if rc != 0:
            failures.append(script.name)
            print(f"FAILED: {script.name} (exit {rc})")

    print(f"\n{'='*60}")
    if failures:
        print(f"Startup completed with {len(failures)} failure(s): {', '.join(failures)}")
        return 1

    print("Startup complete — all services ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
