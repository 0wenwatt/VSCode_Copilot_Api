#!/usr/bin/env python3
"""
Unified MCP Startup Script

Starts all MCPs in proper order with monitoring and health checks:
1. ArangoDB Docker (prerequisite)
2. JarvisMCP (HTTP gateway with mounted ArangoDB MCP)
3. Time MCP (optional)
4. Git MCP (optional)
5. Fetch MCP (optional)
6. Everything MCP (optional)

Usage:
    python startup_all_mcps.py                    # Start all MCPs
    python startup_all_mcps.py --only jarvis      # Start only JarvisMCP
    python startup_all_mcps.py --skip time,git    # Skip specific MCPs
    python startup_all_mcps.py --dry-run          # Show commands without running
    python startup_all_mcps.py --no-arangodb      # Skip ArangoDB Docker
    python startup_all_mcps.py --monitor          # Show live status
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class MCPType(Enum):
    """MCP Server Types"""
    PYTHON_STDIO = "python_stdio"
    NODEJS_STDIO = "nodejs_stdio"
    HTTP_GATEWAY = "http_gateway"
    DOCKER = "docker"


@dataclass
class MCP:
    """MCP Server Configuration"""
    name: str
    path: Path
    start_command: list[str]
    port: Optional[int] = None
    mcp_type: MCPType = MCPType.PYTHON_STDIO
    env: Optional[dict[str, str]] = None
    check_port: bool = False
    wait_time: int = 2
    required: bool = False

    def __post_init__(self):
        if self.env is None:
            self.env = {}


WORKSPACE_ROOT = Path(__file__).resolve().parent
DOCKER_COMPOSE_DIR = WORKSPACE_ROOT / "Modules" / "docker"

MCPs = {
    "arangodb": MCP(
        name="ArangoDB Docker",
        path=DOCKER_COMPOSE_DIR,
        start_command=[
            "docker", "compose",
            "-f", "docker-compose.arango.yml",
            "up", "-d"
        ],
        mcp_type=MCPType.DOCKER,
        port=8893,
        check_port=True,
        wait_time=3,
        required=True,
    ),
    "jarvis": MCP(
        name="JarvisMCP (HTTP Gateway)",
        path=WORKSPACE_ROOT / "Modules" / "AI" / "agents" / "MCP" / "JarvisMCP",
        start_command=[sys.executable, "server.py"],
        mcp_type=MCPType.HTTP_GATEWAY,
        port=8765,
        check_port=True,
        wait_time=2,
        required=True,
    ),
    "time": MCP(
        name="Time MCP",
        path=WORKSPACE_ROOT / "Modules" / "AI" / "agents" / "MCP" / "github" / "servers" / "src" / "time",
        start_command=[sys.executable, "-m", "mcp_server_time"],
        mcp_type=MCPType.PYTHON_STDIO,
        wait_time=2,
    ),
    "git": MCP(
        name="Git MCP",
        path=WORKSPACE_ROOT / "Modules" / "AI" / "agents" / "MCP" / "github" / "servers" / "src" / "git",
        start_command=[sys.executable, "-m", "mcp_server_git", "."],
        mcp_type=MCPType.PYTHON_STDIO,
        wait_time=2,
    ),
    "fetch": MCP(
        name="Fetch MCP",
        path=WORKSPACE_ROOT / "Modules" / "AI" / "agents" / "MCP" / "github" / "servers" / "src" / "fetch",
        start_command=[sys.executable, "-m", "mcp_server_fetch"],
        mcp_type=MCPType.PYTHON_STDIO,
        wait_time=2,
    ),
    "everything": MCP(
        name="Everything MCP",
        path=WORKSPACE_ROOT / "Modules" / "AI" / "agents" / "MCP" / "github" / "servers" / "src" / "everything",
        start_command=["npm", "start"],
        mcp_type=MCPType.NODEJS_STDIO,
        port=3001,
        check_port=True,
        wait_time=3,
    ),
}


class Colors:
    """ANSI Color codes"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def colored(text: str, color: str, bold: bool = False) -> str:
    """Apply color to text"""
    return f"{color}{Colors.BOLD if bold else ''}{text}{Colors.RESET}"


def check_port_open(port: int, timeout: float = 1.0) -> bool:
    """Check if a port is open"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex(("127.0.0.1", port))
        return result == 0
    finally:
        sock.close()


def print_banner():
    """Print startup banner"""
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print(colored("🚀 MCP Unified Startup System", Colors.CYAN, bold=True))
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print()


def print_mcp_list(to_start: list[str]):
    """Print list of MCPs to start"""
    print(colored("📋 MCPs to Start:", Colors.BLUE, bold=True))
    for name in to_start:
        mcp = MCPs[name]
        req = " [REQUIRED]" if mcp.required else ""
        print(f"  • {colored(mcp.name, Colors.YELLOW)}{req}")
    print()


def print_startup_info(mcp: MCP):
    """Print MCP startup information"""
    print()
    print(colored(f"▶ Starting {mcp.name}...", Colors.BLUE, bold=True))
    print(f"  Path: {mcp.path}")
    print(f"  Command: {' '.join(mcp.start_command)}")
    if mcp.port:
        print(f"  Port: {mcp.port}")


async def start_mcp(
    name: str,
    mcp: MCP,
    dry_run: bool = False,
    monitor: bool = False,
) -> bool:
    """Start a single MCP server"""
    
    print_startup_info(mcp)
    
    if not mcp.path.exists():
        print(colored(f"  ✗ Path not found: {mcp.path}", Colors.RED))
        return False
    
    if dry_run:
        print(colored("  [DRY RUN - Not actually started]", Colors.YELLOW))
        return True
    
    try:
        # Start the process
        print(f"  {colored('⏳ Starting...', Colors.YELLOW)}")
        
        process = subprocess.Popen(
            mcp.start_command,
            cwd=str(mcp.path),
            stdout=subprocess.PIPE if not monitor else None,
            stderr=subprocess.PIPE if not monitor else None,
            env={**os.environ, **(mcp.env or {})},
        )
        
        # Wait for startup
        await asyncio.sleep(mcp.wait_time)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            error_msg = stderr.decode("utf-8", errors="replace") if stderr else stdout.decode("utf-8", errors="replace")
            print(colored(f"  ✗ Process exited immediately: {error_msg[:200]}", Colors.RED))
            return False
        
        # Check port if applicable
        if mcp.check_port and mcp.port:
            port_open = check_port_open(mcp.port)
            if port_open:
                print(colored(f"  ✓ Started successfully (PID: {process.pid}, Port: {mcp.port} open)", Colors.GREEN))
            else:
                print(colored(f"  ⚠ Started but port {mcp.port} not yet responding", Colors.YELLOW))
        else:
            print(colored(f"  ✓ Started successfully (PID: {process.pid})", Colors.GREEN))
        
        return True
        
    except Exception as e:
        print(colored(f"  ✗ Error starting: {e}", Colors.RED))
        return False


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Start all MCP servers in proper order",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--only",
        help="Start only specified MCP (comma-separated: jarvis,time,git,fetch,everything)",
        type=str,
    )
    
    parser.add_argument(
        "--skip",
        help="Skip specified MCPs (comma-separated)",
        type=str,
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show commands without running",
    )
    
    parser.add_argument(
        "--no-arangodb",
        action="store_true",
        help="Skip ArangoDB Docker startup",
    )
    
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Show live status monitoring",
    )
    
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check status of running MCPs",
    )
    
    return parser.parse_args()


async def check_running_mcps():
    """Check which MCPs are currently running"""
    print()
    print(colored("🔍 Checking Running MCPs:", Colors.BLUE, bold=True))
    
    running = []
    for name, mcp in MCPs.items():
        if mcp.port and mcp.check_port:
            is_running = check_port_open(mcp.port, timeout=0.5)
            status = colored("✓ RUNNING", Colors.GREEN) if is_running else colored("✗ STOPPED", Colors.RED)
            print(f"  {mcp.name:30} {status} (port {mcp.port})")
            if is_running:
                running.append(name)
    
    print()
    return running


async def main():
    """Main startup sequence"""
    args = parse_args()
    
    print_banner()
    
    # Check only mode
    if args.check_only:
        await check_running_mcps()
        return 0
    
    # Determine which MCPs to start
    all_names = list(MCPs.keys())
    
    if args.only:
        to_start = args.only.split(",")
    else:
        to_start = all_names
    
    if args.skip:
        skip = args.skip.split(",")
        to_start = [m for m in to_start if m not in skip]
    
    if args.no_arangodb:
        to_start = [m for m in to_start if m != "arangodb"]
    
    print_mcp_list(to_start)
    
    # Build prerequisite info
    prerequisites_met = True
    if "arangodb" not in to_start and "jarvis" in to_start:
        print(colored("⚠ Warning: ArangoDB Docker not starting but JarvisMCP requires it", Colors.YELLOW))
        print("   Use --no-arangodb only if ArangoDB is already running")
        print()
    
    # Dry run info
    if args.dry_run:
        print(colored("📋 DRY RUN MODE - Commands will not be executed:", Colors.YELLOW))
        print()
    
    # Start MCPs
    results = {}
    for name in to_start:
        mcp = MCPs[name]
        success = await start_mcp(name, mcp, dry_run=args.dry_run, monitor=args.monitor)
        results[name] = success
        
        if not success and mcp.required:
            print(colored(f"✗ Failed to start required MCP: {name}", Colors.RED))
            prerequisites_met = False
            if not args.dry_run:
                return 1
    
    # Summary
    print()
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print(colored("📊 Startup Summary", Colors.CYAN, bold=True))
    print(colored("=" * 70, Colors.CYAN, bold=True))
    
    successful = [k for k, v in results.items() if v]
    failed = [k for k, v in results.items() if not v]
    
    print(f"  {colored('✓ Successful:', Colors.GREEN)} {len(successful)}/{len(results)}")
    for name in successful:
        print(f"    • {MCPs[name].name}")
    
    if failed:
        print(f"  {colored('✗ Failed:', Colors.RED)} {len(failed)}/{len(results)}")
        for name in failed:
            print(f"    • {MCPs[name].name}")
    
    print()
    
    # Show connection info
    if "jarvis" in successful:
        print(colored("🔗 Connection Information:", Colors.BLUE, bold=True))
        print(f"  JarvisMCP URL: {colored('http://127.0.0.1:8765/mcp', Colors.YELLOW)}")
        print()
        print(colored("📋 Add to mcp.json:", Colors.BLUE, bold=True))
        print("""  {
    "JarvisMCP": {
      "url": "127.0.0.1:8765",
      "type": "http"
    }
  }""")
    
    print()
    
    if not args.dry_run:
        print(colored("✅ Startup complete! MCPs are ready for use.", Colors.GREEN, bold=True))
        print(colored("Press Ctrl+C in individual terminals to stop each MCP", Colors.YELLOW))
        if not prerequisites_met and "jarvis" in to_start:
            return 1
    else:
        print(colored("✅ Dry run complete! No servers were actually started.", Colors.GREEN, bold=True))
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
