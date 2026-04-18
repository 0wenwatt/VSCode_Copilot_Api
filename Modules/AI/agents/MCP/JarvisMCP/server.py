"""
JarvisMCP — FastMCP Server with HTTP & Stdio Support

Entry point for Jarvis MCP server.
Exposes tools, resources, and prompts to LLM clients.

Transport:
- PRIMARY: HTTP on localhost:8765
- FALLBACK: Stdio (for VS Code Copilot Chat direct execution)

Architecture:
    Clients (VS Code Copilot, Claude Desktop, etc.)
        ↓ HTTP (client) ← → (server) HTTP (JarvisMCP)
    JarvisMCP
        └── get_secret_phrase() → "Jarvis is watching"

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

import logging
import sys
from typing import Any

from fastmcp import FastMCP

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

# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool(description="Get the secret phrase from Jarvis")
def get_secret_phrase() -> str:
    """
    Returns Jarvis' secret phrase.

    This is a simple demo tool showing how FastMCP tools work.
    In production, this would be replaced with real functionality.

    Returns:
        str: The secret phrase configured in Jarvis
    """
    logger.info("get_secret_phrase() called")
    return config.secret_phrase


@mcp.tool(description="Get JarvisMCP server information")
def get_server_info() -> dict[str, Any]:
    """
    Returns information about the JarvisMCP server.

    Returns:
        dict: Server metadata including name, version, transport, etc.
    """
    logger.info("get_server_info() called")
    return {
        "name": config.name,
        "version": config.version,
        "transport": config.transport.value,
        "http_url": f"http://{config.http_host}:{config.http_port}",
        "debug_mode": config.debug,
    }


@mcp.tool(description="Echo a message")
def echo(message: str) -> str:
    """
    Echo the provided message.

    This is a simple test tool to verify tool communication works.

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

        # Run the server
        mcp.run(transport=config.transport.value, host=config.http_host, port=config.http_port)

    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
