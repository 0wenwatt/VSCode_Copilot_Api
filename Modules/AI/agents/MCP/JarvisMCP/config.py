"""
JarvisMCP Configuration Management

Handles transport selection, ports, and runtime settings.
Configuration priority: env vars > config file > defaults
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv


class TransportType(Enum):
    """Available MCP transports."""
    HTTP = "http"
    STDIO = "stdio"
    SSE = "sse"


class JarvisConfig:
    """Central configuration for JarvisMCP."""

    def __init__(self):
        # Load environment variables from .env files
        load_dotenv(Path(__file__).parent / ".env")
        load_dotenv(Path(__file__).parent / "../../docker/.env")

        # Transport configuration
        self.transport: TransportType = TransportType(
            os.getenv("JARVIS_TRANSPORT", "http").lower()
        )
        self.http_host: str = os.getenv("JARVIS_HTTP_HOST", "127.0.0.1")
        self.http_port: int = int(os.getenv("JARVIS_HTTP_PORT", "8765"))
        self.stdio_fallback: bool = os.getenv("JARVIS_STDIO_FALLBACK", "true").lower() == "true"

        # Server metadata
        self.name: str = "JarvisMCP"
        self.version: str = "0.1.0"

        # Secret phrase (demo tool)
        self.secret_phrase: str = os.getenv("JARVIS_SECRET_PHRASE", "Jarvis is watching")

        # Features
        self.debug: bool = os.getenv("JARVIS_DEBUG", "false").lower() == "true"

    def get_transport_url(self) -> str:
        """Get the URL for connecting to this server."""
        if self.transport == TransportType.HTTP:
            return f"http://{self.http_host}:{self.http_port}/mcp"
        return "stdio"

    def __repr__(self) -> str:
        return (
            f"JarvisConfig("
            f"transport={self.transport.value}, "
            f"host={self.http_host}, "
            f"port={self.http_port}, "
            f"debug={self.debug})"
        )


# Global config instance
config = JarvisConfig()

if __name__ == "__main__":
    # Display current configuration
    print("JarvisMCP Configuration")
    print("=" * 60)
    print(f"Transport:      {config.transport.value}")
    print(f"HTTP Host:      {config.http_host}")
    print(f"HTTP Port:      {config.http_port}")
    print(f"Server URL:     {config.get_transport_url()}")
    print(f"Stdio Fallback: {config.stdio_fallback}")
    print(f"Secret Phrase:  {config.secret_phrase}")
    print(f"Debug Mode:     {config.debug}")
    print("=" * 60)
