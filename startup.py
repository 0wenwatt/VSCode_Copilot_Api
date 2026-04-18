"""
startup.py — Workspace startup script
Run this once when opening the workspace to bring up all services.

Orchestrates:
1. Docker daemon startup (if needed)
2. ArangoDB container startup
3. JarvisMCP gateway server startup (background)
4. MCP integration validation

Usage:
    python startup.py              # normal mode
    python startup.py --dry-run    # print commands, don't execute
    python startup.py --no-test    # skip integration tests

VS Code auto-runs this via .vscode/tasks.json on folder open.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

# ── Workspace root (this file lives at the root) ──────────────────────────────
WORKSPACE_ROOT = Path(__file__).resolve().parent
STARTUP_SCRIPTS_DIR = WORKSPACE_ROOT / "scripts" / "startup_scripts"

# ── Scripts to run in order ───────────────────────────────────────────────────
# Each entry: (script_path, extra_args, description)
STARTUP_SCRIPTS: list[tuple[Path, list[str], str]] = [
    (
        STARTUP_SCRIPTS_DIR / "setup_arangodb_docker.py",
        [],
        "ArangoDB Docker",
    ),
    (
        STARTUP_SCRIPTS_DIR / "start_jarvismcp.py",
        [],
        "JarvisMCP Gateway",
    ),
    (
        STARTUP_SCRIPTS_DIR / "test_mcp_integration.py",
        [],
        "MCP Integration Test",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Workspace startup — runs all startup scripts in order."
    )
    parser.add_argument("--dry-run", action="store_true", help="Pass --dry-run to all scripts")
    parser.add_argument("--no-test", action="store_true", help="Skip integration tests")
    parser.add_argument("--retries", type=int, default=20, help="Max startup retries")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between retries")
    return parser.parse_args()


def run_script(script: Path, extra_args: list[str], global_args: argparse.Namespace, description: str) -> int:
    """Run a single startup script via the current Python interpreter."""
    cmd = [sys.executable, str(script)]

    # Forward global flags to scripts that accept them
    if global_args.dry_run:
        cmd.append("--dry-run")

    # Skip test script if --no-test is set
    if global_args.no_test and "test_mcp" in script.name:
        print(f"\n{'='*60}")
        print(f"Skipping: {description} (--no-test)")
        print(f"{'='*60}")
        return 0

    # Forward script-specific extra args
    cmd.extend(extra_args)

    # Forward retries/delay to Docker setup script
    if "arangodb_docker" in script.name:
        cmd.extend(["--retries", str(global_args.retries)])
        cmd.extend(["--delay", str(global_args.delay)])

    print(f"\n{'='*60}")
    print(f"[{description}]")
    print(f"{'='*60}")

    result = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT))
    return result.returncode


def main() -> int:
    args = parse_args()
    print(f"\n{'='*60}")
    print(f"Workspace Startup — VSCode Copilot API")
    print(f"{'='*60}")
    print(f"Root: {WORKSPACE_ROOT}")
    print(f"Mode: {'dry-run' if args.dry_run else 'apply'}")
    print(f"Tests: {'disabled' if args.no_test else 'enabled'}")
    print(f"Startup scripts: {STARTUP_SCRIPTS_DIR}")

    failures: list[tuple[str, int]] = []

    for script, extra_args, description in STARTUP_SCRIPTS:
        if not script.exists():
            print(f"\nWARNING: script not found, skipping: {script}")
            continue

        rc = run_script(script, extra_args, args, description)
        if rc != 0:
            failures.append((description, rc))
            print(f"\n[FAILED] {description} failed (exit {rc})")
            # Don't stop on first failure; continue to see all issues
            if "test" in description.lower():
                # But test failures are informational, continue
                pass
            elif rc != 0:
                # Docker/JarvisMCP failures should stop execution
                print(f"Stopping due to critical failure: {description}")
                break

    print(f"\n{'='*60}")
    if failures:
        failed_critical = [f for f in failures if "test" not in f[0].lower()]
        if failed_critical:
            print(f"[FAILED] Startup FAILED: {len(failed_critical)} critical failure(s)")
            for desc, code in failed_critical:
                print(f"   - {desc} (exit {code})")
            return 1
        else:
            print(f"[WARNING] Startup PARTIAL: {len(failures)} test(s) failed")
            for desc, code in failures:
                print(f"   - {desc} (exit {code})")
            print(f"\nServices may still be operational despite test failures.")
            return 1

    print(f"[SUCCESS] Startup complete - all services ready")
    print(f"\nServices running:")
    print(f"  • ArangoDB:     http://127.0.0.1:8529")
    print(f"  • JarvisMCP:    http://127.0.0.1:8765/mcp")
    print(f"{'='*60}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
