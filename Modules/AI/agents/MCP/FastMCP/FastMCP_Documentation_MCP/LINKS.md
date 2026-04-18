# FastMCP Documentation MCP Server (VS Code Extension) — Links

## GitHub Repository
- **Repo:** https://github.com/abcSTARK/vscode-llm-fastmcp-context
- **Cloned to:** `github/vscode-llm-fastmcp-context/`
- **VS Code Marketplace:** https://marketplace.visualstudio.com/items?itemName=abcSTARK.vscode-llm-fastmcp-context
- **Changelog:** https://github.com/abcSTARK/vscode-llm-fastmcp-context/blob/main/CHANGELOG.md

## What It Does
A VS Code extension that auto-registers a remote **FastMCP Documentation MCP Server**
(`https://abcstark-server.fastmcp.app/mcp`) into both your workspace `.vscode/mcp.json`
and user-level `mcp.json`. This exposes a `#fastmcp_docs` tool to MCP-enabled LLM
agents (GitHub Copilot, Cline, RooCode, etc.) so they can query FastMCP documentation
directly from chat.

## Features
| Feature | Description |
|---------|-------------|
| Auto Registration | Adds server to `.vscode/mcp.json` and user `mcp.json` |
| First-Run Onboarding | Welcome page + optional auto-open of config file |
| Status Bar Indicator | Shows FastMCP + tool count; click to open user config |
| One-Click Command | `FastMCP: Add FastMCP Context Server` registers/re-registers |
| Configurable | Settings to disable auto-open and hide/move status bar item |
| Remote HTTP Server | Uses `https://abcstark-server.fastmcp.app/mcp` endpoint |

## MCP Server Config (added automatically)
```json
{
  "servers": {
    "fastmcp-documentation-resource": {
      "url": "https://abcstark-server.fastmcp.app/mcp",
      "type": "http"
    }
  },
  "inputs": []
}
```

## VS Code Commands
| Command Title | Command ID | Description |
|--------------|------------|-------------|
| FastMCP: Add FastMCP Context Server | `fastmcpContext.addServer` | Writes/updates mcp.json + (re)starts server |
| FastMCP: Show FastMCP Welcome | `fastmcpContext.showWelcome` | Re-opens onboarding webview |
| FastMCP: Open User MCP Configuration | `fastmcpContext.openUserMcpConfig` | Opens user-level mcp.json |
| [DEV] Reset FastMCP Onboarding State | `fastmcpContext.resetOnboarding` | Clears first-run flag |

## VS Code Settings
| Setting | Default | Description |
|---------|---------|-------------|
| `fastmcpContext.openConfigOnFirstInstall` | `true` | Auto-open config after first install |
| `fastmcpContext.statusBar.show` | `true` | Show status bar item |
| `fastmcpContext.statusBar.alignmentRight` | `false` | Align status bar item to the right |

## Using the FastMCP Docs Tool in Chat
Once registered, reference the tool via `#fastmcp_docs` in any MCP-enabled chat:
```
Use #fastmcp_docs and summarize FastMCP authentication.
Use #fastmcp_docs to list getting-started topics.
Compare FastMCP auth vs generic MCP auth (use #fastmcp_docs).
```
If the hashtag form doesn't trigger a tool call, say: _"Call the FastMCP docs tool and explain authentication."_

## Resources Referenced by This Extension
- **FastMCP Getting Started:** https://gofastmcp.com/getting-started/welcome
- **FastMCP Full Docs:** https://gofastmcp.com/
- **FastMCP LLMs.txt:** https://gofastmcp.com/llms-full.txt
- **MCP Protocol Docs:** https://modelcontextprotocol.io/docs/getting-started/intro

## Troubleshooting
| Problem | Fix |
|---------|-----|
| Server stays in `Starting` | Check network access to the URL, test with `curl` |
| Tool count not shown | MCP host may not support `listTools` — best-effort only |
| Config didn't open | Disable/enable setting or run `FastMCP: Open User MCP Configuration` |
| Duplicate entries | Run the Add command again — it safely overwrites the URL entry |

## Related
- **Parent module:** [../LINKS.md](../LINKS.md) — FastMCP Python library
- **FastMCP repo:** https://github.com/PrefectHQ/fastmcp
- **MCP module:** [../../LINKS.md](../../LINKS.md)
