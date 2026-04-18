# GitHub Copilot API Gateway — Links

## GitHub Repository
- **Repo:** https://github.com/suhaibbinyounis/github-copilot-api-vscode
- **Cloned to:** `github/copilot-api-gateway/`
- **VS Code Marketplace:** https://marketplace.visualstudio.com/items?itemName=suhaibbinyounis.github-copilot-api-vscode
- **Open VSX:** https://open-vsx.org/extension/suhaibbinyounis/github-copilot-api-vscode
- **Homepage:** https://copilot-api.suhaib.in/

## Official Documentation
- **Official Docs:** https://notes.suhaib.in/docs/vscode/extensions/github-copilot-api-gateway/
- **Changelog:** https://github.com/suhaibbinyounis/github-copilot-api-vscode/blob/main/CHANGELOG.md
- **Contributing (incl. TLS setup):** https://github.com/suhaibbinyounis/github-copilot-api-vscode/blob/main/CONTRIBUTING.md
- **Issues:** https://github.com/suhaibbinyounis/github-copilot-api-vscode/issues

## What It Does
Exposes VS Code's `vscode.lm` API (Copilot, Gemini, Ollama, etc.) as a local
OpenAI-compatible HTTP server on `http://127.0.0.1:3030`. Works with any tool
that speaks OpenAI — LangChain, LangGraph, AutoGPT, Aider, Cursor, etc.

## API Endpoints (default port 3030)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server health check |
| `/docs` | GET | Interactive Swagger UI |
| `/v1/models` | GET | List all available models |
| `/v1/chat/completions` | POST | Chat completions (streaming supported) |
| `/v1/completions` | POST | Legacy completions API |
| `/v1/responses` | POST | OpenAI Responses API (2026 spec) |
| `/v1/messages` | POST | Anthropic Claude-compatible endpoint |
| `/v1beta/models/:model:generateContent` | POST | Google Gemini-compatible endpoint |
| `/v1/tools` | GET | List VS Code + MCP tools |
| `/v1/tools/call` | POST | Execute a tool directly |
| `/v1/mcp/servers` | GET | List connected MCP servers |

## Configuration (VS Code Settings)
```json
{
  "githubCopilotApi.server.port": 3030,
  "githubCopilotApi.server.host": "127.0.0.1",
  "githubCopilotApi.server.apiKey": "",
  "githubCopilotApi.server.autoStart": true
}
```

## Usage with LangChain / LangGraph
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://127.0.0.1:3030/v1",
    api_key="anything",       # no real key needed
    model="gpt-4o",           # or claude-3.5-sonnet, gemini-2.0-flash, etc.
)
```

## Supported Model Providers (auto-discovered via vscode.lm)
| Provider | Extension Required | Example Models |
|----------|-------------------|----------------|
| GitHub Copilot | GitHub Copilot Chat | gpt-4o, claude-3.5-sonnet, o3-mini |
| Google Gemini | Gemini Code Assist | gemini-2.0-flash |
| Ollama | Any Ollama VS Code ext | llama3, mistral, etc. |
| Any other | Any `vscode.lm` extension | Auto-discovered |

## Troubleshooting
- **TLS/HTTPS issue (v2.11.8-2.11.9 on Windows):** If the server fails to respond
  to HTTP requests, open VS Code Settings and ensure
  `githubCopilotApi.server.tls` is `false` or unset. This is a known bug with
  self-signed cert generation on Windows in recent builds.
- **Server not responding:** Confirm you clicked "Start Server" in the Gateway
  sidebar panel in VS Code (or set `autoStart: true`).
- **Models not appearing:** Ensure GitHub Copilot Chat extension is installed and
  you are signed in.

## Related Modules
- **`../`** — VS Code GitHub Copilot module (see `../LINKS.md`)
- **`../MCP/`** — MCP module — gateway exposes MCP servers via `/v1/mcp/servers`
