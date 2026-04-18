"""
JarvisMCP — FastMCP Server with Multi-MCP Composition

Entry point for Jarvis MCP server that acts as a gateway to multiple
MCP servers using FastMCP's native subprocess management.

Transport:
- PRIMARY: HTTP on localhost:8765
- FALLBACK: Stdio (for VS Code Copilot Chat direct execution)

Architecture:
    Clients (VS Code Copilot, Claude Desktop, etc.)
        ↓ HTTP (client) ← → (server) HTTP (JarvisMCP)
    JarvisMCP (FastMCP gateway)
        ├── Local tools (get_secret_phrase, echo, etc.)
        └── Remote MCPs (ArangoDB, etc.) via stdio subprocess

Configuration:
    Environment variables (.env or system):
    - JARVIS_TRANSPORT=http|stdio|sse (default: http)
    - JARVIS_HTTP_HOST=127.0.0.1 (default)
    - JARVIS_HTTP_PORT=8765 (default)
    - JARVIS_STDIO_FALLBACK=true|false (default: true)
    - JARVIS_SECRET_PHRASE="Jarvis is watching" (default)
    - JARVIS_DEBUG=true|false (default: false)
"""

from __future__ import annotations

import atexit
import logging
import os
import sys
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.client import Client
from fastmcp.client.transports import NodeStdioTransport
from fastmcp.server import create_proxy

from config import TransportType, config

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.INFO,
    format="[%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("JarvisMCP")

# ── FastMCP Server Instance ──────────────────────────────────────────────────
mcp = FastMCP(config.name, version=config.version)

# ── Track mounted servers for status reporting ─────────────────────────────────────
mounted_servers: dict[str, str] = {}


def register_remote_mcp(
    name: str,
    script_path: Path | str,
    env: dict[str, str] | None = None,
    cwd: str | None = None,
) -> bool:
    """
    Mount a remote MCP server via Node.js stdio transport.
    
    Args:
        name: Name of the MCP server
        script_path: Path to the Node.js MCP server script
        env: Environment variables for the subprocess
        cwd: Working directory for the subprocess
        
    Returns:
        True if successful, False otherwise
    """
    try:
        script_path = Path(script_path)
        
        logger.info(f"Mounting remote MCP: {name}")
        logger.debug(f"Script: {script_path}")
        logger.debug(f"CWD: {cwd}")
        
        if not script_path.exists():
            logger.error(f"✗ Script not found: {script_path}")
            return False
        
        # Create a Node.js stdio transport
        transport = NodeStdioTransport(
            script_path=str(script_path),
            env=env,
            cwd=cwd,
            keep_alive=True,
        )
        
        # Create a client and proxy
        client = Client(transport=transport)
        proxy = create_proxy(target=client, name=f"{name}_proxy")
        
        # Mount the proxy on the main server
        mcp.mount(server=proxy, namespace=name)
        
        mounted_servers[name] = str(script_path)
        logger.info(f"✓ {name} MCP mounted with namespace '{name}'")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to mount {name} MCP: {e}", exc_info=True)
        return False


def shutdown_remote_mcps():
    """Clean shutdown of remote MCPs (handled by FastMCP)."""
    logger.info("Shutting down...")
    # FastMCP handles cleanup of mounted servers automatically


# ── Local Tools ──────────────────────────────────────────────────────────────

@mcp.tool(description="Get the secret phrase from Jarvis")
def get_secret_phrase() -> str:
    """
    Returns Jarvis' secret phrase.
    
    Returns:
        str: The secret phrase configured in Jarvis
    """
    logger.info("get_secret_phrase() called")
    return config.secret_phrase


@mcp.tool(description="Get JarvisMCP server information")
def get_server_info() -> dict[str, Any]:
    """
    Returns information about the JarvisMCP server and mounted remote MCPs.
    
    Returns:
        dict: Server metadata including name, version, transport, mounted MCPs, etc.
    """
    logger.info("get_server_info() called")
    return {
        "name": config.name,
        "version": config.version,
        "transport": config.transport.value,
        "http_url": f"http://{config.http_host}:{config.http_port}",
        "debug_mode": config.debug,
        "mounted_remote_mcps": mounted_servers,
    }


@mcp.tool(description="Echo a message")
def echo(message: str) -> str:
    """
    Echo the provided message.
    
    Args:
        message (str): The message to echo
        
    Returns:
        str: The echoed message with a prefix
    """
    logger.info(f"echo() called with: {message}")
    return f"Jarvis echoes: {message}"


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        logger.info(f"JarvisMCP {config.version} Starting")
        logger.info(f"Using {config.transport.value} transport")
        logger.info(f"Configuration: {config}")

        # Register remote MCPs
        logger.info("Registering remote MCP servers...")
        
        # ArangoDB MCP - path from JarvisMCP to arangodb module
        # JarvisMCP is at: Modules/AI/agents/MCP/JarvisMCP
        # ArangoDB MCP is at: Modules/arangodb/arangodb_mcp/github/mcp-server-arangodb
        arangodb_path = Path(__file__).parent.parent.parent.parent.parent / "arangodb" / "arangodb_mcp" / "github" / "mcp-server-arangodb"
        logger.debug(f"Looking for ArangoDB MCP at: {arangodb_path}")
        
        if arangodb_path.exists():
            arangodb_build_path = arangodb_path / "build" / "index.js"
            if arangodb_build_path.exists():
                arango_env = {
                    "ARANGO_URL": "http://localhost:8893",
                    "ARANGO_DB": "_system",
                    "ARANGO_USERNAME": "root",
                    "ARANGO_PASSWORD": "test123",
                }
                
                register_remote_mcp(
                    "arangodb",
                    arangodb_build_path,
                    env=arango_env,
                    cwd=str(arangodb_path),
                )
            else:
                logger.warning(f"⚠ ArangoDB MCP build not found at {arangodb_build_path}")
        else:
            logger.warning(f"⚠ ArangoDB MCP not found at {arangodb_path}")
        
        # Playwright MCP - path from JarvisMCP to playwright module
        # Playwright MCP is at: Modules/playwright/github/packages/playwright-mcp
        playwright_path = Path(__file__).parent.parent.parent.parent.parent / "playwright" / "github" / "packages" / "playwright-mcp"
        logger.debug(f"Looking for Playwright MCP at: {playwright_path}")
        
        if playwright_path.exists():
            playwright_entry = playwright_path / "cli.js"
            if playwright_entry.exists():
                register_remote_mcp(
                    "playwright",
                    playwright_entry,
                    cwd=str(playwright_path),
                )
            else:
                logger.warning(f"⚠ Playwright MCP cli.js not found at {playwright_entry}")
        else:
            logger.warning(f"⚠ Playwright MCP not found at {playwright_path}")
        
        # Mermaid MCP - path from JarvisMCP to mermaid module
        # Mermaid MCP is at: Modules/mermaid/mermaid_mcp/github/mcp-mermaid
        mermaid_path = Path(__file__).parent.parent.parent.parent.parent / "mermaid" / "mermaid_mcp" / "github" / "mcp-mermaid"
        logger.debug(f"Looking for Mermaid MCP at: {mermaid_path}")
        
        if mermaid_path.exists():
            mermaid_build_path = mermaid_path / "build" / "index.js"
            if mermaid_build_path.exists():
                register_remote_mcp(
                    "mermaid",
                    mermaid_build_path,
                    cwd=str(mermaid_path),
                )
            else:
                logger.info(f"ℹ Mermaid MCP build not available at {mermaid_build_path}")
                logger.info("  To enable Mermaid MCP, run: cd Modules/mermaid/mermaid_mcp/github/mcp-mermaid && npm install && npm run build")
        else:
            logger.warning(f"⚠ Mermaid MCP not found at {mermaid_path}")

        # Set up graceful shutdown
        atexit.register(shutdown_remote_mcps)

        # Run the FastMCP server
        logger.info(f"Starting FastMCP HTTP server on {config.http_host}:{config.http_port}")
        mcp.run(transport=config.transport.value, host=config.http_host, port=config.http_port)

    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down gracefully...")
        shutdown_remote_mcps()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        shutdown_remote_mcps()
        sys.exit(1)
