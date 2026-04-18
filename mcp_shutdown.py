#!/usr/bin/env python3
"""
MCP Shutdown & Cleanup Script

Gracefully shuts down all running MCP servers and Docker containers:
- Stops individual MCP processes
- Stops ArangoDB Docker
- Performs cleanup
- Verifies shutdown

Usage:
    python mcp_shutdown.py              # Graceful shutdown
    python mcp_shutdown.py --force      # Force termination
    python mcp_shutdown.py --purge      # Cleanup all data (Docker volumes)
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


class Colors:
    """ANSI color codes"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


def colored(text: str, color: str, bold: bool = False) -> str:
    """Apply color to text"""
    return f"{color}{Colors.BOLD if bold else ''}{text}{Colors.RESET}"


def print_banner():
    """Print banner"""
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print(colored("🛑 MCP Shutdown & Cleanup System", Colors.CYAN, bold=True))
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print()


async def stop_docker(force: bool = False, purge: bool = False):
    """Stop ArangoDB Docker container"""
    print(colored("🐳 Stopping ArangoDB Docker...", Colors.BLUE, bold=True))
    
    workspace_root = Path(__file__).resolve().parent
    docker_dir = workspace_root / "Modules" / "docker"
    
    if not docker_dir.exists():
        print(colored("  ⚠ Docker directory not found", Colors.YELLOW))
        return False
    
    try:
        # Stop containers
        cmd = ["docker", "compose", "-f", "docker-compose.arango.yml", "down"]
        if purge:
            cmd.append("-v")  # Remove volumes
            print(colored("  ⚠ Removing volumes (--purge)", Colors.YELLOW))
        
        result = subprocess.run(
            cmd,
            cwd=str(docker_dir),
            capture_output=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            print(colored("  ✓ ArangoDB Docker stopped", Colors.GREEN))
            return True
        else:
            error = result.stderr.decode("utf-8", errors="replace")
            print(colored(f"  ✗ Error stopping Docker: {error[:100]}", Colors.RED))
            return False
    except subprocess.TimeoutExpired:
        print(colored("  ✗ Docker stop timed out", Colors.RED))
        return False
    except Exception as e:
        print(colored(f"  ✗ Error: {e}", Colors.RED))
        return False


def find_mcp_processes() -> dict[str, int]:
    """Find running MCP processes"""
    processes = {}
    
    # Look for Python MCPs
    try:
        result = subprocess.run(
            ["tasklist", "/v", "/fo", "csv"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        for line in result.stdout.split("\n"):
            if "python" in line.lower() and ("mcp" in line.lower() or "jarvis" in line.lower()):
                # Very basic parsing - extract PID
                parts = line.split(",")
                if len(parts) > 1:
                    try:
                        pid = int(parts[1].strip('"'))
                        processes[f"Python MCP (PID {pid})"] = pid
                    except ValueError:
                        pass
    except Exception:
        pass
    
    # Look for Node.js MCPs
    try:
        result = subprocess.run(
            ["tasklist", "/v", "/fo", "csv"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        for line in result.stdout.split("\n"):
            if "node" in line.lower() and "mcp" in line.lower():
                parts = line.split(",")
                if len(parts) > 1:
                    try:
                        pid = int(parts[1].strip('"'))
                        processes[f"Node.js MCP (PID {pid})"] = pid
                    except ValueError:
                        pass
    except Exception:
        pass
    
    return processes


async def stop_mcp_processes(force: bool = False):
    """Stop running MCP processes"""
    print(colored("🔌 Stopping MCP processes...", Colors.BLUE, bold=True))
    
    processes = find_mcp_processes()
    
    if not processes:
        print(colored("  ℹ No MCP processes found running", Colors.YELLOW))
        return True
    
    success = True
    for name, pid in processes.items():
        try:
            # Use taskkill on Windows
            cmd = ["taskkill", "/PID", str(pid)]
            if force:
                cmd.append("/F")
            
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            
            if result.returncode == 0:
                print(colored(f"  ✓ Stopped {name}", Colors.GREEN))
            else:
                print(colored(f"  ⚠ Could not stop {name}", Colors.YELLOW))
                success = False
        except Exception as e:
            print(colored(f"  ✗ Error stopping {name}: {e}", Colors.RED))
            success = False
    
    return success


async def cleanup():
    """Perform cleanup"""
    print(colored("🧹 Cleanup...", Colors.BLUE, bold=True))
    
    # Check for temp files
    workspace_root = Path(__file__).resolve().parent
    
    # Remove old startup logs if present
    for logfile in ["startup_output.txt", "startup_final.txt"]:
        logpath = workspace_root / logfile
        if logpath.exists():
            try:
                logpath.unlink()
                print(colored(f"  ✓ Removed {logfile}", Colors.GREEN))
            except Exception as e:
                print(colored(f"  ⚠ Could not remove {logfile}: {e}", Colors.YELLOW))
    
    print()


async def verify_shutdown() -> bool:
    """Verify all MCPs are shut down"""
    print(colored("✓ Verification", Colors.BLUE, bold=True))
    
    # Check ports
    import socket
    
    ports_to_check = [
        (8765, "JarvisMCP"),
        (8893, "ArangoDB"),
        (3001, "Everything MCP"),
    ]
    
    all_closed = True
    for port, name in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            result = sock.connect_ex(("127.0.0.1", port))
            if result == 0:
                print(colored(f"  ⚠ Port {port} ({name}) still responding", Colors.YELLOW))
                all_closed = False
            else:
                print(colored(f"  ✓ Port {port} ({name}) closed", Colors.GREEN))
        finally:
            sock.close()
    
    print()
    return all_closed


async def main():
    """Main shutdown sequence"""
    parser = argparse.ArgumentParser(description="MCP Shutdown & Cleanup")
    parser.add_argument("--force", action="store_true", help="Force termination")
    parser.add_argument("--purge", action="store_true", help="Cleanup data (Docker volumes)")
    parser.add_argument("--docker-only", action="store_true", help="Only stop Docker")
    parser.add_argument("--processes-only", action="store_true", help="Only stop processes")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.purge:
        print(colored("⚠ WARNING: --purge will remove Docker volumes (data loss!)", Colors.YELLOW, bold=True))
        response = input("Are you sure? (yes/no): ").strip().lower()
        if response != "yes":
            print("Cancelled.")
            return 0
        print()
    
    success = True
    
    # Stop processes
    if not args.docker_only:
        if await stop_mcp_processes(force=args.force):
            await asyncio.sleep(1)  # Let processes terminate
        else:
            success = False
    
    print()
    
    # Stop Docker
    if not args.processes_only:
        if not await stop_docker(force=args.force, purge=args.purge):
            success = False
    
    print()
    
    # Cleanup
    await cleanup()
    
    # Verify
    await verify_shutdown()
    
    # Summary
    print(colored("=" * 70, Colors.CYAN, bold=True))
    if success:
        print(colored("✅ Shutdown complete!", Colors.GREEN, bold=True))
    else:
        print(colored("⚠ Shutdown completed with warnings", Colors.YELLOW, bold=True))
    print(colored("=" * 70, Colors.CYAN, bold=True))
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
