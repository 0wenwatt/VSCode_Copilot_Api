# Playwright MCP — Links

## GitHub Repository
- **Repo:** https://github.com/microsoft/playwright-mcp
- **Cloned to:** `github/`
- **NPM:** https://www.npmjs.com/package/@playwright/mcp
- **License:** Apache-2.0

## Documentation
- **Docs home:** https://playwright.dev/
- **Getting Started:** https://playwright.dev/docs/intro
- **Playwright MCP Docs:** https://playwright.dev/docs/getting-started-mcp
- **Playwright CLI:** https://playwright.dev/docs/getting-started-cli
- **Test Runner:** https://playwright.dev/docs/intro
- **VS Code Extension:** https://playwright.dev/docs/getting-started-vscode
- **Codegen:** https://playwright.dev/docs/codegen
- **Trace Viewer:** https://playwright.dev/docs/trace-viewer-intro
- **Authentication:** https://playwright.dev/docs/auth

## Community & Support
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/playwright
- **Discord:** https://aka.ms/playwright/discord
- **Twitter:** https://twitter.com/playwrightweb
- **LinkedIn:** https://www.linkedin.com/company/playwrightweb
- **YouTube:** https://www.youtube.com/channel/UC46Zj8pDH5tDosqm1gd7WTg
- **Blog:** https://dev.to/playwright
- **Ambassadors:** https://playwright.dev/community/ambassadors
- **Learn Videos:** https://playwright.dev/community/learn-videos
- **Feature Videos:** https://playwright.dev/community/feature-videos

## Related Protocols & Standards
- **Model Context Protocol (MCP):** https://modelcontextprotocol.io/
- **MCP Architecture:** https://modelcontextprotocol.io/docs/learn/architecture
- **MCP Security Best Practices:** https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

## What It Is
Playwright MCP is a Model Context Protocol server that provides browser automation 
capabilities using Playwright. This server enables LLMs and coding agents to interact 
with web pages through structured accessibility snapshots, bypassing the need for 
screenshots or visually-tuned models.

## Key Features
- **Fast and lightweight** — Uses Playwright's accessibility tree, not pixel-based input
- **LLM-friendly** — No vision models needed; operates purely on structured data
- **Deterministic tool application** — Avoids ambiguity common with screenshot-based approaches
- **Multi-browser support** — Chromium, Firefox, WebKit, and Chrome channels
- **MCP client integration** — Works with VS Code, Cursor, Windsurf, Claude Desktop, and more

## Installation
```bash
# NPM (recommended)
npx @playwright/mcp@latest

# Or install globally
npm i -g @playwright/mcp@latest
```

## Quick Start Configuration
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## Playwright Vs. Alternatives
### Playwright MCP vs Playwright CLI
- **CLI**: Modern coding agents favor CLI-based workflows with SKILLs for token efficiency
- **MCP**: Better for agentic loops needing persistent state, rich introspection, iterative reasoning (exploratory automation, self-healing tests, long-running workflows)

## Available Capabilities
- Core automation (required)
- Tab management (required)
- Browser installation (required)
- Configuration (opt-in via `--caps=config`)
- Network tools (opt-in via `--caps=network`)
- Storage/cookies (opt-in via `--caps=storage`)
- DevTools (opt-in via `--caps=devtools`)
- Coordinate-based/Vision (opt-in via `--caps=vision`)
- PDF generation (opt-in via `--caps=pdf`)
- Test assertions (opt-in via `--caps=testing`)

## Language Support
- **TypeScript** 62.2%
- **CSS** 28.3%
- **JavaScript** 7.2%
- **Dockerfile** 1.5%
- **HTML** 0.8%

## Browser Support
- Chromium (Google Chrome)
- Firefox
- WebKit (Safari)
- Chrome channels (msedge, etc.)

## Platforms
- Linux
- macOS
- Windows

## Profile Management
- **Persistent Profile** — Stores session data between runs (default)
- **Isolated Profile** — Fresh context per session (testing)
- **Browser Extension** — Connect to existing browser sessions with logged-in state

## Configuration Options
Notable startup flags:
- `--headless` — Run in headless mode (headed by default)
- `--isolated` — Keep profile in memory, don't save to disk
- `--user-data-dir` — Custom profile directory
- `--storage-state` — Load cookies/local storage from file
- `--init-page` — TypeScript file to evaluate on page object
- `--init-script` — JavaScript file to add as initialization script
- `--viewport-size` — Browser viewport (e.g., "1280x720")
- `--device` — Emulate device (e.g., "iPhone 15")
- `--proxy-server` — HTTP/SOCKS proxy
- `--allowed-hosts` — Whitelist hosts the server serves
- `--blocked-origins` — Blocklist for origins

## Use Cases
- **Testing** — Full-featured test runner with auto-waiting and parallelism
- **Scripting** — Automation scripts for web tasks
- **AI Agents** — Browser automation for Claude, GitHub Copilot, and coding agents
- **Web Scraping** — Reliable automation with modern tooling
- **Session Recording** — Visual dashboard with live screencast previews

## Companies Using Playwright
- VS Code
- Bing
- Outlook
- Disney+ Hotstar
- Material UI
- ING
- Adobe
- React Navigation
- Accessibility Insights

## Requirements
- Node.js 18 or newer
- MCP-compatible client (VS Code, Cursor, Windsurf, Claude Desktop, etc.)
- Optional: Docker for containerized deployment

## Security
Playwright MCP is **not a security boundary**. See MCP Security Best Practices 
for guidance on securing your deployment.

## Multi-Language Support
Available for:
- TypeScript / JavaScript (primary)
- Python (via `pip install playwright`)
- .NET / C# (via NuGet)
- Java (via Maven)

## Contributing
- **Contributing Guide:** https://github.com/microsoft/playwright-mcp/blob/main/CONTRIBUTING.md
- **Security Policy:** https://github.com/microsoft/playwright-mcp/blob/main/SECURITY.md
- **Code of Conduct:** Available in repository
- **Contributors:** 64+ contributors

## Release Information
- **Latest Release:** v0.0.70 (3 weeks ago)
- **Total Releases:** 60+
- **GitHub Stars:** 31.1k+
- **GitHub Forks:** 2.5k+
