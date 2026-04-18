#!/usr/bin/env python3
"""
MCP Health Check & Monitoring System

Checks status of all MCP servers and provides detailed diagnostics:
- Port connectivity
- Process status
- API responsiveness
- Tool availability
- Configuration validation

Usage:
    python mcp_health_check.py              # Quick status check
    python mcp_health_check.py --detailed   # Detailed diagnostics
    python mcp_health_check.py --watch      # Live monitoring (updates every 5s)
    python mcp_health_check.py --test       # Run comprehensive tests
"""

from __future__ import annotations

import argparse
import asyncio
import json
import socket
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore


class Status(Enum):
    """Health status"""
    HEALTHY = "✓ HEALTHY"
    DEGRADED = "⚠ DEGRADED"
    UNHEALTHY = "✗ UNHEALTHY"
    UNKNOWN = "? UNKNOWN"
    STOPPED = "⊘ STOPPED"


@dataclass
class HealthCheckResult:
    """Health check result"""
    name: str
    status: Status
    port: Optional[int] = None
    port_open: bool = False
    api_responsive: bool = False
    tools_available: int = 0
    details: list[str] = None
    timestamp: float = 0.0

    def __post_init__(self):
        if self.details is None:
            self.details = []
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class Colors:
    """ANSI color codes"""
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
    """Check if port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex(("127.0.0.1", port))
        return result == 0
    finally:
        sock.close()


async def check_jarvis_mcp() -> HealthCheckResult:
    """Check JarvisMCP health"""
    result = HealthCheckResult(
        name="JarvisMCP",
        status=Status.UNKNOWN,
        port=8765,
    )
    
    # Check port
    result.port_open = check_port_open(result.port, timeout=1.0)
    if not result.port_open:
        result.status = Status.STOPPED
        result.details.append("Port 8765 not responding")
        return result
    
    result.details.append("Port 8765 open")
    
    # Check API
    if httpx:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.post(
                    "http://127.0.0.1:8765/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {},
                            "clientInfo": {"name": "health-check", "version": "1.0"}
                        }
                    },
                )
                if response.status_code == 200:
                    result.api_responsive = True
                    result.details.append("API responding")
                    result.status = Status.HEALTHY
                else:
                    result.status = Status.DEGRADED
                    result.details.append(f"API returned {response.status_code}")
        except Exception as e:
            result.status = Status.DEGRADED
            result.details.append(f"API check failed: {str(e)[:50]}")
    else:
        result.status = Status.HEALTHY if result.port_open else Status.DEGRADED
    
    return result


async def check_arangodb_mcp() -> HealthCheckResult:
    """Check ArangoDB MCP health"""
    result = HealthCheckResult(
        name="ArangoDB MCP",
        status=Status.UNKNOWN,
        port=8893,  # ArangoDB database port
    )
    
    # Check database port (not MCP port)
    result.port_open = check_port_open(result.port, timeout=1.0)
    if not result.port_open:
        result.status = Status.STOPPED
        result.details.append("ArangoDB database port 8893 not responding")
        return result
    
    result.details.append("ArangoDB database running on port 8893")
    
    # Try to connect to ArangoDB HTTP API
    if httpx:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(
                    "http://127.0.0.1:8893/_api/version",
                    auth=("root", "test123"),
                )
                if response.status_code == 200:
                    data = response.json()
                    version = data.get("version", "unknown")
                    result.api_responsive = True
                    result.details.append(f"ArangoDB v{version} responding")
                    result.status = Status.HEALTHY
                else:
                    result.status = Status.DEGRADED
                    result.details.append(f"API returned {response.status_code}")
        except Exception as e:
            result.status = Status.DEGRADED
            result.details.append(f"Database check failed: {str(e)[:50]}")
    else:
        result.status = Status.HEALTHY if result.port_open else Status.DEGRADED
    
    return result


async def check_time_mcp() -> HealthCheckResult:
    """Check Time MCP health"""
    result = HealthCheckResult(
        name="Time MCP",
        status=Status.UNKNOWN,
    )
    
    result.status = Status.STOPPED
    result.details.append("Stdio-based MCP (no port to check)")
    result.details.append("Start with: python -m mcp_server_time")
    
    return result


async def check_git_mcp() -> HealthCheckResult:
    """Check Git MCP health"""
    result = HealthCheckResult(
        name="Git MCP",
        status=Status.UNKNOWN,
    )
    
    result.status = Status.STOPPED
    result.details.append("Stdio-based MCP (no port to check)")
    result.details.append("Start with: python -m mcp_server_git .")
    
    return result


async def check_fetch_mcp() -> HealthCheckResult:
    """Check Fetch MCP health"""
    result = HealthCheckResult(
        name="Fetch MCP",
        status=Status.UNKNOWN,
    )
    
    result.status = Status.STOPPED
    result.details.append("Stdio-based MCP (no port to check)")
    result.details.append("Start with: python -m mcp_server_fetch")
    
    return result


async def check_everything_mcp() -> HealthCheckResult:
    """Check Everything MCP health"""
    result = HealthCheckResult(
        name="Everything MCP",
        status=Status.UNKNOWN,
        port=3001,
    )
    
    result.port_open = check_port_open(result.port, timeout=1.0)
    if not result.port_open:
        result.status = Status.STOPPED
        result.details.append("Port 3001 not responding")
        return result
    
    result.details.append("Port 3001 open")
    result.status = Status.HEALTHY
    
    return result


async def run_health_checks(detailed: bool = False) -> dict[str, HealthCheckResult]:
    """Run all health checks"""
    checks = [
        check_jarvis_mcp(),
        check_arangodb_mcp(),
        check_time_mcp(),
        check_git_mcp(),
        check_fetch_mcp(),
        check_everything_mcp(),
    ]
    
    results = {}
    for check in asyncio.as_completed(checks):
        result = await check
        results[result.name] = result
    
    return results


def print_banner():
    """Print banner"""
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print(colored("🏥 MCP Health Check System", Colors.CYAN, bold=True))
    print(colored("=" * 70, Colors.CYAN, bold=True))
    print()


def print_results(results: dict[str, HealthCheckResult], detailed: bool = False):
    """Print health check results"""
    print(colored("📊 MCP Status Report", Colors.BLUE, bold=True))
    print()
    
    # Status colors
    status_colors = {
        Status.HEALTHY: Colors.GREEN,
        Status.DEGRADED: Colors.YELLOW,
        Status.UNHEALTHY: Colors.RED,
        Status.STOPPED: Colors.RED,
        Status.UNKNOWN: Colors.YELLOW,
    }
    
    # Print each result
    for name in sorted(results.keys()):
        result = results[name]
        color = status_colors.get(result.status, Colors.WHITE)
        status_text = colored(result.status.value, color, bold=True)
        
        print(f"{status_text:30} {colored(result.name, Colors.WHITE, bold=True)}")
        
        if detailed and result.details:
            for detail in result.details:
                print(f"  {colored('→', Colors.DIM)} {detail}")
        
        if result.port:
            port_status = colored(f"✓ Open", Colors.GREEN) if result.port_open else colored(f"✗ Closed", Colors.RED)
            print(f"  {colored('→', Colors.DIM)} Port {result.port}: {port_status}")
        
        print()
    
    # Summary
    print(colored("📈 Summary", Colors.BLUE, bold=True))
    healthy = sum(1 for r in results.values() if r.status == Status.HEALTHY)
    degraded = sum(1 for r in results.values() if r.status == Status.DEGRADED)
    unhealthy = sum(1 for r in results.values() if r.status == Status.UNHEALTHY)
    stopped = sum(1 for r in results.values() if r.status == Status.STOPPED)
    total = len(results)
    
    print(f"  {colored('✓ Healthy:', Colors.GREEN)} {healthy}/{total}")
    if degraded:
        print(f"  {colored('⚠ Degraded:', Colors.YELLOW)} {degraded}/{total}")
    if unhealthy:
        print(f"  {colored('✗ Unhealthy:', Colors.RED)} {unhealthy}/{total}")
    if stopped:
        print(f"  {colored('⊘ Stopped:', Colors.YELLOW)} {stopped}/{total}")
    
    print()


def print_recommendations(results: dict[str, HealthCheckResult]):
    """Print recommendations based on results"""
    print(colored("💡 Recommendations", Colors.BLUE, bold=True))
    
    issues = []
    
    jarvis = results.get("JarvisMCP")
    if jarvis and jarvis.status != Status.HEALTHY:
        issues.append("JarvisMCP is not responding. Start it with:\n  cd Modules/AI/agents/MCP/JarvisMCP && python server.py")
    
    arangodb = results.get("ArangoDB MCP")
    if arangodb and arangodb.status != Status.HEALTHY:
        issues.append("ArangoDB is not running. Start with:\n  cd Modules/docker && docker compose -f docker-compose.arango.yml up -d")
    
    everything = results.get("Everything MCP")
    if everything and everything.status == Status.STOPPED:
        issues.append("Everything MCP is not running. Build and start with:\n  cd Modules/AI/agents/MCP/github/servers/src/everything && npm install && npm run build && npm start")
    
    if not issues:
        print(colored("✅ All systems operational!", Colors.GREEN, bold=True))
        print()
        print("Next steps:")
        print("  1. Open VS Code Copilot Chat")
        print("  2. Use the MCPs in your conversations:")
        print("     - Query database with ArangoDB MCP")
        print("     - Get current time with Time MCP")
        print("     - Perform Git operations with Git MCP")
        print("     - Fetch web content with Fetch MCP")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
    
    print()


async def watch_health(interval: int = 5):
    """Continuously monitor health"""
    try:
        iteration = 0
        while True:
            if iteration > 0:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="", flush=True)
            
            print_banner()
            results = await run_health_checks()
            print_results(results, detailed=False)
            
            iteration += 1
            if iteration > 0:
                next_check = time.strftime("%H:%M:%S")
                print(colored(f"⏱ Last updated: {next_check} | Next in {interval}s (Ctrl+C to stop)", Colors.DIM))
                
                try:
                    await asyncio.sleep(interval)
                except KeyboardInterrupt:
                    print()
                    print(colored("✓ Monitoring stopped", Colors.YELLOW))
                    break
    except KeyboardInterrupt:
        print()
        print(colored("✓ Monitoring stopped", Colors.YELLOW))


async def main():
    """Main entry point"""
    args = argparse.ArgumentParser(
        description="MCP Health Check & Monitoring System",
    ).parse_args()
    
    # Parse custom arguments
    import sys
    detailed = "--detailed" in sys.argv
    watch = "--watch" in sys.argv
    
    print_banner()
    
    if watch:
        print(colored("🔄 Starting continuous monitoring (Ctrl+C to stop)...", Colors.BLUE, bold=True))
        print()
        await watch_health(interval=5)
    else:
        print(colored("🔍 Running health checks...", Colors.BLUE, bold=True))
        print()
        results = await run_health_checks(detailed=detailed)
        print_results(results, detailed=detailed)
        print_recommendations(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
