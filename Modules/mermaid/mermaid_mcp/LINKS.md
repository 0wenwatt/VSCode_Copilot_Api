# MCP Mermaid — Links

## GitHub Repository
- **Repo:** https://github.com/hustcc/mcp-mermaid
- **Cloned to:** `github/mcp-mermaid/`
- **NPM:** https://www.npmjs.com/package/mcp-mermaid
- **Docker Hub:** https://hub.docker.com/repository/docker/susuperli/mcp-mermaid/tags
- **Smithery:** https://smithery.ai/server/@hustcc/mcp-mermaid

## What It Does
MCP server that generates Mermaid diagrams and charts from AI prompts dynamically.
Supports all Mermaid diagram types, multiple output formats, and multiple transport
protocols (stdio, SSE, Streamable HTTP). Listed in the official Mermaid community
integrations under LLM Integrations.

## Features
- Full Mermaid syntax support (all diagram types)
- Output formats: `base64`, `svg`, `mermaid`, `file`, `svg_url`, `png_url`
- `backgroundColor` and `theme` configuration
- Mermaid syntax validation (for multi-round AI correction)
- Transport protocols: `stdio` (default), `sse`, `streamable`
- Docker support (`susuperli/mcp-mermaid:latest`)

## MCP Configuration

### Windows (VS Code / Claude Desktop / Cline / Cherry Studio)
```json
{
  "mcpServers": {
    "mcp-mermaid": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "mcp-mermaid"]
    }
  }
}
```

### macOS / Linux
```json
{
  "mcpServers": {
    "mcp-mermaid": {
      "command": "npx",
      "args": ["-y", "mcp-mermaid"]
    }
  }
}
```

## Running as a Server (SSE / Streamable)

### Global install
```bash
npm install -g mcp-mermaid

mcp-mermaid -t sse            # SSE on port 3033  → http://localhost:3033/sse
mcp-mermaid -t streamable     # Streamable        → http://localhost:1122/mcp
```

### CLI Options
| Flag | Default | Description |
|------|---------|-------------|
| `-t, --transport` | `stdio` | `stdio`, `sse`, or `streamable` |
| `-p, --port` | `3033` | Port for SSE/streamable |
| `-e, --endpoint` | `/sse` (SSE), `/mcp` (streamable) | Endpoint path |

## Docker
```bash
docker pull susuperli/mcp-mermaid:latest

# SSE transport
docker run -p 3033:3033 susuperli/mcp-mermaid:latest --transport sse

# Streamable transport
docker run -p 1122:1122 susuperli/mcp-mermaid:latest --transport streamable --port 1122
```

## Access Points
| Transport | URL |
|-----------|-----|
| SSE | `http://localhost:3033/sse` |
| Streamable (local) | `http://localhost:1122/mcp` |
| Streamable (global) | `http://localhost:3033/mcp` |

## Related
- **Parent module:** [../LINKS.md](../LINKS.md) — Mermaid JS library
- **Mermaid integrations list:** https://mermaid.ai/open-source/ecosystem/integrations-community.html
